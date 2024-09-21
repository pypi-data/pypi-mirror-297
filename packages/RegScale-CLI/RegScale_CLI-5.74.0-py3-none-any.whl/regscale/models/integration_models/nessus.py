#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclasses for a Tenable integration """
import collections
import gc
import glob
import pickle
import shutil
import tempfile
import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from logging import Logger
from pathlib import Path
from typing import Any, List, Optional, Set, Tuple, Union
from uuid import UUID
from xml.etree.ElementTree import Element

import nessus_file_reader as nfr
from pydantic import BaseModel
from rich.progress import Progress
from tenable.io.exports.iterator import ExportsIterator

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    check_file_path,
    convert_datetime_to_regscale_string,
    create_progress_object,
    epoch_to_datetime,
    error_and_exit,
    get_current_datetime,
    log_memory,
)
from regscale.core.app.utils.nessus_utils import (
    IteratorConsumptionError,
    determine_available_space,
    determine_identifier,
    filter_severity,
    get_cpe_data,
    get_due_delta,
    get_minimum_severity,
    lookup_kev,
    software,
)
from regscale.core.app.utils.regscale_utils import check_module_id
from regscale.integrations.integration.issue import IntegrationIssue
from regscale.integrations.public.cisa import pull_cisa_kev
from regscale.models.integration_models.tenable_models.models import (
    Plugin,
    TenableBasicAsset,
    TenablePort,
    TenableScan,
)
from regscale.models.regscale_models import Asset, File, Issue, Link, ScanHistory, SoftwareInventory, Vulnerability
from regscale.models.regscale_models.regscale_model import T

REPORT_FILE = "report.txt"


class NessusReport(BaseModel, IntegrationIssue):
    """
    Tenable Nessus Report (maps to regscale vuln)
    """

    asset: TenableBasicAsset
    output: Optional[str]
    plugin: Plugin
    port: TenablePort
    scan: TenableScan
    severity: Optional[str] = None
    severity_id: int
    severity_default_id: int
    severity_modification_type: str
    first_found: Optional[datetime] = None
    last_fixed: Optional[datetime] = None
    last_found: Optional[datetime] = None
    state: Optional[str] = None
    indexed: Optional[datetime] = None

    @staticmethod
    def create_asset(config: dict, asset_properties: dict) -> Asset:
        """
        Create an asset

        :param dict config: The configuration dictionary
        :param dict asset_properties: A dictionary of asset properties
        :return: An Asset object
        :rtype: Asset
        """
        aws_ident = [aws for aws in asset_properties["all_tags"] if "aws-instance-instanceId" == aws["name"]]
        aws_identifier = aws_ident[0]["val"] if aws_ident else ""

        return Asset(
            **{
                "id": 0,
                "name": asset_properties["name"],
                "ipAddress": asset_properties["host_ip"],
                "isPublic": True,
                "status": "Active (On Network)",
                "assetCategory": "Hardware",
                "tenableId": asset_properties["tenable_id"],  # UUID from Nessus HostProperties tag
                "bLatestScan": True,
                "bAuthenticatedScan": True,
                "scanningTool": "Tenable",
                "assetOwnerId": asset_properties["user_id"],
                "netBIOS": asset_properties["netbios_name"],
                "macAddress": asset_properties["mac_address"],
                "assetType": "Other",
                "fqdn": asset_properties["fqdn"],
                "awsIdentifier": aws_identifier,
                "VLANId": asset_properties["vlan_id"],
                "location": asset_properties["location"],
                "operatingSystem": Asset.find_os(asset_properties["operating_system"]),
                "systemAdministratorId": config["userId"],
                "parentId": asset_properties["parent_id"],
                "parentModule": "securityplans",
            }
        )

    @staticmethod
    def get_vulnerability_data(file_vuln: Any) -> dict:
        """
        Get the vulnerability data

        :param Any file_vuln: A file vulnerability xml element
        :return: dict of vulnerability data
        :rtype: dict
        """

        def get(field_name: str) -> Optional[str]:
            """
            Get the field value

            :param str field_name: The field name to get
            :return: Field value
            :rtype: Optional[str]
            """
            try:
                result = file_vuln.find(field_name).text
            except AttributeError:
                result = None
            return result

        description = get("description")
        plugin_text = get("plugin_output")
        base = get("cvss_base_score")
        if base:
            cve_base_score = float(base)
        else:
            cve_base_score = 0.0
        cve = get("cve")
        synopsis = get("synopsis")
        solution = get("solution")
        severity = Vulnerability.determine_cvss3_severity_text(cve_base_score)
        return {
            "description": description,
            "synopsis": synopsis,
            "plugin_text": plugin_text,
            "cve": cve,
            "cve_base_score": cve_base_score,
            "severity": severity,
            "solution": solution,
        }

    @staticmethod
    def create_vulnerability(file_vuln: Any, asset_properties: dict, vulnerability_data: dict) -> Vulnerability:
        """Create a Vulnerability object

        :param Any file_vuln: File Vulnerability xml element
        :param dict asset_properties: A dictionary of asset properties
        :param dict vulnerability_data: A dictionary of vulnerability data
        :return: Vulnerability object
        :rtype: Vulnerability
        """
        extra_data = {
            "synopsis": vulnerability_data["synopsis"],
            "solution": vulnerability_data["solution"],
            "report_uuid": asset_properties["nessus_report_uuid"],
        }
        try:
            last_seen = epoch_to_datetime(asset_properties["last_scan"])
        except ValueError:
            last_seen = epoch_to_datetime("0")
        return Vulnerability(
            id=0,
            extra_data=extra_data,
            queryId=0,
            firstSeen="",
            cve=vulnerability_data["cve"],
            cvsSv3BaseScore=vulnerability_data["cve_base_score"],
            lastSeen=last_seen,
            dns=asset_properties["name"],
            title=file_vuln.attrib.get("pluginName"),
            ipAddress=asset_properties["scanner_ip"],
            createdById=asset_properties["user_id"],
            name=file_vuln.attrib.get("pluginName"),
            description=vulnerability_data["description"],
            severity=vulnerability_data["severity"],
            port=file_vuln.attrib.get("port"),
            protocol=file_vuln.attrib.get("protocol"),
            plugInId=file_vuln.attrib.get("pluginID"),
            plugInText=vulnerability_data["plugin_text"],
            plugInName=file_vuln.attrib.get("pluginName"),
            asset_name=asset_properties["name"],
            parentId=asset_properties["asset_id"],
            parentModule="assets",
        )

    @staticmethod
    def create_scan(
        asset_properties: dict,
        count_low: int,
        count_medium: int,
        count_high: int,
        count_critical: int,
    ) -> dict:
        """
        Create a scan

        :param dict asset_properties: A dictionary of asset properties
        :param int count_low: Scan count low
        :param int count_medium: Scan count medium
        :param int count_high: Scan count high
        :param int count_critical: Scan count critical
        :return: dict of scan data
        :rtype: dict
        """
        try:
            last_seen = epoch_to_datetime(asset_properties["last_scan"])
        except ValueError:
            last_seen = epoch_to_datetime("0")
        return {
            "id": 0,
            "scanningTool": "NESSUS",
            "scanDate": last_seen,
            "scannedIPs": asset_properties["asset_count"],
            "checks": count_low + count_medium + count_high + count_critical,
            "vInfo": 0,
            "vLow": count_low,
            "vMedium": count_medium,
            "vHigh": count_high,
            "vCritical": count_critical,
            "parentId": asset_properties["asset_id"],
            "parentModule": "assets",
            "createdById": asset_properties["user_id"],
            "lastUpdatedById": asset_properties["user_id"],
            "isPublic": True,
            "tenantsId": asset_properties.get("tenants_id", 1),  # Required for Scan object
            "tenableId": asset_properties["nessus_report_uuid"],
            "dateCreated": get_current_datetime(),
            "dateLastUpdated": get_current_datetime(),
        }

    @staticmethod
    def get_vulnerabilities(root: Element, file_asset: Any, asset_properties: dict) -> Tuple[List[Vulnerability], dict]:
        """
        Get the vulnerabilities of an asset

        :param Element root: XML Root
        :param Any file_asset: XML file asset
        :param dict asset_properties: A dictionary of asset properties
        :return: Tuple of vulnerabilities and scan
        :rtype: Tuple[List[Vulnerability], dict]
        """
        asset_name = file_asset.attrib.get("name")
        vulnerabilities = set()
        for file_vuln in root.iterfind(f"./Report/ReportHost[@name='{asset_name}']/ReportItem"):
            vulnerability_data = NessusReport.get_vulnerability_data(file_vuln)
            vulnerability = NessusReport.create_vulnerability(
                file_vuln,
                asset_properties,
                vulnerability_data,
            )
            vulnerabilities.add(vulnerability)
        counts = dict(collections.Counter([vuln.severity for vuln in vulnerabilities]))
        # Create a scan
        scan = NessusReport.create_scan(
            asset_properties,
            counts.get("low", 0),
            counts.get("medium", 0),
            counts.get("high", 0),
            counts.get("critical", 0),
        )
        return list(vulnerabilities), scan

    @staticmethod
    def update_vulnerability_scans(
        app: Application, scans: List[dict], vulnerabilities: List[dict]
    ) -> Tuple[List[Vulnerability], List[dict]]:
        """
        Update the vulnerability scans

        :param Application app: The application instance
        :param List[dict] scans: The scans
        :param List[dict] vulnerabilities: The vulnerabilities to be updated
        :return: The updated vulnerabilities and scans
        :rtype: Tuple[List[Vulnerability], List[dict]]
        """
        api = Api()
        res = api.post(url=app.config["domain"] + "/api/scanhistory/batchcreate", json=scans)
        inserted_scans = []
        updated_vulnerabilities: List[Vulnerability] = []
        if res.ok and res.status_code == 200:
            inserted_scans = res.json()
            for posted_scan in res.json():
                scan_id = posted_scan["id"]
                asset_id = posted_scan["parentId"]
                vulns: dict = next(
                    (item for item in vulnerabilities if item["scan_asset"] == asset_id),
                    {},
                )

                for vulnerability in vulns.get("vulns", []):
                    vulnerability.scanId = scan_id
                    updated_vulnerabilities.append(vulnerability)
        return updated_vulnerabilities, inserted_scans

    @staticmethod
    def process_file_asset(*args: Any) -> Tuple[dict, dict, dict]:
        """
        Process a file asset

        :param Any *args: Additional arguments
        :return: A tuple of dictionaries
        :rtype: Tuple[dict, dict, dict]
        """
        (
            root,
            regscale_ssp_id,
            cpe_list,
            file_asset,
            existing_assets,
            existing_assets_in_scan,
        ) = args[0]
        app = Application()
        logger = create_logger()
        logger.debug("Processing asset: %s", file_asset.attrib.get("name"))
        asset_properties = NessusReport.get_asset_properties(app, (root, cpe_list, file_asset, regscale_ssp_id))
        asset = NessusReport.create_asset(app.config, asset_properties)
        if asset not in existing_assets:
            res = asset.create()
        else:
            existing_asset = [existing_asset for existing_asset in existing_assets if asset == existing_asset][0]
            asset.id = existing_asset["id"]
            res = asset.save()

        if asset.id:
            asset_id = asset.id
        else:
            asset_id = res.id if res else 0
        asset_properties["asset_id"] = asset_id
        asset_properties["tenants_id"] = 1
        vulnerabilities, scan = NessusReport.get_vulnerabilities(
            root,
            file_asset,
            asset_properties=asset_properties,
        )
        dat = {"scan_asset": asset_id, "vulns": vulnerabilities}
        counter = dict(collections.Counter([vuln.severity for vuln in vulnerabilities]))
        app.logger.debug("Asset %s has %s vulnerabilities", asset_properties["name"], counter)
        existing_assets_in_scan.add(asset_id)
        return scan, dat, asset_properties

    @staticmethod
    def get_asset_properties(app: Application, *args: Any) -> dict:
        """
        Get the asset properties

        :param Application app: The application instance
        :param Any *args: Additional arguments
        :return: dict of asset properties
        :rtype: dict
        """
        logger = create_logger()
        (root, cpe_items, file_asset, regscale_ssp_id) = args[0]

        start = time.time()
        nessus_report_uuid = nfr.scan.server_preference_value(root, "report_task_id")
        nfr_start = time.time()
        asset_name = nfr.host.report_host_name(file_asset)
        temp = f"./Report/ReportHost[@name='{asset_name}']/HostProperties/tag"
        operating_system = nfr.host.detected_os(file_asset)
        netbios = nfr.host.netbios_network_name(root, file_asset)
        resolved_ip = nfr.host.resolved_ip(file_asset)
        scanner_ip = nfr.host.scanner_ip(root, file_asset)
        nfr_end = time.time()
        logger.debug("NFR functions ran in %s seconds", nfr_end - nfr_start)
        software_inventory = software(cpe_items, file_asset)  # Placeholder for CPE lookup,
        tag_map = {
            "id": "tenable_id",
            "host-ip": "host_ip",
            "host-fqdn": "fqdn",
            "mac-address": "macaddress",
            "HOST_START_TIMESTAMP": "begin_scan",
            "HOST_END_TIMESTAMP": "last_scan",
            "aws-instance-instanceId": "aws_instance_id",
            "aws-instance-vpc-id": "vlan_id",
            "aws-instance-region": "location",
        }

        tag_values = {tag_map[key]: "" for key in tag_map}

        for file_asset_tag in root.iterfind(temp):
            tag_name = file_asset_tag.attrib.get("name")
            tag_value = file_asset_tag.text
            if tag_name in tag_map:
                variable_name = tag_map[tag_name]
                tag_values[variable_name] = tag_value
        end = time.time()
        logger.debug("Time to process asset properties: %s", end - start)
        return {
            "name": asset_name,
            "operating_system": operating_system,
            "tenable_id": (tag_values["tenable_id"] if "tenable_id" in tag_values else ""),
            "netbios_name": netbios["netbios_computer_name"],
            "all_tags": [{"name": attrib.attrib["name"], "val": attrib.text} for attrib in root.iterfind(temp)],
            "mac_address": tag_values["macaddress"],
            "last_scan": tag_values["last_scan"],
            "user_id": app.config["userId"],
            "parent_id": regscale_ssp_id,
            "resolved_ip": resolved_ip,
            "asset_count": len(list(root.iter("ReportHost"))),
            "scanner_ip": scanner_ip,
            "host_ip": tag_values["host_ip"],
            "fqdn": tag_values["fqdn"],
            "software_inventory": software_inventory,
            "nessus_report_uuid": nessus_report_uuid,
            "aws_identifier": tag_values["aws_instance_id"],
            "vlan_id": tag_values["vlan_id"],
            "location": tag_values["location"],
        }

    @staticmethod
    def build_software_inventory(
        app: Application, asset_id: int, inventory: List[dict]
    ) -> Tuple[List[SoftwareInventory], List[SoftwareInventory]]:
        """
        Build and insert the software inventory

        :param Application app: The application instance
        :param int asset_id: The ID of the asset
        :param List[dict] inventory: The software inventory
        :return: A tuple of lists of inventory objects
        :rtype: Tuple[List[SoftwareInventory], List[SoftwareInventory]]
        """
        existing_inventory = []
        insert_inventory = []
        update_inventory = []
        res = Api().get(url=app.config["domain"] + f"/api/softwareInventory/getAllByParent/{asset_id}")
        if res.ok and res.status_code == 200:
            existing_inventory = res.json()
        for soft in inventory:
            software_inv = SoftwareInventory(
                **{
                    "id": 0,
                    "UUID": "",
                    "name": soft["title"],
                    "version": soft["version"],
                    "function": "",
                    "patchLevel": "",
                    "parentHardwareAssetId": asset_id,
                    "parentSoftwareAssetId": None,
                    "dateLastUpdated": None,
                    "createdById": app.config["userId"],
                    "dateCreated": None,
                    "lastUpdatedById": "",
                    "isPublic": True,
                }
            )
            if software_inv.name not in {inv["name"] for inv in existing_inventory if "name" in inv.keys()}:
                insert_inventory.append(software_inv)
            else:
                software_inv.id = [inv for inv in existing_inventory if software_inv.name == inv["name"]][0]["id"]
                update_inventory.append(software_inv)
        return insert_inventory, update_inventory

    @staticmethod
    def process_assets(
        assets: List[Element],
        root: Element,
        regscale_ssp_id: int,
        cpe_list: List[str],
        existing_assets: List[dict],
        existing_assets_in_scan: Set[int],
    ) -> Tuple[List[dict], List[dict], List[dict]]:
        """
        Process the assets

        :param List[Element] assets: A list of assets
        :param Element root: The root element
        :param int regscale_ssp_id: The ID of the parent security plan
        :param List[str] cpe_list: A list of CPE elements
        :param List[dict] existing_assets: A list of existing assets
        :param Set[int] existing_assets_in_scan: A set of existing assets in the scan
        :return: A tuple of lists of vulnerabilities, scans, and asset properties
        :rtype: Tuple[List[dict], List[dict], List[dict]]
        """
        app = Application()
        logger = app.logger
        vulns_to_post = []
        scans_to_post = []
        asset_props = []
        with ThreadPoolExecutor() as executor:
            futures = []
            start = time.time()
            end = time.time()
            for file_asset in assets:
                logger.debug("CPE element list created in %s seconds", end - start)
                future = executor.submit(
                    NessusReport.process_file_asset,
                    (
                        root,
                        regscale_ssp_id,
                        cpe_list,
                        file_asset,
                        existing_assets,
                        existing_assets_in_scan,
                    ),
                )
                futures.append(future)
            for future in as_completed(futures):
                scans, vuln_data, asset_properties = future.result()
                vulns_to_post.append(vuln_data)
                scans_to_post.append(scans)
                asset_props.append(asset_properties)
        return vulns_to_post, scans_to_post, asset_props

    @staticmethod
    def process_inventory(asset_props: List[dict]) -> Tuple[List[SoftwareInventory], List[SoftwareInventory]]:
        """
        Process the software inventory

        :param List[dict] asset_props: A list of asset properties
        :return: A tuple of lists of inventory objects
        :rtype: Tuple[List[SoftwareInventory], List[SoftwareInventory]]
        """
        app = Application()
        inventory_to_insert = []
        inventory_to_update = []
        for asset in asset_props:
            (
                insert_inventory,
                update_inventory,
            ) = NessusReport.build_software_inventory(
                app=app,
                asset_id=asset["asset_id"],
                inventory=asset["software_inventory"],
            )
            inventory_to_insert.extend(insert_inventory)
            inventory_to_update.extend(update_inventory)
        return inventory_to_insert, inventory_to_update

    @staticmethod
    def process_nessus_file(file: str, regscale_ssp_id: int) -> Tuple[Set[Issue], List[T], List[dict]]:
        """
        Process a Nessus file

        :param str file: The full path to the Nessus file
        :param int regscale_ssp_id: The ID of the parent security plan
        :return: A tuple of sets of issues,  existing assets and vulns to post
        :rtype: Tuple[Set[Issue], List[T], List[dict]]
        """
        app = Application()
        job_progress = create_progress_object()
        root = nfr.file.nessus_scan_file_root_element(file)
        _, cpe_list = get_cpe_data()

        app.logger.info("Processing Nessus file: %s", file)
        assets = nfr.scan.report_hosts(root)
        existing_assets = Asset.get_all_by_parent(parent_id=regscale_ssp_id, parent_module="securityplans")
        existing_assets_in_scan = set()
        inserted_scans = []

        with job_progress:
            vulns_to_post, scans_to_post, asset_props = NessusReport.process_assets(
                assets,
                root,
                regscale_ssp_id,
                cpe_list,
                existing_assets,
                existing_assets_in_scan,
            )
            inventory_to_insert, inventory_to_update = NessusReport.process_inventory(asset_props)
            vulns, scans = NessusReport.update_vulnerability_scans(app, scans_to_post, vulns_to_post)
            Vulnerability.post_vulnerabilities(app=app, vulnerabilities=vulns)
            NessusReport.process_software_inventory(
                job_progress=job_progress,
                inventory_to_insert=inventory_to_insert,
                inventory_to_update=inventory_to_update,
            )
            inserted_scans.extend(scans)
        issues_to_save = NessusReport.generate_issues(regscale_ssp_id=regscale_ssp_id, vulns_to_post=vulns_to_post)
        return issues_to_save, existing_assets, vulns_to_post

    @staticmethod
    def process_software_inventory(
        job_progress: Progress,
        inventory_to_insert: List[SoftwareInventory],
        inventory_to_update: List[SoftwareInventory],
    ) -> None:
        """
        Process the software inventory

        :param Progress job_progress: The progress object
        :param List[SoftwareInventory] inventory_to_insert: A list of software inventory objects to insert
        :param List[SoftwareInventory] inventory_to_update: A list of software inventory objects to update
        :return: None
        :rtype: None
        """
        app = Application()
        inventory_task = job_progress.add_task(
            "[#f68d1f]Processing software inventory..",
            total=len(inventory_to_insert) + len(inventory_to_update),
        )
        with ThreadPoolExecutor() as executor:
            futures: List[Future] = []
            for inventory in inventory_to_insert:
                futures.append(
                    executor.submit(
                        SoftwareInventory.insert,
                        app=app,
                        obj=inventory,
                    )
                )
            for inventory in inventory_to_update:
                futures.append(
                    executor.submit(
                        SoftwareInventory.update,
                        app=app,
                        obj=inventory,
                    )
                )
            for future in as_completed(futures):
                future.result()
                job_progress.update(inventory_task, advance=1)

    @staticmethod
    def move_files(ssp_id: int, file_collection: List[str], logger: Logger) -> None:
        """
        Move files to processed directory

        :param int ssp_id: The ID of the parent security Plan
        :param List[str] file_collection: A list of files to move_files
        :param Logger logger: The logger Instance

        :return: None
        :rtype: None
        """
        for file in file_collection:
            api = Api()
            # Create processed directory if it doesn't exist, and copy file to it.
            file_path = Path(file)
            new_file_path = ""
            processed_dir = file_path.parent / "processed"
            check_file_path(str(processed_dir.absolute()))
            logger.debug("Moving %s to %s", file, processed_dir / file)
            try:
                if ssp_id:
                    file_name = f"{file_path.stem}_{get_current_datetime('%Y_%m_%d-%I_%M_%S_%p')}".replace(" ", "_")
                    # Rename to friendly file name and post to Regscale
                    new_file_path = file_path.rename(file_path.parent / (file_name + ".nessus"))
                    logger.info(
                        "Renaming %s to %s, and posting to RegScale...",
                        file_path.name,
                        new_file_path.name,
                    )
                    File.upload_file_to_regscale(
                        file_name=str(new_file_path.absolute()),
                        parent_id=ssp_id,
                        parent_module="securityplans",
                        api=api,
                    )
                    shutil.move(new_file_path, processed_dir)
            except shutil.Error:
                logger.debug(
                    "File %s already exists in %s",
                    new_file_path.name,
                    processed_dir,
                )
            except OSError as e:
                logger.error("Error moving file: %s", e)

    @staticmethod
    def process_files(file_collection: list, regscale_ssp_id: int) -> Tuple[Set[Issue], Set[int], List[dict]]:
        """
        Process multiple Nessus files

        :param list file_collection: List of Nessus files to process
        :param int regscale_ssp_id: RegScale SSP ID number
        :return: Tuple of issues to create, scanned assets and vulnerabilities to create
        :rtype: Tuple[Set[Issue], Set[int], List[dict]]
        """
        insert_issues: Set[Issue] = set()
        assets_scanned: Set[int] = set()
        for file in file_collection:
            (issues_to_save, existing_asset_in_scan, vulns_to_post) = NessusReport.process_nessus_file(
                file, regscale_ssp_id
            )
            insert_issues.update(issues_to_save)
            assets_scanned.update(existing_asset_in_scan)
        return insert_issues, assets_scanned, vulns_to_post

    @staticmethod
    def process_nessus_files(regscale_ssp_id: int, folder_path: Path) -> None:
        """
        Process multiple Nessus files

        :param int regscale_ssp_id: The ID of the parent security plan
        :param Path folder_path: The full path to the folder of Nessus files
        :return: None
        :rtype: None
        :raises ValueError: If the SSP ID is invalid
        """

        def lookup_asset(assets: List[Asset], issue: Issue) -> dict:
            """
            Lookup asset

            :param List[Asset] assets: A list of assets
            :param Issue issue: The issue object
            :return: A dictionary with an asset_id as the key, and associated vulnerabilities (from current report)
            :rtype: dict
            """
            asset_identifier = issue.assetIdentifier
            matched_asset = [inv for inv in assets if inv.name == asset_identifier]
            if matched_asset:
                # Get vulnerabilities for this issue
                try:
                    matched_vulns = [
                        vuln for vuln in vulnerabilities_dict[matched_asset[0].id] if issue.title == vuln.plugInName
                    ]
                    return {matched_asset[0].id: matched_vulns}
                except KeyError:
                    # No vulnerabilities for this asset are present in this scan!
                    return {matched_asset[0].id: []}
            return {}

        app = Application()
        api = Api()
        logger = create_logger()
        mod_check = check_module_id(parent_id=regscale_ssp_id, parent_module="securityplans")
        if not mod_check:
            raise ValueError("Invalid SSP ID, please make sure the SSP exists " + "on your RegScale system.")
        if isinstance(folder_path, str):
            folder_path = Path(folder_path)
        file_collection = glob.glob(str(folder_path / "*.nessus"))
        if len(file_collection) == 0:
            error_and_exit("No Nessus files found in folder path.")
        # Loop through nessus files in folder_path
        insert_issues, assets_scanned, vulns_to_post = NessusReport.process_files(file_collection, regscale_ssp_id)
        # Save
        new_issues = Issue.bulk_insert(app, issues=list(insert_issues))
        logger.info("Generating Issue Links")
        new_links = []
        # Update links
        for iss in new_issues:
            if iss.id:
                # Create Link
                link = Link(
                    title=f"Tenable Plugin {iss.pluginId}",
                    url=f"https://www.tenable.com/plugins/nessus/{iss.pluginId}",
                    parentID=iss.id,
                    parentModule="issues",
                )
                new_links.append(link)
        all_issues: List[Issue] = Issue.get_all_by_parent(parent_id=regscale_ssp_id, parent_module="securityplans")
        Link.bulk_insert(api=api, links=new_links)
        vulnerabilities_dict = {vuln["scan_asset"]: vuln["vulns"] for vuln in vulns_to_post}
        issue_vuln_map = {iss.id: lookup_asset(assets_scanned, iss) for iss in all_issues if iss.status == "Open"}

        # Automatically close issues
        NessusReport.close_issues(issue_vuln_map=issue_vuln_map)
        # move files
        NessusReport.move_files(ssp_id=regscale_ssp_id, file_collection=file_collection, logger=logger)

    @staticmethod
    def prepare_tenable_data(
        existing_assets: List[dict],
        vulns: Union[ExportsIterator, UUID],
        logger: Logger,
        **kwargs,
    ) -> Tuple[Any, List[ScanHistory]]:
        """
        Prepares Tenable data for download

        :param List[dict] existing_assets: A list of existing Asset objects to compare against
        :param Union[ExportsIterator, UUID] vulns: An iterable of NessusReport objects to prepare for download
        :param Logger logger: The logger object to use for logging
        :param dict **kwargs: The keyword arguments for this function
        :raises IteratorConsumptionError: If there was a problem downloading Tenable data
        :return: A tuple containing a file wrapper and a list of scans.
        :rtype: Tuple[Any, List[ScanHistory]]
        """
        log_memory()
        tmp_dir = tempfile.TemporaryDirectory()
        logger.info("Preparing to download Tenable Data ...")
        report_vulns, count, saved_count, file_count = [], 0, 0, 0
        index = 0
        has_data = False
        job_progress = create_progress_object()
        # give the user a progress object so they know it is working
        with job_progress:
            fetching_task = job_progress.add_task(
                "[#f8b737]Fetching vulnerability data from Tenable...",
                total=100,
            )
            for index, tenable_data in enumerate(vulns):
                # don't let the user the process is done prematurely
                if index and job_progress.tasks[fetching_task].completed < 95:
                    job_progress.update(fetching_task, advance=0.05)
                if vulns.page:
                    has_data = True
                (
                    report_vulns,
                    count,
                    saved_count,
                    file_count,
                ) = NessusReport.process_tenable_data(
                    index,
                    tenable_data,
                    vulns,
                    report_vulns,
                    count,
                    saved_count,
                    file_count,
                    tmp_dir,
                    **kwargs,
                )
            # mark the task complete
            job_progress.update(fetching_task, advance=100)
        if has_data and index == 0:
            raise IteratorConsumptionError("There was a problem downloading Tenable data, please try again.")

        logger.info(
            "%i of %i records saved for processing.",
            saved_count,
            index + 1,
        )
        logger.info("Processing scan data from Tenable...")
        existing_scans = ScanHistory.convert_from_tenable(
            tmp_dir.name,
            existing_assets=existing_assets,
        )
        report_vulns.clear()
        gc.collect()
        log_memory()
        NessusReport.create_report(tmp_dir.name, existing_scans)

        return tmp_dir, existing_scans

    @staticmethod
    def process_tenable_data(
        index: int,
        tenable_data: Any,
        vulns: ExportsIterator,
        report_vulns: List["NessusReport"],
        count: int,
        filtered: int,
        file_count: int,
        tmp_dir: Any,
        **kwargs: dict,
    ) -> Tuple[List["NessusReport"], int, int, int]:
        """
        Process Tenable data

        :param int index: The index of the current record
        :param Any tenable_data: The Tenable data to process
        :param ExportsIterator vulns: The Tenable data iterator
        :param List[NessusReport] report_vulns: The list of NessusReport objects
        :param int count: The count of records processed
        :param int filtered: The count of records filtered
        :param int file_count: The count of files processed
        :param Any tmp_dir: The temporary directory
        :param dict **kwargs: The keyword arguments for this function
        :return: A tuple containing the report_vulns list and the file count
        :rtype: Tuple[List[NessusReport], int, int, int]
        """

        report = NessusReport(**tenable_data)
        report_vulns.append(report)
        count += 1
        filtered += 1

        if index and len(report_vulns) == len(vulns.page):
            # when count matches size of vulns.page, dump to disk
            report_vulns, file_count = NessusReport.dump_report_to_disk(
                report_vulns, file_count, tmp_dir, vulns, **kwargs
            )
            NessusReport.log_download_progress(index=index, saved_count=filtered)
            # reset the count and start a new page
            count = 0

        return report_vulns, count, filtered, file_count

    @staticmethod
    def log_download_progress(**kwargs: dict) -> None:
        """
        Log the download progress

        :param dict **kwargs The keyword arguments for this function
        :rtype: None
        """
        app = Application()
        saved_count = kwargs.get("saved_count", 0)
        if saved_count > 0 and saved_count % 500 == 0:
            app.logger.info("Processed  %i records ..", saved_count)

    @staticmethod
    def dump_report_to_disk(
        report_vulns: List["NessusReport"],
        file_count: int,
        tmp_dir: Any,
        vulns: ExportsIterator,
        **kwargs: dict,
    ) -> Tuple[List["NessusReport"], int]:
        """
        Dump report to disk

        :param List[NessusReport] report_vulns: The list of NessusReport objects
        :param int file_count: The count of files processed
        :param Any tmp_dir: The temporary directory
        :param ExportsIterator vulns: The Tenable data iterator
        :param dict **kwargs: The keyword arguments for this function
        :return: A tuple containing the report_vulns list and the file count
        :rtype: Tuple[List[NessusReport], int]
        """
        vuln_file = tempfile.NamedTemporaryFile(dir=tmp_dir.name, delete=False)
        if report_vulns:
            try:
                with open(vuln_file.name, "wb") as vuln_file_wrapper:
                    pickle.dump(report_vulns, vuln_file_wrapper)
                    file_count += 1
                    if file_count == 1:
                        NessusReport.check_disk_space(vuln_file_wrapper, vulns, **kwargs)
                    vuln_file.close()
                report_vulns.clear()
                gc.collect()
            except OSError as e:
                error_and_exit(f"Error saving file: {e}")

        return report_vulns, file_count

    @staticmethod
    def check_disk_space(vuln_file_wrapper: Any, vulns: ExportsIterator, **kwargs: dict) -> None:
        """Check if there is enough disk space to process Tenable data

        :param Any vuln_file_wrapper: The file wrapper for the vulnerability file
        :param ExportsIterator vulns: The Tenable data iterator
        :param dict **kwargs: The keyword arguments for this function
        :rtype: None
        """
        client = kwargs.get("client")
        app = kwargs.get("app")
        total_chunks = (client.exports.status(export_uuid=vulns.uuid, export_type="vulns"))["total_chunks"]
        file_size = vuln_file_wrapper.tell()
        app.logger.debug("Space needed: %i", file_size * total_chunks)
        if file_size * total_chunks > determine_available_space():
            error_and_exit("The estimated space to process Tenable data is below the current available space.")

    @staticmethod
    def create_regscale_vuln(**kwargs: dict) -> Tuple[List["NessusReport"], List[ScanHistory]]:
        """
        Prepares Tenable data for download

        :param dict **kwargs: The keyword arguments for this function
        :return: A tuple containing two lists: NessusReport objects and Scan objects
        :rtype: Tuple[List[NessusReport], List[ScanHistory]]
        """
        app = kwargs.get("app")
        parent_id = kwargs.get("parent_id")
        parent_module = kwargs.get("parent_module")
        existing_assets = kwargs.get("existing_assets")
        report = kwargs.get("report")
        existing_scans = kwargs.get("existing_scans")
        existing_vulns = kwargs.get("existing_vulns")
        asset = None
        report_asset: TenableBasicAsset = report.asset
        res = [asset for asset in existing_assets if asset["otherTrackingNumber"] == report_asset.uuid]
        if res:
            asset = res[0]
            parent_id = asset.id if isinstance(asset, Asset) else asset["id"]
            parent_module = "assets"

        # refresh existing scans
        if scans := [
            scan for scan in existing_scans if scan.tenableId == report.scan.uuid and scan.parentId == parent_id
        ]:
            regscale_vuln = Vulnerability(
                id=0,
                uuid=report.scan.uuid,
                scanId=scans[0].id,
                parentId=parent_id,
                parentModule=parent_module,
                lastSeen=convert_datetime_to_regscale_string(report.last_found),
                firstSeen=convert_datetime_to_regscale_string(report.first_found),
                daysOpen=None,
                dns=report_asset.hostname,
                ipAddress=report_asset.ipv4,
                mitigated=None,
                operatingSystem=(report_asset.operating_system[0] if report_asset.operating_system else None),
                port=report.port.port,
                protocol=report.port.protocol,
                severity="moderate" if report.severity == "medium" else report.severity,
                plugInName=report.plugin.name,
                plugInId=report.plugin.id,
                cve=None,
                vprScore=None,
                tenantsId=0,
                exploitAvailable=report.plugin.exploit_available,
                cvss3BaseScore=report.plugin.cvss3_base_score,
                title=f"{report.output} on asset {report_asset.hostname}",
                description=report.output,
                plugInText=report.plugin.description,
                createdById=app.config["userId"],
                lastUpdatedById=app.config["userId"],
                dateCreated=convert_datetime_to_regscale_string(datetime.now()),
            )
            if regscale_vuln not in existing_vulns:
                return regscale_vuln
            if existing_vulns:
                regscale_vuln.id = [vuln for vuln in existing_vulns if vuln == regscale_vuln][0].id
                return regscale_vuln

        return None

    @staticmethod
    def sync_to_regscale(
        vulns: Union[ExportsIterator, UUID],
        parent_id: int,
        parent_module="securityplans",
        **kwargs,
    ) -> None:
        """
        Synchronizes Tenable vulns to RegScale

        :param Union[ExportsIterator, UUID] vulns: An iterable of NessusReport objects to prepare for download
        :param int parent_id: The ID of the parent object associated with the data
        :param str parent_module: The name of the parent module associated with the data, defaults to "securityplans"
        :param kwargs: The keyword arguments for this function
        :rtype: None
        """
        logger = create_logger()
        app = Application()
        existing_assets = Asset.get_all_by_parent(parent_id=parent_id, parent_module=parent_module)
        if len(existing_assets) == 0:
            error_and_exit(
                "In order to sync vulnerabilities, you must have assets for the provided Security Plan in RegScale."
            )
        tmp_dir, existing_scans = NessusReport.prepare_tenable_data(
            existing_assets, vulns, logger, client=kwargs.get("client"), app=app
        )
        existing_vulns = NessusReport.existing_vulns(existing_scans=existing_scans, app=app)
        logger.info("Saving Tenable Vulnerabilities to RegScale...")
        threads = 100
        filelst = list(Path(tmp_dir.name).glob("*"))
        asset_vuln_tmp_dir = NessusReport.convert_to_asset_vuln_files(filelst)
        count_posted = 0
        asset_vuln_file_list = list(Path(asset_vuln_tmp_dir.name).glob("*"))
        if not asset_vuln_file_list:
            return
        logger.info("Iterating through cached data to update RegScale ..")
        for file in asset_vuln_file_list:
            file_vulns = []
            if file.suffix == ".txt":
                # skip text files
                continue
            with open(file, "rb") as fp:
                file_vulns.extend(pickle.load(fp))
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = [
                    executor.submit(
                        NessusReport.create_regscale_vuln,
                        parent_id=parent_id,
                        parent_module=parent_module,
                        report=report,
                        existing_assets=existing_assets,
                        existing_scans=existing_scans,
                        existing_vulns=existing_vulns,
                        app=app,
                    )
                    for report in file_vulns
                ]
            new_vulns = NessusReport.process_vuln_results(futures, file_vulns, existing_vulns, logger=logger)
            logger.debug("Found %s new vulnerabilities", len(new_vulns))
            log_memory()
            responses = Vulnerability.post_vulnerabilities(app=app, vulnerabilities=new_vulns)
            count_posted += len([res for res in responses if isinstance(res, bytes)])
        asset_vuln_tmp_dir.cleanup()
        if count_posted:
            logger.info("Successfully posted %i new vulnerabilities", count_posted)
        # move report with pathlib
        if Path(tmp_dir.name).exists():
            # assert artifacts exists
            artifacts = Path("./artifacts")
            artifacts.mkdir(exist_ok=True)
            # user friendly date string
            now = get_current_datetime("%Y_%m_%d-%I_%M_%S")
            report_path = artifacts / f"sync_vulns_report_{now}.txt"
            shutil.copy(Path(tmp_dir.name) / REPORT_FILE, report_path)
            logger.info("Report saved to %s", report_path)

    @staticmethod
    def convert_to_asset_vuln_files(filelst: List):
        """
        Convert a List of pickle files representing pages of Tenable IO to a dict of asset hostnames with Tenable IO
        vulns as the payload.

        :param List filelst: A list of file paths to pickle files
        :return None
        """
        res = {}
        for file in filelst:
            with open(file, "rb") as fp:
                try:
                    vulns = pickle.load(fp)
                except pickle.UnpicklingError:
                    # skip the file if it can't be unpickled
                    continue
                hosts = {
                    vuln.asset.hostname for vuln in vulns if vuln.asset and isinstance(vuln.asset, TenableBasicAsset)
                }
                for host in hosts:
                    if host not in res:
                        res[host] = []
                    # Filter out the info vulns
                    res[host].extend([vuln.dict() for vuln in vulns if vuln.asset.hostname == host])
                del vulns
                gc.collect()
        # tmp_dir.close()
        log_memory()
        host_temp = tempfile.TemporaryDirectory()
        for host in res.keys():
            # Pickle every host list, this will make it easier to process and not have to worry about memory
            with tempfile.NamedTemporaryFile(dir=host_temp.name, delete=False) as host_file:
                try:
                    with open(host_file.name, "wb") as fp:
                        # We can be assured that every item in the list contains all the reports for a given host
                        pickle.dump([NessusReport(**vuln) for vuln in res[host]], fp)
                        # clear data from dictionary after dump
                        res[host].clear()
                except OSError as e:
                    error_and_exit(f"Error saving file: {e}")
        del res
        gc.collect()
        log_memory()
        return host_temp

    @staticmethod
    def process_vuln_results(
        futures: List[Future],
        vulns: List["NessusReport"],
        existing_vulns: List[Vulnerability],
        **kwargs,
    ) -> list[Vulnerability]:
        """
        Processes the results of the vulnerability futures

        :param List[Future] futures: A list of Future objects representing the vulnerability futures
        :param List["NessusReport"] vulns: A list of NessusReport objects representing vulnerabilities
        :param List[Vulnerability] existing_vulns: A list of existing Vulnerability objects to compare against
        :param kwargs The keyword arguments
        :return: list[Vulnerability]
        """
        app = Application()
        new_vulns = []
        count = 0
        logger = kwargs.get("logger")
        for future in as_completed(futures):
            count += 1
            if count % 5000 == 0:
                logger.info(
                    "Processed %i of %i %s.",
                    count,
                    len(vulns),
                    "vulnerability" if len(new_vulns) == 1 else "vulnerabilities",
                )
            regscale_vuln = future.result()
            if regscale_vuln is not None and (regscale_vuln not in existing_vulns):
                new_vulns.append(regscale_vuln)
        counters = collections.Counter(
            [v.severity for v in [fut.result() for fut in as_completed(futures) if fut.result()]]
        )
        if len(new_vulns) > 0:
            logger.debug("Vuln Breakdown: %s", dict(counters))
            logger.info(
                "Found %i new %s with a severity > %s.",
                len(new_vulns),
                "vulnerability" if len(new_vulns) == 1 else "vulnerabilities",
                app.config["tenableMinimumSeverityFilter"],
            )
        return new_vulns

    @staticmethod
    def existing_vulns(existing_scans: List[ScanHistory], app: Application) -> List[Vulnerability]:
        """Existing Vulns

        :param List[ScanHistory] existing_scans: A list of existing scans
        :param Application app: Application Instance
        :return: List of Vulns
        :rtype: List[Vulnerability]
        """
        results = []
        api = Api()
        for scan_id in {scan.id for scan in existing_scans}:
            results.extend(api.get(url=app.config["domain"] + f"/api/vulnerability/getAllByParent/{scan_id}").json())
        return [Vulnerability(**vuln) for vuln in results]

    @staticmethod
    def generate_issues(
        regscale_ssp_id: int,
        vulns_to_post: List[dict],
    ) -> Set[Issue]:
        """
        Generate issues from a Nessus file

        :param int regscale_ssp_id: The ID of the parent security plan
        :param List[dict] vulns_to_post: A list of vulnerabilities to be posted
        :return: A tuple containing : new issues and updated issues
        :rtype: Set[Issue]
        """
        app = Application()
        # Update the issues in the SSP
        app.logger.info("Generating issues...")

        # Get all assets in SSP
        existing_issues = Issue.get_all_by_parent(parent_id=regscale_ssp_id, parent_module="securityplans")
        # Filter tenable issues
        tenable_issues = [iss for iss in existing_issues if iss.pluginId or iss.tenableId]
        # Create issues
        issues = NessusReport.create_regscale_issues(vulns_to_post, regscale_ssp_id)

        # create updated issues
        new_issues = NessusReport.update_issue_sets(issues, tenable_issues)
        counter = collections.Counter([iss.severityLevel for iss in new_issues])
        app.logger.debug("New Issue Breakdown (before filter): %s", dict(counter))
        # Filter issues that are >= moderate
        new_issues = {
            iss for iss in new_issues if iss.severityLevel not in ["IV - Not Assigned", "III - Low - Other Weakness"]
        }

        return new_issues

    @staticmethod
    def update_issue_sets(issues: Set[Issue], tenable_issues: List[Issue]) -> Set[Issue]:
        """
        Determine if an issue is new.

        :param Set[Issue] issues: A list of issue sets to be updated
        :param List[Issue] tenable_issues: A list of tenable issues
        :return: A tuple containing two sets of issues: new issues and updated issues
        :rtype: Set[Issue]
        """

        def is_new_issue() -> bool:
            """
            Check if an issue is new.

            :return: True if the issue is new, False otherwise.
            :rtype: bool
            """
            return issue.title not in {iss.title for iss in tenable_issues}

        new_issues: Set[Issue] = set()

        for issue in issues:
            if is_new_issue():
                new_issues.add(issue)

        return new_issues

    @staticmethod
    def create_issue(
        app: Application,
        item: Vulnerability,
        asset: Asset,
        severity: Optional[str],
        plugin_id: Union[str, int],
        regscale_ssp_id: int,
        kev_due_date: Optional[str],
        kev_list: Any,
    ) -> Issue:
        """Create RegScale Issue

        :param Application app: The application instance
        :param Vulnerability item: The NessusReport object
        :param Asset asset: The related asset
        :param Optional[str] severity: The severity of the issue
        :param Union[str, int] plugin_id: The plugin ID
        :param int regscale_ssp_id: The ID of the parent security plan
        :param Optional[str] kev_due_date: The due date of the issue (from the KEV)
        :param Any kev_list: The list of CVEs (from the KEV)
        :return: An Issue object
        :rtype: Issue
        """
        fmt = "%Y-%m-%d %H:%M:%S"
        poam = severity.lower() in ["low", "moderate", "high", "critical"]
        iss = Issue(
            isPoam=poam,
            title=item.title,
            description=item.description,
            status="Open",
            severityLevel=Issue.assign_severity(severity),
            issueOwnerId=app.config["userId"],
            pluginId=str(plugin_id),
            assetIdentifier=determine_identifier(asset),
            securityPlanId=regscale_ssp_id,
            recommendedActions=item.extra_data["solution"],
            cve=item.cve,
            kevList=kev_list,
            autoApproved="No",
        )
        iss.originalRiskRating = iss.assign_risk_rating(severity)
        iss.dateFirstDetected = item.lastSeen
        if not iss.dateFirstDetected:
            iss.dateFirstDetected = datetime.strftime(datetime.now(), fmt)
        if kev_due_date and (datetime.strptime(kev_due_date, fmt) > datetime.now()):
            iss.dueDate = kev_due_date
        elif kev_due_date and (datetime.strptime(kev_due_date, fmt) <= datetime.now()):
            iss.dueDate = datetime.strftime(datetime.now() + timedelta(days=1), fmt)
        else:
            due_dt = datetime.strptime(iss.dateFirstDetected, fmt) + timedelta(get_due_delta(app, severity))
            iss.dueDate = datetime.strftime(due_dt, fmt)
            if due_dt < datetime.now():
                iss.dueDate = datetime.strftime(datetime.now() + timedelta(get_due_delta(app, severity)), fmt)
        iss.identification = "Vulnerability Assessment"
        iss.tenableNessusId = item.extra_data["report_uuid"]
        iss.parentId = regscale_ssp_id
        iss.parentModule = "securityplans"
        iss.basisForAdjustment = "Tenable Nessus import."
        return iss

    @staticmethod
    def create_regscale_issues(vulns: List[dict], regscale_ssp_id: int) -> Set[Issue]:
        """
        Create RegScale issues from Nessus

        :param List[dict] vulns: The list of vulnerabilities
        :param int regscale_ssp_id: The ID of the parent security plan
        :return: A list of issues
        :rtype: Set[Issue]
        """
        app = Application()
        minimum_severity = get_minimum_severity(app)
        list_of_vulns = NessusReport.get_vuln_list(vulns)
        issues: Set[Issue] = set()
        existing_assets: List[Asset] = Asset.get_all_by_parent(parent_id=regscale_ssp_id, parent_module="securityplans")

        kev_data = pull_cisa_kev()
        kev_due_date = None
        kev_list = None
        for item in filter_severity(list_of_vulns, minimum_severity):
            asset = next(asset for asset in existing_assets if asset.id == item.parentId)
            severity = {dat.severity for dat in list_of_vulns if dat.plugInName == item.title}.pop()
            plugin_id = {str(dat.plugInId) for dat in list_of_vulns if dat.plugInName == item.title}.pop()

            if app.config["issues"]["tenable"]["useKev"]:
                kev, kev_due_date = lookup_kev(item.cve, kev_data)
                kev_list = kev["cveID"] if kev else None
            iss = NessusReport.create_issue(
                app,
                item,
                asset,
                severity,
                plugin_id,
                regscale_ssp_id,
                kev_due_date,
                kev_list,
            )
            if (iss.assetIdentifier, iss.title) not in {(issue.assetIdentifier, issue.title) for issue in issues}:
                issues.add(iss)
        return issues

    @staticmethod
    def get_vuln_list(vulns: List[dict]) -> List[Vulnerability]:
        """
        Convert a list of data to a list of Vulnerability objects

        :param List[dict] vulns: A list of vulnerabilities
        :return: A list of vulnerabilities
        :rtype: List[Vulnerability]
        """
        list_of_vulns = []
        for dat in vulns:
            if "vulns" in dat.keys():
                list_of_vulns.extend(dat["vulns"])
        return list_of_vulns

    def pull(self):
        """
        Pull inventory from an Integration platform into RegScale
        """
        pass

    @staticmethod
    def create_report(tmp_dir: str, scan_data: list) -> None:
        """
        Create a report of the processed Tenable data

        :param str tmp_dir: The temporary directory
        :param list scan_data: The scan data
        :rtype: None
        """

        def pad_with_hyphens(s: str, total_length: int = 80) -> str:
            """
            Pad a string with hyphens on each side

            :param str s: The string to be padded
            :param int total_length: The total length of the padded string, defaults to 80
            :return: Padded string with hyphens
            :rtype: str
            """
            # Calculate the number of hyphens needed on each side
            num_hyphens_each_side = (total_length - len(s)) // 2

            # If the total length is not an even number, add an extra hyphen on the right side
            right_padding = num_hyphens_each_side if len(s) % 2 == 0 else num_hyphens_each_side + 1

            # Return the padded string
            return f"{'-' * num_hyphens_each_side}{s}{'-' * right_padding}"

        # Generate a temporary report file, we can update with scan data now
        # and move when the vulnerability data is posted
        report_file = Path(tmp_dir) / REPORT_FILE
        # Get datetime string
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not report_file.exists():
            # Pad line to 80 char
            line1 = pad_with_hyphens(f"Tenable IO Report - {now}")
            line2 = pad_with_hyphens("SCAN HISTORY")
        with open(Path(tmp_dir) / REPORT_FILE, "a+") as f:
            f.write(line1 + "\n" + line2 + "\n\n")
            for scan in scan_data:
                f.write(
                    f"{scan.parentModule}: {scan.parentId} critical: {scan.vCritical} high: {scan.vHigh} moderate: {scan.vMedium} low: {scan.vLow} info: {scan.vInfo}\n"
                )
