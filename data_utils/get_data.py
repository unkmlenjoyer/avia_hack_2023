# %%
import pathlib
from dataclasses import dataclass, field
from typing import Dict

import pandas as pd


# %%
@dataclass
class LoadConstants:
    """Class of dowloading data constants

    SAVE_FOLDER : pathlib.Path
        Save path-object with predefined folder path

    GOOGLE_DRIVE_PREFIX : str
        String for configure load link from shared link

    LINK_DATA_SOURCE : Dict
        Dict with file name and shared links to google drive
    """

    SAVE_FOLDER: pathlib.Path = pathlib.Path("../data/raw_data")
    GOOGLE_DRIVE_PREFIX: str = "https://drive.google.com/uc?id="
    LINK_DATA_SOURCE: Dict = field(
        default_factory=lambda: {
            "DescriptionAgent": "https://docs.google.com/spreadsheets/d/1SqKcg46aYfpO0MfTkBYQUV2v5gsVqB08/edit?usp=share_link&ouid=103743120778575003333&rtpof=true&sd=true",
            "DescriptionClient": "https://docs.google.com/spreadsheets/d/1P1eAJq7HzSvMAwuacWTUokjw3BPO4Itj/edit?usp=share_link&ouid=103743120778575003333&rtpof=true&sd=true",
            "RequestAgent": "https://docs.google.com/spreadsheets/d/1C4p1CLZ9zoh8SpZg2mtjS-lj4mZk-gBy/edit?usp=share_link&ouid=103743120778575003333&rtpof=true&sd=true",
            "RequestClient": "https://docs.google.com/spreadsheets/d/1z_993H_XLUgJ1M87QpOL8OW8kito3iWO/edit?usp=share_link&ouid=103743120778575003333&rtpof=true&sd=true",
        }
    )


# %%
load_const = LoadConstants()

# create folder if it not created
if not load_const.SAVE_FOLDER.is_dir():
    load_const.SAVE_FOLDER.mkdir()

# %%
n_files = len(load_const.LINK_DATA_SOURCE)
for i, file in enumerate(load_const.LINK_DATA_SOURCE, start=1):
    print(f"{i} / {n_files}: file `{file}` dowloading...")

    # reconfigure link
    file_url = (
        load_const.GOOGLE_DRIVE_PREFIX
        + load_const.LINK_DATA_SOURCE[file].split("/")[-2]
    )

    # configure save path
    save_path = load_const.SAVE_FOLDER / (file + ".xlsx")

    # load and save
    pd.read_excel(file_url).to_excel(save_path)

    print(f"{i} / {n_files}: File `{file}` downloaded and saved to {save_path}")
