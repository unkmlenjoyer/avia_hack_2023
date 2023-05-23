import datetime
from itertools import zip_longest
from typing import Dict, Tuple, Union

import pytz
from airportsdata import Airport


def grouper(iterable: str, n: int, fillvalue: str = None) -> zip_longest:
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
    zip_longest
        Chunker
    """

    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def extract_airports(route: str) -> Tuple:
    """Extract airports values from search route

    Parameters
    ----------
    route : str
        Search route

    Returns
    -------
    res : Tuple[str, str, str, str]
        Splitted airports IATA codes.
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


def get_airport_info(
    target: str, air_storage: Dict[str, Union[Airport, Dict[str, str]]]
) -> Tuple[str, str]:
    """Extract airport data from storage

    Parameters
    ----------
    target : str
        IATA code for airport
    air_storage : Dict[str, Union[Airport, Dict[str, str]]]
        Data for 23.8k airports. If airport not
    Returns
    -------
    Tuple[str, str]
        Timezone and country code for specific airport
    """
    if target == "":
        return ("", "")
    tmp = air_storage.get(target, {"tz": "Europe/Moscow", "country": "RU"})
    return tmp["tz"], tmp["country"]


def convert_time_zones(
    date_local: datetime.datetime, local_tz: str, to_convert: str
) -> datetime.datetime:
    """Convertation local time with local tz to another time zone

    Parameters
    ----------
    date_local : datetime.datetime
        Local datetime to convert
    local_tz : str
        Local timezone in IANA format
    to_convert : str
        Result timezone in IANA format

    Returns
    -------
    converted_time : datetime.datetime
        Local datetime in result timezone
    """
    try:
        loc_tz = pytz.timezone(local_tz)
        convert_tz = pytz.timezone(to_convert)
        localmoment = loc_tz.localize(date_local, is_dst=None)
        converted_time = localmoment.astimezone(convert_tz).tz_localize(None)
        return converted_time
    except:
        print(date_local, local_tz, to_convert)
