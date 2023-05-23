from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ServiceConfig:
    """Class with configuration / extended data

    path_model_one_way : str
        Path to one way model file

    path_model_one_way : str
        Path to two way model file

    cols_model_one_way : List[str]
        Columns of data to the first model (one way)

    cols_model_two_way : List[str]
        Columns of data to the second model (two way)

    extended_air_data: Dict[str, Dict[str, str]]
        Extended airports data
    """

    path_model_one_way: str = "src/models/model_one_way"
    path_model_two_way: str = "src/models/model_two_way"
    cols_model_one_way: List[str] = field(
        default_factory=lambda: [
            "TravellerGrade",
            "SegmentCount",
            "Amount",
            "class",
            "IsBaggage",
            "isRefundPermitted",
            "isExchangePermitted",
            "isDiscount",
            "InTravelPolicy",
            "forw_hours",
            "forw_hours_diff_min",
            "forw_hours_diff_mean",
            "req_dep_hours_diff",
            "price_diff_min_perc",
            "price_diff_mean_perc",
            "is_direct",
        ]
    )
    cols_model_two_way: List[str] = field(
        default_factory=lambda: [
            "TravellerGrade",
            "SegmentCount",
            "Amount",
            "class",
            "IsBaggage",
            "isRefundPermitted",
            "isExchangePermitted",
            "isDiscount",
            "InTravelPolicy",
            "forw_hours",
            "back_hours",
            "total_hours",
            "forw_hours_diff_min",
            "forw_hours_diff_mean",
            "back_hours_diff_min",
            "back_hours_diff_mean",
            "req_dep_hours_diff",
            "req_ret_hours_diff",
            "price_diff_min_perc",
            "price_diff_mean_perc",
            "is_direct",
        ]
    )
    extended_air_data: Dict[str, Dict[str, str]] = field(
        default_factory=lambda: {
            "BAK": {"country": "AZ", "tz": "Asia/Baku"},
            "BJS": {"country": "CN", "tz": "Asia/Shanghai"},
            "BUE": {"country": "AR", "tz": "America/Argentina/Buenos_Aires"},
            "BUH": {"country": "RO", "tz": "Europe/Bucharest"},
            "CHI": {"country": "US", "tz": "America/Chicago"},
            "EYK": {"country": "RU", "tz": "Asia/Yekaterinburg"},
            "ITU": {"country": "RU", "tz": "Asia/Tokyo"},
            "IZM": {"country": "TR", "tz": "Turkey"},
            "JKT": {"country": "ID", "tz": "Asia/Jakarta"},
            "KCK": {"country": "RU", "tz": "Asia/Irkutsk"},
            "KLF": {"country": "RU", "tz": "Europe/Moscow"},
            "KPW": {"country": "RU", "tz": "Asia/Anadyr"},
            "LON": {"country": "GB", "tz": "Europe/London"},
            "MIL": {"country": "IT", "tz": "Europe/Rome"},
            "MOW": {"country": "RU", "tz": "Europe/Moscow"},
            "NER": {"country": "RU", "tz": "Asia/Yakutsk"},
            "NYC": {"country": "US", "tz": "America/New_York"},
            "PAR": {"country": "FR", "tz": "Europe/Paris"},
            "RIO": {"country": "BR", "tz": "America/Sao_Paulo"},
            "RMZ": {"country": "RU", "tz": "Asia/Yekaterinburg"},
            "ROM": {"country": "IT", "tz": "Europe/Rome"},
            "SEL": {"country": "KR", "tz": "Asia/Seoul"},
            "STO": {"country": "SE", "tz": "Europe/Stockholm"},
            "TYO": {"country": "JP", "tz": "Asia/Tokyo"},
            "WAS": {"country": "US", "tz": "America/New_York"},
            "XDB": {"country": "FR", "tz": "Europe/Paris"},
            "YMQ": {"country": "CA", "tz": "America/Toronto"},
            "YTO": {"country": "CA", "tz": "America/Toronto"},
            "БОЧ": {"country": "RU", "tz": "Asia/Krasnoyarsk"},
            "НЖГ": {"country": "RU", "tz": "Asia/Irkutsk"},
            "СЕН": {"country": "RU", "tz": "Asia/Krasnoyarsk"},
            "ЧАР": {"country": "RU", "tz": "Asia/Chita"},
        }
    )
