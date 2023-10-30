import pandas as pd
from datetime import datetime


def concat_and_save_dfs(
    dfs: list,
    file_name: str,
    suffix: str = "",
    timestamp: str = (datetime.now()).strftime("%Y%m%dT%H%M%S"),
):
    res = pd.concat(dfs, join="outer").fillna("na")
    timestamp = (datetime.now()).strftime("%Y%m%dT%H%M%S")
    res.to_csv(f"{file_name}-{suffix}-{timestamp}.csv", index=True, index_label="id")
    return True
