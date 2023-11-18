from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse


def sanitize_from_urn(tag: str) -> str:
    """Remove urn from tag."""
    return tag.split("}")[-1]


def is_in_list(tag: str, lists: list) -> bool:
    """Check if tag is in lists."""
    for lista in lists:
        if tag in lista:
            return True
    return False


def get_wellformed_tag(
    tag: str, parent_tag: str, parent_tag_to_exlude: list = [], ns_name: str = "ns"
) -> bool:
    """Get a well formed tag."""
    tag = sanitize_from_urn(tag)
    parent_tag = sanitize_from_urn(parent_tag)
    res = ""

    if parent_tag in parent_tag_to_exlude or parent_tag == "":
        res = f"{ns_name}:{tag}"
    else:
        res = f"{ns_name}:{parent_tag}/{ns_name}:{tag}"

    return res


def get_wellformed_key(
    suffix: str,
    tag: str,
    string_to_replace: str = "ns:",
    string_to_replace_with: str = "",
) -> str:
    """Get a well formed key."""
    tmp = tag.replace(string_to_replace, string_to_replace_with)
    tmp = tmp.replace("/", ".")
    return f"{suffix}.{tmp}"


def get_wellformed_tags(
    root, parent_to_exclude: list = [], lists_to_check: list[list] = [[]]
):
    res = []
    if root != None:
        for element in root.xpath(".//*"):
            tag = element.tag
            parent_tag = element.getparent().tag if element.getparent() != None else ""
            well_formed_tag = get_wellformed_tag(
                tag=tag, parent_tag=parent_tag, parent_tag_to_exlude=parent_to_exclude
            )
            is_tag_in_lists = is_in_list(
                well_formed_tag,
                lists_to_check,
            )
            if is_tag_in_lists == False:
                res.append(well_formed_tag)
                lists_to_check.append([well_formed_tag])
    return res


def get_xml_data(root, elements_list: [], nsmap: dict, suffix: str) -> dict:
    row = {}
    for element in elements_list:
        e = root.find(
            element,
            namespaces=nsmap,
        )
        if e != None:
            tmp = e.text.strip()
            if len(tmp) != 0:
                key = get_wellformed_key(suffix=f"{suffix}", tag=element)
                row[key] = tmp
        else:
            key = get_wellformed_key(suffix=f"{suffix}", tag=element)
            row[key] = "na"
    return row


def get_point_quantity(period, i, nsmap, ns_name: str = "ns"):
    res = ""
    is_point_existing = False
    point = period.xpath(
        f".//{ns_name}:Point/{ns_name}:position[text()='{i}']", namespaces=nsmap
    )

    if point != None and len(point) > 0:
        is_point_existing = True
        point = point[0]

    if is_point_existing == False:
        res = "na"
    else:
        res = (point.getparent().find(f".//{ns_name}:quantity", namespaces=nsmap)).text
    return res


def get_period_dates(period, nsmap, ns_name: str = "ns") -> tuple:
    start = None
    end = None
    t_start = period.find(f".//{ns_name}:start", namespaces=nsmap)
    t_end = period.find(f".//{ns_name}:end", namespaces=nsmap)

    if t_start != None:
        start = t_start.text

    if t_end != None:
        end = t_end.text

    start_date = datetime.strptime(start, "%Y-%m-%dT%H:%MZ")
    end_date = datetime.strptime(end, "%Y-%m-%dT%H:%MZ")

    return start_date, end_date


def get_period_resolution(period, nsmap, ns_name: str = "ns"):
    res = ""
    resolution = period.find(f".//{ns_name}:resolution", namespaces=nsmap)
    if resolution != None:
        res = resolution.text
    return res


def interval_divided_by_delta(
    start_date: datetime, end_date: datetime, rel_delta: relativedelta
):
    current_time = start_date
    number_of_deltas = 0

    while current_time < end_date:
        current_time = current_time + rel_delta
        number_of_deltas += 1
        # print(type(current_time), type(rel_delta))

    return number_of_deltas


def get_resolution_relativedelta(resolution: str, multiplier: int = 1) -> relativedelta:
    rel_delta = timedelta()
    if resolution == "P1Y":
        rel_delta = relativedelta(years=(1 * multiplier))
    elif resolution == "PT1M":
        rel_delta = relativedelta(months=(1 * multiplier))
    elif resolution == "P7D":
        rel_delta = relativedelta(days=(7 * multiplier))
    elif resolution == "P1D":
        rel_delta = relativedelta(days=(1 * multiplier))
    elif resolution == "PT60M":
        rel_delta = relativedelta(minutes=(60 * multiplier))
    elif resolution == "PT30M":
        rel_delta = relativedelta(minutes=(30 * multiplier))
    elif resolution == "PT15M":
        rel_delta = relativedelta(minutes=(15 * multiplier))

    return rel_delta


def max_number_of_points(period, nsmap, ns_name: str = "ns"):
    start, end = get_period_dates(period=period, nsmap=nsmap, ns_name=ns_name)
    resolution = get_period_resolution(period=period, nsmap=nsmap, ns_name=ns_name)
    rel_delta = get_resolution_relativedelta(resolution=resolution)
    number_of_points = interval_divided_by_delta(
        start_date=start, end_date=end, rel_delta=rel_delta
    )
    # print("no points: ", number_of_points)
    return number_of_points


def get_namespace_from_root(root, namespace_name: str = "ns"):
    nmsp = root.nsmap
    res = {}
    for key, value in nmsp.items():
        res[namespace_name] = value

    return res


def get_minutes_from_resolution(resolution: str) -> int:
    minutes = 0
    if resolution == "PT60M":
        minutes = 60
    elif resolution == "PT30M":
        minutes = 30
    elif resolution == "PT15M":
        minutes = 15
    return minutes


def get_mtu(
    date: datetime,
    calculate_only_mtu: bool = False,
    prefix: str = "",
) -> str | dict:
    mtu_elements = {}
    mtu = date
    mtu_elements[f"{prefix}mtu"] = mtu.strftime("%Y-%m-%dT%H:%MZ")

    mtu_elements[f"{prefix}year"] = mtu.year
    mtu_elements[f"{prefix}month"] = mtu.month
    mtu_elements[f"{prefix}day"] = mtu.day
    mtu_elements[f"{prefix}week"] = mtu.isocalendar()[1]
    mtu_elements[f"{prefix}hour"] = mtu.hour
    mtu_elements[f"{prefix}minute"] = mtu.minute

    return mtu_elements


def get_time_data(
    date_start: datetime,
    date_end: datetime,
    resolution: str,
) -> dict:
    mtu_start = get_mtu(
        prefix="mtu.start.",
        date=date_start,
    )
    mtu_end = get_mtu(prefix="mtu.end.", date=date_end)

    mtu = {**mtu_start, **mtu_end}
    return mtu


def extract_code_from_key(dict_list: [dict], key: str) -> str:
    for d in dict_list:
        if d["key"] == key:
            return d["code"]
    return ""
