from itertools import zip_longest
from typing import Dict, Tuple

import pandas as pd
import pytz
from airportsdata import Airport


def grouper(iterable: str, n: int, fillvalue: str = None):
    """Collect data into fixed-length chunks or blocks

    Parameters
    ----------
    iterable : str
        Airports route
    n : int
        Length of chunk
    fillvalue : str, optional
        Value to fill empty, by default None

    Returns
    -------
    _type_
        _description_
    """

    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def extract_airports(route: str) -> Tuple:
    """Extract values from route

    Parameters
    ----------
    route : str
        Search route

    Returns
    -------
    res : Tuple[str, str, str, str]
        Splitted airports IATA codes
    """
    tmp = route.split("/")
    dep_forw, arr_forw = ("".join(group) for group in grouper(tmp[0], 3, fillvalue=""))

    if len(tmp) > 1:
        res = (
            dep_forw,
            arr_forw,
            *("".join(group) for group in grouper(tmp[1], 3, fillvalue="")),
        )
    else:
        res = (dep_forw, arr_forw, "", "")

    return res


def get_airport_info(target: str, air_storage: Dict[str, Airport]):
    """_summary_

    Parameters
    ----------
    target : str
        _description_
    air_storage : Dict[str, Airport]
        _description_
    extended_data : Dict[str, Dict[str, str]]
        _description_

    Returns
    -------
    _type_
        _description_
    """
    if target == "":
        return ("", "")

    tmp = {"tz": "", "country": ""}
    if target in air_storage:
        tmp = air_storage[target]

    return tmp["tz"], tmp["country"]


def convert_time_zones(date_local, local_tz, to_convert):
    """_summary_

    Parameters
    ----------
    date_local : _type_
        _description_
    local_tz : _type_
        _description_
    to_convert : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    loc_tz = pytz.timezone(local_tz)
    convert_tz = pytz.timezone(to_convert)
    try:
        localmoment = loc_tz.localize(date_local, is_dst=None)
        converted_time = localmoment.astimezone(convert_tz).tz_localize(None)
        return converted_time
    except:
        print("error", date_local, local_tz, to_convert)
