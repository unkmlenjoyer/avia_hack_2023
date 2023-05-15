from dataclasses import dataclass
from typing import Tuple


@dataclass
class CustomResearchConstants:
    """Custom constant storage

    PD_MAX_ROWS : int
        Amount of max visible rows in pd.DataFrame, by default 100

    PD_MAX_COLUMNS : int
        Amount of max visible columns in pd.DataFrame, by default 50

    PD_WIDTH : int
        Pandas max width

    PD_MAX_COL_WIDTH : int
        Pandas max column width

    SNS_STYLE : str
        Style for seaborn

    SNS_FIG_SIZE : Tuple[int, int]
        Size for figure
    """

    PD_MAX_ROWS: int = 100
    PD_MAX_COLUMNS: int = 50
    PD_WIDTH: int = 50
    PD_MAX_COL_WIDTH: int = 50

    # seaborn settings constants
    SNS_STYLE: str = "darkgrid"
    SNS_FIG_SIZE: Tuple[int, int] = (60, 35)
