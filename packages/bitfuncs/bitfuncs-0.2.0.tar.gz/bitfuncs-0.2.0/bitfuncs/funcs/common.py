import json
import os
from datetime import datetime

import aiofiles

from ..constants import DT_FMT_SEC


async def dump(data, name="out", outdir="./var"):
    path = os.path.join(outdir, f"{name}.json")
    async with aiofiles.open(path, mode="w") as f:
        await f.write(json.dumps(data, indent=2))


def merge_values_w_ticker(values, ticker):
    """Just make sure that ticker is more recent than values"""
    if not values or not ticker:
        return values

    lvalue_dt = datetime.strptime(values[0]["time"], DT_FMT_SEC)
    ticker_dt = datetime.strptime(ticker["time"], DT_FMT_SEC)

    if lvalue_dt.date() < ticker_dt.date():
        values.insert(0, ticker)

    return values
