from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse


def sanitize_from_urn(tag: str) -> str:
    """
    Remove the URN prefix from a tag.

    Args:
        tag (str): The tag to sanitize.

    Returns:
        str: The sanitized tag.
    """
    return tag.split("}")[-1]


def is_in_list(tag: str, lists: list) -> bool:
    """
    Check if a tag is present in any of the lists.

    Args:
        tag (str): The tag to check.
        lists (list): The lists to search in.

    Returns:
        bool: True if the tag is found in any of the lists, False otherwise.
    """
    for lista in lists:
        if tag in lista:
            return True
    return False


def get_wellformed_tag(
    tag: str, parent_tag: str, parent_tag_to_exlude: list = [], ns_name: str = "ns"
) -> bool:
    """
    Get the well-formed tag based on the parent tag and exclusion list.

    Args:
        tag (str): The tag.
        parent_tag (str): The parent tag.
        parent_tag_to_exlude (list, optional): The list of parent tags to exclude. Defaults to [].
        ns_name (str, optional): The namespace name. Defaults to "ns".

    Returns:
        bool: The well-formed tag.
    """
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
    """
    Get the well-formed key based on the suffix and tag.

    Args:
        suffix (str): The suffix.
        tag (str): The tag.
        string_to_replace (str, optional): The string to replace in the tag. Defaults to "ns:".
        string_to_replace_with (str, optional): The string to replace with. Defaults to "".

    Returns:
        str: The well-formed key.
    """
    tmp = tag.replace(string_to_replace, string_to_replace_with)
    tmp = tmp.replace("/", ".")
    return f"{suffix}.{tmp}"


def get_wellformed_tags(
    root, parent_to_exclude: list = [], lists_to_check: list[list] = [[]]
):
    """
    Get the well-formed tags from the root element.

    Args:
        root: The root element.
        parent_to_exclude (list, optional): The list of parent tags to exclude. Defaults to [].
        lists_to_check (list[list], optional): The lists to check for tag presence. Defaults to [[]].

    Returns:
        list: The well-formed tags.
    """
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
    """
    Get the XML data from the root element.

    Args:
        root: The root element.
        elements_list (list): The list of elements to extract data from.
        nsmap (dict): The namespace map.
        suffix (str): The suffix for the keys.

    Returns:
        dict: The extracted XML data.
    """
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
    """
    Get the quantity of a point in a period.

    Args:
        period: The period element.
        i: The position of the point.
        nsmap: The namespace map.
        ns_name (str, optional): The namespace name. Defaults to "ns".

    Returns:
        str: The quantity of the point.
    """
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
    """
    Get the start and end dates of a period.

    Args:
        period: The period element.
        nsmap: The namespace map.
        ns_name (str, optional): The namespace name. Defaults to "ns".

    Returns:
        tuple: The start and end dates of the period.
    """
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
    """
    Get the resolution of a period.

    Args:
        period: The period element.
        nsmap: The namespace map.
        ns_name (str, optional): The namespace name. Defaults to "ns".

    Returns:
        str: The resolution of the period.
    """
    res = ""
    resolution = period.find(f".//{ns_name}:resolution", namespaces=nsmap)
    if resolution != None:
        res = resolution.text
    return res


def interval_divided_by_delta(
    start_date: datetime, end_date: datetime, rel_delta: relativedelta
):
    """
    Calculate the number of deltas between two dates.

    Args:
        start_date (datetime): The start date.
        end_date (datetime): The end date.
        rel_delta (relativedelta): The relative delta.

    Returns:
        int: The number of deltas.
    """
    current_time = start_date
    number_of_deltas = 0

    while current_time < end_date:
        current_time = current_time + rel_delta
        number_of_deltas += 1
        # print(type(current_time), type(rel_delta))

    return number_of_deltas


def get_resolution_relativedelta(resolution: str, multiplier: int = 1) -> relativedelta:
    """
    Get the relative delta based on the resolution.

    Args:
        resolution (str): The resolution.
        multiplier (int, optional): The multiplier for the relative delta. Defaults to 1.

    Returns:
        relativedelta: The relative delta.
    """
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
    """
    Get the maximum number of points in a period.

    Args:
        period: The period element.
        nsmap: The namespace map.
        ns_name (str, optional): The namespace name. Defaults to "ns".

    Returns:
        int: The maximum number of points.
    """
    start, end = get_period_dates(period=period, nsmap=nsmap, ns_name=ns_name)
    resolution = get_period_resolution(period=period, nsmap=nsmap, ns_name=ns_name)
    rel_delta = get_resolution_relativedelta(resolution=resolution)
    number_of_points = interval_divided_by_delta(
        start_date=start, end_date=end, rel_delta=rel_delta
    )
    return number_of_points


def get_namespace_from_root(root, namespace_name: str = "ns"):
    """
    Get the namespace from the root element.

    Args:
        root: The root element.
        namespace_name (str, optional): The namespace name. Defaults to "ns".

    Returns:
        dict: The namespace.
    """
    nmsp = root.nsmap
    res = {}
    for key, value in nmsp.items():
        res[namespace_name] = value

    return res


def get_minutes_from_resolution(resolution: str) -> int:
    """
    Get the number of minutes from a resolution.

    Args:
        resolution (str): The resolution.

    Returns:
        int: The number of minutes.
    """
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
    """
    Get the MTU (Measurement Time Unit) from a date.

    Args:
        date (datetime): The date.
        calculate_only_mtu (bool, optional): Whether to calculate only the MTU. Defaults to False.
        prefix (str, optional): The prefix for the MTU elements. Defaults to "".

    Returns:
        str | dict: The MTU as a string or a dictionary of MTU elements.
    """
    mtu_elements = {}
    mtu = date
    mtu_elements[f"{prefix}mtu"] = mtu.strftime("%Y-%m-%dT%H:%MZ")

    mtu_elements[f"{prefix}year"] = mtu.year
    mtu_elements[f"{prefix}month"] = mtu.month
    mtu_elements[f"{prefix}day"] = mtu.day
    mtu_elements[f"{prefix}week"] = mtu.isocalendar()[1]
    mtu_elements[f"{prefix}hour"] = mtu.hour
    mtu_elements[f"{prefix}minute"] = mtu.minute

    if calculate_only_mtu:
        return mtu_elements[f"{prefix}mtu"]
    else:
        return mtu_elements


def get_time_data(
    date_start: datetime,
    date_end: datetime,
) -> dict:
    """
    Get the time data from start and end dates.

    Args:
        date_start (datetime): The start date.
        date_end (datetime): The end date.

    Returns:
        dict: The time data.
    """
    mtu_start = get_mtu(
        prefix="mtu.start.",
        date=date_start,
    )
    mtu_end = get_mtu(prefix="mtu.end.", date=date_end)

    mtu = {**mtu_start, **mtu_end}
    return mtu


def extract_code_from_key(dict_list: [dict], key: str) -> str:
    """
    Extract the code from a list of dictionaries based on a key.

    Args:
        dict_list ([dict]): The list of dictionaries.
        key (str): The key to search for.

    Returns:
        str: The code extracted from the dictionary.
    """
    for d in dict_list:
        if d["key"] == key:
            return d["code"]
    return ""
