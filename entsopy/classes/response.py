import json
import pandas as pd
from dataclasses import dataclass
from lxml import etree
from const import DIRS
from utils.utils import *


@dataclass
class ResponseData:
    """
    Represents a response data object.

    Args:
        content (str): The content of the response.
        article_code (str): The article code.

    Attributes:
        root (etree.Element): The root element of the XML content.
        article_code (str): The article code.
        ns_name (str): The namespace name.
        nsmap (dict): The namespace map.
        data (list): The list of data rows.
        df (pd.DataFrame): The data in a pandas DataFrame.
        max_no_points (int): The maximum number of points.
        resolution (str): The resolution of the timeserie period.

    Methods:
        save_to_csv(file_name: str, path: str = ""): Saves the data to a CSV file.
        fill_missing_psr_types(all_psr_types: list = []): Fills missing PSR types in the data.
    """

    def __init__(self, content: str, article_code: str):
        content = content
        self.root = etree.XML(content)
        self.article_code = article_code
        self.ns_name = "ns"
        self.nsmap = get_namespace_from_root(self.root)
        document_elements = []
        timeseries_elements = []
        period_elements = []
        mkt_elements = []
        point_elements = []

        tms = self.root.find(
            f".//{self.ns_name}:TimeSeries",
            namespaces=self.nsmap,
        )

        period = self.root.find(
            f".//{self.ns_name}:Period",
            namespaces=self.nsmap,
        )

        mktpsrtype = self.root.find(
            f".//{self.ns_name}:MktPSRType",
            namespaces=self.nsmap,
        )

        point = self.root.find(
            f".//{self.ns_name}:Point",
            namespaces=self.nsmap,
        )

        point_elements = get_wellformed_tags(
            point,
            parent_to_exclude=[],
            lists_to_check=[point_elements],
        )

        period_elements = get_wellformed_tags(
            period,
            parent_to_exclude=["Period"],
            lists_to_check=[period_elements, point_elements],
        )

        mkt_elements = get_wellformed_tags(
            mktpsrtype,
            parent_to_exclude=["MktPSRType"],
            lists_to_check=[mkt_elements, point_elements],
        )

        timeseries_elements = get_wellformed_tags(
            tms,
            parent_to_exclude=["TimeSeries"],
            lists_to_check=[
                timeseries_elements,
                period_elements,
                point_elements,
                mkt_elements,
            ],
        )

        document_elements = get_wellformed_tags(
            self.root,
            parent_to_exclude=["GL_MarketDocument"],
            lists_to_check=[
                document_elements,
                timeseries_elements,
                period_elements,
                point_elements,
                mkt_elements,
            ],
        )
        document_res = get_xml_data(
            self.root, document_elements, self.nsmap, suffix="document"
        )

        data = []
        resolution = (
            self.root.find(f".//{self.ns_name}:resolution", namespaces=self.nsmap)
        ).text

        initial_time_start = (
            self.root.find(
                f".//{self.ns_name}:time_Period.timeInterval/{self.ns_name}:start",
                namespaces=self.nsmap,
            )
        ).text
        initial_time_end = (
            self.root.find(
                f".//{self.ns_name}:Period/{self.ns_name}:timeInterval/{self.ns_name}:end",
                namespaces=self.nsmap,
            )
        ).text

        date_start = datetime.strptime(initial_time_start, "%Y-%m-%dT%H:%MZ")
        date_end = datetime.strptime(initial_time_end, "%Y-%m-%dT%H:%MZ")
        self.date_start = date_start
        self.date_end = date_end

        timeseries = self.root.findall(
            f".//{self.ns_name}:TimeSeries", namespaces=self.nsmap
        )
        for tms in timeseries:
            row = {}
            data_tm = get_xml_data(
                tms, timeseries_elements, self.nsmap, suffix="timeseries"
            )

            period = tms.find(
                f".//{self.ns_name}:Period",
                namespaces=self.nsmap,
            )
            data_period = get_xml_data(
                period, period_elements, self.nsmap, suffix="period"
            )

            mkt = tms.find(
                f".//{self.ns_name}:MktPSRType",
                namespaces=self.nsmap,
            )
            data_mkt = get_xml_data(mkt, mkt_elements, self.nsmap, suffix="mkt")

            max_no_points = max_number_of_points(period, self.nsmap)

            for i in range(1, max_no_points + 1):
                data_point = {}

                # start_date, end_date = get_period_dates(period, self.nsmap)

                data_timing = get_time_data(
                    date_start=date_start,
                    date_end=date_start,
                    resolution=resolution,
                    position=i,
                )

                data_point["position"] = i
                data_point["quantity"] = get_point_quantity(period, i, self.nsmap)
                row = {
                    **document_res,
                    **data_tm,
                    **data_period,
                    **data_mkt,
                    **data_timing,
                    **data_point,
                }
                data.append(row)

        self.data = data
        self.df = pd.DataFrame(self.data)
        self.max_no_points = max_no_points
        self.resolution = resolution

        if (
            self.article_code == "14.1.A" or self.article_code == "16.1.B&C"
        ):  # TODO: refactor
            print("filling missing psr types")
            self.fill_missing_psr_types()
        elif self.article_code == "14.1.D":
            self.fill_missing_psr_types(all_psr_types=["B16", "B18", "B19"])

    def save_to_csv(self, file_name: str, path: str = ""):
        timestamp = (datetime.now()).strftime("%Y%m%dT%H%M%S")
        self.df.to_csv(
            f"{file_name}-{self.article_code}-{timestamp}.csv",
            index=True,
            index_label="id",
        )

    def fill_missing_psr_types(
        self,
        all_psr_types: list = (
            psr["code"] for psr in (json.load(open(DIRS["type_psrtypes"], "r")))
        ),
    ):
        psr_type = self.df["mkt.psrType"].unique()

        missing_psr_types = [psr for psr in all_psr_types if psr not in psr_type]

        for i in range(1, self.max_no_points + 1):
            for missing_psr_type in missing_psr_types:
                new_row = self.df[:1]
                new_row["quantity"] = "na"
                new_row["position"] = i
                new_row["mkt.psrType"] = missing_psr_type
                self.df = pd.concat([self.df, new_row])

                data_time = get_time_data(
                    self.date_start,
                    self.date_start,
                    position=i,
                    resolution=self.resolution,
                )

                for key, value in data_time.items():
                    new_row[key] = value

        if self.article_code == "14.1.A" or self.article_code == "16.1.B&C":
            self.df = self.df.sort_values(by=["mkt.psrType"])

        self.df = self.df.reset_index(drop=True)
