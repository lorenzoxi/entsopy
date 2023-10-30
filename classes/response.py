import pandas as pd
from datetime import datetime
from dataclasses import dataclass
from lxml import etree
from utils.utils import *


@dataclass
class ResponseData:
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

        # ------------------------------------------------------

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

        # ------------------------------------------------------

        data = []
        resolution = (
            self.root.find(f".//{self.ns_name}:resolution", namespaces=self.nsmap)
        ).text

        time_start = (
            self.root.find(
                f".//{self.ns_name}:Period/{self.ns_name}:timeInterval/{self.ns_name}:start",
                namespaces=self.nsmap,
            )
        ).text
        time_end = (
            self.root.find(
                f".//{self.ns_name}:Period/{self.ns_name}:timeInterval/{self.ns_name}:end",
                namespaces=self.nsmap,
            )
        ).text

        date_start = datetime.strptime(time_start, "%Y-%m-%dT%H:%MZ")
        date_end = datetime.strptime(time_end, "%Y-%m-%dT%H:%MZ")

        max_no_points = get_timeseries_max_no_points(date_start, date_end, resolution)

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
            for i in range(1, max_no_points + 1):
                data_point = {}
                data_timing = get_time_data(date_start, resolution, position=i)
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

    def save_to_csv(self, file_name: str, path: str = ""):
        timestamp = (datetime.now()).strftime("%Y%m%dT%H%M%S")
        self.df.to_csv(
            f"{file_name}-{self.article_code}-{timestamp}.csv",
            index=True,
            index_label="id",
        )
