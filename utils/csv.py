import pandas as pd
from datetime import datetime


def concat_and_save_dfs(
    dfs: list,
    file_name: str,
    suffix: str = "",
    timestamp: str = (datetime.now()).strftime("%Y%m%dT%H%M%S"),
) -> str:
    res = pd.concat(dfs, join="outer").fillna("na")
    timestamp = (datetime.now()).strftime("%Y%m%dT%H%M%S")
    file_saving_name = f"{file_name}-{suffix}-{timestamp}.csv"
    res.to_csv(file_saving_name, index=True, index_label="id")
    return file_saving_name
