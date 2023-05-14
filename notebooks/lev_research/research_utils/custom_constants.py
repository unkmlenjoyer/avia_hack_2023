from dataclasses import dataclass
from typing import Tuple


@dataclass
class CustomResearchConstants:
    PD_MAX_ROWS: int = 100
    PD_MAX_COLUMNS: int = 50
    PD_WIDTH: int = 50
    PD_MAX_COL_WIDTH: int = 50

    # seaborn settings constants
    SNS_STYLE: str = "darkgrid"
    SNS_FIG_SIZE: Tuple[int, int] = (60, 35)
