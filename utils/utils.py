from datetime import datetime, timedelta


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


def get_xml_data(root, elements_list: [], nsmap: dict, suffix: str) -> list:
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


def get_namespace_from_root(root, namespace_name: str = "ns"):
    nmsp = root.nsmap
    res = {}
    for key, value in nmsp.items():
        res[namespace_name] = value

    return res


def get_timeseries_max_no_points(
    date_start: datetime, date_end: datetime, resolution: str
):
    no_days = (date_end - date_start).days
    res = 0

    if resolution == "P1Y":  # TODO: check
        res = 1
    elif resolution == "PT1M":  # TODO: check
        res = 12
    elif resolution == "P7D":  # TODO: check
        res = 48
    elif resolution == "PT60M":
        res = 24 * no_days
    elif resolution == "PT30M":
        res = 48 * no_days
    elif resolution == "PT15M":
        res = 96 * no_days

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


def calculate_mtu(
    date: datetime,
    position: int,
    minutes: int,
    calculate_only_mtu: bool = True,
) -> str | dict:
    mtu = date + timedelta(minutes=minutes * (position - 1))
    mtu_str = mtu.strftime("%Y-%m-%dT%H:%MZ")

    if calculate_only_mtu == False:
        mtu_dict = {}
        mtu_dict["mtu.day"] = mtu.day
        mtu_dict["mtu.month"] = mtu.month
        mtu_dict["mtu.year"] = mtu.year
        return mtu_dict

    return mtu_str


def get_time_data(date: datetime, resolution: int, position: int):
    minutes = 0
    minutes = get_minutes_from_resolution(resolution)
    mtu_dict = calculate_mtu(
        date=date,
        position=(position - 1),
        minutes=minutes,
        calculate_only_mtu=False,
    )
    mtu_end = calculate_mtu(date=date, position=position, minutes=minutes)

    mtu_dict["mtu.end"] = mtu_end
    return mtu_dict


def extract_code_from_key(dict_list: [dict], key: str) -> str:
    for d in dict_list:
        if d["key"] == key:
            return d["code"]
    return ""
