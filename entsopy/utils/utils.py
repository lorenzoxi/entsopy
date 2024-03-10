from datetime import datetime, timedelta
import sys
from dateutil.relativedelta import relativedelta, SU
from entsopy.utils.date import count_weeks, number_weeks_year, get_week, get_week_boundrais


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

    if period == None:
        print("Period is None")

    start = period.findtext(f".//{ns_name}:start", namespaces=nsmap)
    end = period.findtext(f".//{ns_name}:end", namespaces=nsmap)

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
    start_date: datetime, end_date: datetime, resolution: str
):
    current_time = start_date
    number_of_deltas = 0

    if resolution == "P7D":
        return count_weeks(start_date, end_date)

    while current_time < end_date:
        current_time = current_time + get_resolution_relativedelta(
            resolution=resolution, multiplier=1, date=current_time
        )
        number_of_deltas += 1

    return number_of_deltas


def get_resolution_relativedelta(
    resolution: str, multiplier: int = 0, date: datetime = None
) -> relativedelta | int:
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
        rel_delta = date.isocalendar()[1]
    elif resolution == "P1D":
        rel_delta = relativedelta(days=(1 * multiplier))
    elif resolution == "PT60M":
        rel_delta = relativedelta(minutes=(60 * (multiplier)))
    elif resolution == "PT30M":
        rel_delta = relativedelta(minutes=(30 * multiplier))
    elif resolution == "PT15M":
        rel_delta = relativedelta(minutes=(15 * multiplier))
    return rel_delta


def max_number_of_points(period, resolution, nsmap, ns_name: str = "ns"):
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
    number_of_points = interval_divided_by_delta(
        start_date=start, end_date=end, resolution=resolution
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
    # stringify mtu
    mtu = date
    mtu_elements[f"mtu.{prefix}mtu"] = mtu.strftime("%Y-%m-%dT%H:%MZ")

    mtu_elements[f"mtu.{prefix}year"] = f"{mtu.year}"
    mtu_elements[f"mtu.{prefix}month"] = f"{mtu.month:02d}"
    mtu_elements[f"mtu.{prefix}day"] = f"{mtu.day:02d}"
    mtu_elements[f"mtu.{prefix}week"] = mtu.isocalendar()[1]
    mtu_elements[f"mtu.{prefix}hour"] = f"{mtu.hour:02d}"
    mtu_elements[f"mtu.{prefix}minute"] = f"{mtu.minute:02d}"

    if calculate_only_mtu:
        return mtu_elements[f"{prefix}mtu"]
    else:
        return mtu_elements


def get_time_data(
    date_start: datetime,
    date_end: datetime,
    position: int,
    resolution: str,
    time_type: str = ""
) -> dict:
    """
    Get the time data from start and end dates.

    Args:
        date_start (datetime): The start date.
        date_end (datetime): The end date.

    Returns:
        dict: The time data.
    """
    
    if resolution == "P1D":
        #retrieve week number of the end_date date
        week_number = date_end.isocalendar()[1]
        #get the i-th day of the week
        day = ith_day_of_iso_week(date_end.year, week_number, position)
        start = datetime(day.year, day.month, day.day, 0, 0, 0)
        end = datetime(day.year, day.month, day.day, 23, 0, 0)
        mtu_start = get_mtu(prefix="start", date=start)
        mtu_end = get_mtu(prefix="end", date=end)
    
    elif resolution == "P7D":
        
        # go the the first day of the next year of the start date if the start date is not the first day of the year
        if(date_start.month == 12 and time_type == "yyyy"):
            date_start = date_start + relativedelta(years=1, month=1, day=1)
        
        day_start, day_end = get_week_boundrais(date_start, position, time_type=time_type)
                        
        mtu_start = get_mtu(prefix="start", date=day_start) 
        mtu_end = get_mtu(prefix="end", date=day_end)
        
    elif resolution == "P1Y":
        if(date_start.month == 12):
            date_start = date_start + relativedelta(years=1, month=1, day=1)
        
        date_start = datetime(date_start.year, 1, 1, 0, 0, 0)
        date_end = datetime(date_start.year, 12, 31, 23, 0, 0)
        mtu_start = get_mtu(prefix="start", date=date_start)
        mtu_end = get_mtu(prefix="end", date=date_end)
        
    elif resolution == "PT60M":
        date_end = date_start + relativedelta(minutes=(60 * (position+1)))
        date_start = date_start + relativedelta(minutes=(60 * (position)))

        
        mtu_start = get_mtu(prefix="start", date=date_start)
        mtu_end = get_mtu(prefix="end", date=date_end)
        
    else:
        mtu_start = get_mtu(
            prefix="start",
            date=(
                date_start
                + get_resolution_relativedelta(
                    resolution=resolution, multiplier=(position - 1), date=date_start
                )
            ),
        )
        mtu_end = get_mtu(
            prefix="end",
            date=(
                date_end
                + get_resolution_relativedelta(
                    resolution=resolution, multiplier=position, date=date_end
                )
            ),
        )

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


def extract_elements_from_node(node, to_exclude=[], prefix="doc"):
    tags_to_exclude = to_exclude
    data = {}
    if node.getchildren() == []:
        key = prefix + "." + sanitize_from_urn(node.tag)
        data[key] = node.text
    else:
        for child in node.xpath(".//*"):
            tag = sanitize_from_urn(child.tag).strip()
            parent_tag = ""
            grandparent_tag = ""

            parent = child.getparent()
            grandparent = parent.getparent() if parent != None else None

            if parent is not None:
                parent_tag = sanitize_from_urn(parent.tag).strip()

            if parent is not None and grandparent is not None:
                grandparent_tag = sanitize_from_urn(grandparent.tag).strip()

            if (
                tag not in tags_to_exclude
                and parent_tag not in tags_to_exclude
                and grandparent_tag not in tags_to_exclude
            ):
                if child.getchildren() == []:
                    key = prefix + "." + parent_tag + "." + tag
                    data[key] = child.text
            else:
                pass
    return data


def is_debug_active() -> bool:
    """Return if the debugger is currently active"""
    return hasattr(sys, "gettrace") and sys.gettrace() is not None

def get_time_interval(start_date: str, time_type: str) -> str :
    time_interval = ""
    if time_type == "yyyy":
        year = int(start_date)
        # get the first day of the first week of the year
        first_day = first_day_of_first_week_of_year(int(year))
        start_interval = f"{year}-01-{first_day:02d}T00:00:00Z"
        last_day = last_day_of_last_week_of_year(int(year))
        end_interval = f"{year}-12-{last_day:02d}T23:00:00Z"
        
    elif time_type == "yyyy-mm":
        date = start_date
        lower_bound = datetime.strptime(date[0], "%Y-%m")
        upper_bound = datetime.strptime(date[1], "%Y-%m")
        
        year = lower_bound.year
        month = lower_bound.month
        first_day = first_day_of_first_week_of_month(year, month)
        start_interval = f"{year}-{month:02d}-{first_day:02d}T00:00:00Z"
        
        year = upper_bound.year
        month = upper_bound.month
        end_interval = last_day_of_last_week_of_month(year, month)
        end_interval = f"{year}-{month:02d}-{end_interval:02d}T23:00:00Z"
        
    elif time_type == "yyyy-W":
        date = start_date
        lower_bound = datetime.strptime(date[0], "%Y-W%W")
        upper_bound = datetime.strptime(date[1], "%Y-W%W")
        
        year = lower_bound.year
        week = lower_bound.isocalendar()[1]
        start_interval = first_day_of_week(year, week)
        month = start_interval.month
        day = start_interval.day
        start_interval = f"{year}-{month:02d}-{day:02d}T00:00:00Z"
        
        month = upper_bound.month
        end_interval = last_day_of_week(year, week)
        day = end_interval.day
        end_interval = f"{year}-{month:02d}-{day:02d}T23:00:00Z"
        
        
    time_interval = f"{start_interval}/{end_interval}"
    return time_interval

def first_day_of_week(year, week):
    jan_1 = datetime(year, 1, 1)
    jan_1_weekday = jan_1.weekday()
    delta_days = 7 - jan_1_weekday if jan_1_weekday > 0 else 0
    first_monday = jan_1 + timedelta(days=delta_days)
    first_day_of_week = first_monday + timedelta(weeks=week - 1)
    return first_day_of_week

def last_day_of_week(year, week):
    jan_1 = datetime(year, 1, 1)
    jan_1_weekday = jan_1.weekday()
    delta_days = 7 - jan_1_weekday if jan_1_weekday > 0 else 0
    first_monday = jan_1 + timedelta(days=delta_days)
    first_day_of_week = first_monday + timedelta(weeks=week - 1)
    last_day_of_week = first_day_of_week + timedelta(days=6)

    return last_day_of_week

def first_day_of_first_week_of_month(year, month):
    first_day = datetime(year, month, 1)
    days_to_add = (7 - first_day.weekday()) % 7
    first_monday = (first_day + timedelta(days=days_to_add))
    return first_monday

def last_day_of_last_week_of_month(year, month):
    if month == 12:
        next_month_first_day = datetime(year + 1, 1, 1)
    else:
        next_month_first_day = datetime(year, month + 1, 1)

    days_to_subtract = next_month_first_day.weekday() + 1

    last_sunday = (next_month_first_day - timedelta(days=days_to_subtract))
    return last_sunday


def first_day_of_first_week_of_year(year):
    jan_4 = datetime(year, 1, 4)
    day_of_week = jan_4.weekday()
    first_day_of_week = (jan_4 - timedelta(days=day_of_week))
    return first_day_of_week

def last_day_of_last_week_of_year(year):
    dec_31 = datetime(year, 12, 31)
    day_of_week = dec_31.weekday()
    days_to_last_thursday = (day_of_week - 3) % 7
    last_thursday = dec_31 - timedelta(days=days_to_last_thursday)
    last_day_of_last_week = (last_thursday + timedelta(days=3))

    return last_day_of_last_week


def ith_day_of_iso_week(year, week, i):
    jan_1 = datetime(year, 1, 1)
    jan_1_weekday = jan_1.weekday()
    delta_days = 7 - jan_1_weekday if jan_1_weekday > 0 else 0
    first_monday = jan_1 + timedelta(days=delta_days)
    first_day_of_week = first_monday + timedelta(weeks=week - 1)
    ith_day = first_day_of_week + timedelta(days=i - 1)
    return ith_day

def last_day_of_month(year, month):
    if month == 12:
        next_month_first_day = datetime(year + 1, 1, 1)
    else:
        next_month_first_day = datetime(year, month + 1, 1)

    days_to_subtract = next_month_first_day.weekday() + 1
    last_day = (next_month_first_day - timedelta(days=days_to_subtract))
    return last_day
    
def split_in_intervals_load(start_date:str, end_date:str, time_type:str):
    intervals = []

    if (time_type == "yyyy"):
        start_year = datetime.strptime(start_date, "%Y").year
        end_year = datetime.strptime(end_date, "%Y").year
        years = [str(start_year + i) for i in range(end_year - start_year + 1)]
        for i in range(len(years)):
            date = first_day_of_first_week_of_year(int(years[i]))
            
            day = date.day
            month = date.month
            year = date.year
            start_date = f"{year}-{month:02d}-{day:02d}T00:00:00Z"
            last_day = last_day_of_last_week_of_year(int(years[i]))
            day = last_day.day
            month = last_day.month
            year = last_day.year
            end_date = f"{year}-{month:02d}-{day:02d}T23:00:00Z"
            intervals.append((start_date, end_date))
    
    elif (time_type == "yyyy-mm"):
        start_date = datetime.strptime(start_date, "%Y-%m")
        end_date = datetime.strptime(end_date, "%Y-%m")
        
        current_date = start_date
        end_date = end_date
        current_year = start_date.year
        
        while current_date <= end_date:
            # Add the first month of the current year
            first = (current_date.strftime('%Y-%m'))

            # Add the last month of the current year
            last_month_date = datetime(current_year, 12, 1)
            if last_month_date <= end_date:
                last = (last_month_date.strftime('%Y-%m'))
            else:
                last = (end_date.strftime('%Y-%m'))
                
            intervals.append((first, last))

            # Move to the next year
            current_year += 1
            current_date = datetime(current_year, 1, 1)
            
        new_intervals = []
        for interval in intervals:
            date = interval
            lower_bound = datetime.strptime(date[0], "%Y-%m")
            upper_bound = datetime.strptime(date[1], "%Y-%m")
            
            year = lower_bound.year
            month = lower_bound.month
            first_day = first_day_of_first_week_of_month(year, month)
            
            year = first_day.year
            month = first_day.month
            day = first_day.day
            
            start_interval = f"{year}-{month:02d}-{day:02d}T00:00:00Z"
            
            year = upper_bound.year
            month = upper_bound.month
            last_day = last_day_of_last_week_of_month(year, month)
            year = last_day.year
            month = last_day.month
            day = last_day.day
            
            end_interval = f"{year}-{month:02d}-{day:02d}T23:00:00Z"
            new_intervals.append((start_interval, end_interval))
        
        intervals = new_intervals
            
    elif (time_type == "yyyy-W"):
        
        start = start_date.split("-")
        start_year = start[0]
        start_week = start[1]

        end = end_date.split("-")
        end_year = int(end[0])
        end_week = int(end[1])
        
        current_year = int(start_year)
        intervals = []
        while(current_year <= end_year):
            tmp_start = ""
            tmp_end = ""
            if(current_year == int(start_year)):
                tmp_start = start_week
            else:
                tmp_start = "01"
            if(current_year == end_year):
                tmp_end = end_week
            else:
                tmp_end = number_weeks_year(current_year)
                
            intervals.append((f"{current_year}-{tmp_start}", f"{current_year}-{tmp_end}"))
            
            current_year += 1
                    
        new_intervals = []
        for interval in intervals:            
            date = interval[0].split("-")
            
            year_start = int(date[0])
            week_start = int(date[1])
            
            start_interval = first_day_of_week(year_start, week_start)
            year = start_interval.year
            month = start_interval.month
            day = start_interval.day
            start_interval = f"{year}-{month:02d}-{day:02d}T00:00:00Z"
            
            date = interval[1].split("-")
            year_end = int(date[0])
            week_end = int(date[1])
            
            end_interval = last_day_of_week(year_end, week_end)
            year = end_interval.year
            month = end_interval.month
            day = end_interval.day
            end_interval = f"{year}-{month:02d}-{day:02d}T23:00:00Z"
            new_intervals.append((start_interval, end_interval))
        intervals = new_intervals
            
    elif (time_type == "yyyy-mm-dd"):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        start_year = int(start_date.year)
        current_year = start_year
        end_year = int(end_date.year)

        current_date = start_date
        while(current_year <= end_year):
            tmp_start = ""
            tmp_end = ""
            if(current_year == int(start_year)):
                #calculate the day before start_date
                start_date = start_date - timedelta(days=1)
                tmp_start = start_date.strftime("%Y-%m-%dT23:00:00Z")
            else:
                tmp_date = f"{current_year}-01-01"
                tmp_date = datetime.strptime(tmp_date, "%Y-%m-%d")
                tmp_date = tmp_date - timedelta(days=1)
                tmp_start = tmp_date.strftime("%Y-%m-%dT23:00:00Z")
            if(current_year == end_year):
                tmp_end = end_date.strftime("%Y-%m-%dT23:00:00Z")
            else:
                tmp_end = f"{current_year}-12-31T23:00:00Z"
                
            intervals.append((f"{tmp_start}", f"{tmp_end}"))
            
            current_year += 1
            
        
    return intervals


def day_before_first_day_of_the_year(year):
    date = f"{year}-01-01"
    date = datetime.strptime(date, "%Y-%m-%d")
    date = date - timedelta(days=1)
    return date

def last_day_of_the_year(year):
    date = f"{year}-12-31"
    date = datetime.strptime(date, "%Y-%m-%d")
    return date

def split_in_intervals_generation(start_date:str, end_date:str, time_type:str, start_with_week:bool = False):
    intervals = []

    if (time_type == "yyyy"):
        
        start_year = datetime.strptime(start_date, "%Y").year
        end_year = datetime.strptime(end_date, "%Y").year
        years = [str(start_year + i) for i in range(end_year - start_year + 1)]
        for i in range(len(years)):
            if (start_with_week == False):
                tmp_start = day_before_first_day_of_the_year(int(years[i]))
                tmp_start = tmp_start.strftime("%Y-%m-%dT23:00:00Z")
                tmp_end = last_day_of_the_year(int(years[i]))
                tmp_end = tmp_end.strftime("%Y-%m-%dT23:00:00Z")
                intervals.append((f"{tmp_start}", f"{tmp_end}"))
            else:
                tmp_start = first_day_of_first_week_of_year(int(years[i]))
                tmp_start = tmp_start.strftime("%Y-%m-%dT00:00:00Z")
                tmp_end = last_day_of_last_week_of_year(int(years[i]))
                tmp_end = tmp_end.strftime("%Y-%m-%dT23:00:00Z")
                intervals.append((f"{tmp_start}", f"{tmp_end}"))
    
    elif (time_type == "yyyy-mm-dd"):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        start_year = int(start_date.year)
        current_year = start_year
        end_year = int(end_date.year)

        current_date = start_date
        while(current_year <= end_year):
            tmp_start = ""
            tmp_end = ""
            if(current_year == int(start_year)):
                #calculate the day before start_date
                start_date = start_date - timedelta(days=1)
                tmp_start = start_date.strftime("%Y-%m-%dT23:00:00Z")
            else:
                tmp_date = f"{current_year}-01-01"
                tmp_date = datetime.strptime(tmp_date, "%Y-%m-%d")
                tmp_date = tmp_date - timedelta(days=1)
                tmp_start = tmp_date.strftime("%Y-%m-%dT23:00:00Z")
            if(current_year == end_year):
                tmp_end = end_date.strftime("%Y-%m-%dT23:00:00Z")
            else:
                tmp_end = f"{current_year}-12-31T23:00:00Z"
                
            intervals.append((f"{tmp_start}", f"{tmp_end}"))
            
            current_year += 1
    
        
    return intervals


def split_to_intervals(start_date:str, end_date:str, time_type:str, request_week_based:bool = False):
    intervals = []
    
    if (time_type == "yyyy"):
        start_year = datetime.strptime(start_date, "%Y").year
        end_year = datetime.strptime(end_date, "%Y").year
        years = [str(start_year + i) for i in range(end_year - start_year + 1)]
        for i in range(len(years)):
            
            tmp_start_date = None
            tmp_end_date = None
            
            if(request_week_based):
                tmp_start_date = first_day_of_first_week_of_year(int(years[i]))
                tmp_end_date = last_day_of_last_week_of_year(int(years[i]))
            else:
                tmp_start_date = datetime(int(years[i]), 1, 1)
                tmp_end_date = datetime(int(years[i]), 12, 31)
            
            s_day = tmp_start_date.day
            s_month = tmp_start_date.month
            s_year = tmp_start_date.year
            start_date = f"{s_year}-{s_month:02d}-{s_day:02d}T00:00:00Z"

            e_day = tmp_end_date.day
            e_month = tmp_end_date.month
            e_year = tmp_end_date.year
            end_date = f"{e_year}-{e_month:02d}-{e_day:02d}T23:00:00Z"
            intervals.append((start_date, end_date))
    
    elif (time_type == "yyyy-mm"):
        start_date = datetime.strptime(start_date, "%Y-%m")
        end_date = datetime.strptime(end_date, "%Y-%m")
        
        current_date = start_date
        end_date = end_date
        current_year = start_date.year
        
        #calculate intervals
        while current_date <= end_date:
            first = (current_date.strftime('%Y-%m'))

            last_month_date = datetime(current_year, 12, 1)
            if last_month_date <= end_date:
                last = (last_month_date.strftime('%Y-%m'))
            else:
                last = (end_date.strftime('%Y-%m'))
                
            intervals.append((first, last))

            current_year += 1
            current_date = datetime(current_year, 1, 1)
            
        #refine intervals
        new_intervals = []
        for interval in intervals:
            date = interval
            lower_bound = datetime.strptime(date[0], "%Y-%m")
            upper_bound = datetime.strptime(date[1], "%Y-%m")
            
            tmp_start_date = None
            tmp_end_date = None
            
            if(request_week_based):
                tmp_start_date = first_day_of_first_week_of_month(lower_bound.year, lower_bound.month)
                tmp_end_date = last_day_of_last_week_of_month(upper_bound.year, upper_bound.month)
            else:
                tmp_start_date = datetime(lower_bound.year, lower_bound.month, 1)
                tmp_end_date = datetime(upper_bound.year, upper_bound.month, last_day_of_month(upper_bound.year, upper_bound.month))    
            
            s_day = tmp_start_date.day
            s_month = tmp_start_date.month
            s_year = tmp_start_date.year
            start_date = f"{s_year}-{s_month:02d}-{s_day:02d}T00:00:00Z"

            e_day = tmp_end_date.day
            e_month = tmp_end_date.month
            e_year = tmp_end_date.year
            end_date = f"{e_year}-{e_month:02d}-{e_day:02d}T23:00:00Z"
            
            new_intervals.append((start_date, end_date))
        
        intervals = new_intervals
            
    elif (time_type == "yyyy-W"):
        
        start = start_date.split("-")
        start_year = start[0]
        start_week = start[1]

        end = end_date.split("-")
        end_year = int(end[0])
        end_week = int(end[1])
        
        current_year = int(start_year)
        intervals = []
        
        #calculate intervals
        while(current_year <= end_year):
            tmp_start = ""
            tmp_end = ""
            if(current_year == int(start_year)):
                tmp_start = start_week
            else:
                tmp_start = "01"
            if(current_year == end_year):
                tmp_end = end_week
            else:
                tmp_end = number_weeks_year(current_year)
                
            intervals.append((f"{current_year}-{tmp_start}", f"{current_year}-{tmp_end}"))
            
            current_year += 1
        
        #refine intervals
        new_intervals = []
        for interval in intervals:            
            date = interval[0].split("-")
            
            year_start = int(date[0])
            week_start = int(date[1])
            
            if(request_week_based == True):
                start_interval = first_day_of_week(year_start, week_start)
                year = start_interval.year
                month = start_interval.month
                day = start_interval.day
                start_interval = f"{year}-{month:02d}-{day:02d}T00:00:00Z"
                
                date = interval[1].split("-")
                year_end = int(date[0])
                week_end = int(date[1])
                
                end_interval = last_day_of_week(year_end, week_end)
                year = end_interval.year
                month = end_interval.month
                day = end_interval.day
                end_interval = f"{year}-{month:02d}-{day:02d}T23:00:00Z"
                new_intervals.append((start_interval, end_interval))

        intervals = new_intervals
            
    elif (time_type == "yyyy-mm-dd"):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        start_year = int(start_date.year)
        current_year = start_year
        end_year = int(end_date.year)

        current_date = start_date
        while(current_year <= end_year):
            tmp_start = None
            tmp_end = None
            
            if(request_week_based == False):
                if(current_year == int(start_year)):
                    #calculate the day before start_date
                    start_date = start_date - timedelta(days=1)
                    tmp_start = start_date.strftime("%Y-%m-%dT23:00:00Z")
                else:
                    tmp_date = f"{current_year}-01-01"
                    tmp_date = datetime.strptime(tmp_date, "%Y-%m-%d")
                    tmp_date = tmp_date - timedelta(days=1)
                    tmp_start = tmp_date.strftime("%Y-%m-%dT23:00:00Z")
                if(current_year == end_year):
                    tmp_end = end_date.strftime("%Y-%m-%dT23:00:00Z")
                else:
                    tmp_end = f"{current_year}-12-31T23:00:00Z"
                
            intervals.append((f"{tmp_start}", f"{tmp_end}"))
            
            current_year += 1
            
        
    return intervals

