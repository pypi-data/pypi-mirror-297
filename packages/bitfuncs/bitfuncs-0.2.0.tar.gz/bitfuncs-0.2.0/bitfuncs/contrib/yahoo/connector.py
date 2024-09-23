import logging
from datetime import datetime

import yfinance as yf
from chamallow import flow

from .chart_parser import chart_to_values
from .constants import Y_RESOLUTIONS

logger = logging.getLogger(__name__)


def get_ticker_date(symbol):
    pass


@flow()
async def get_ticker(symbol):
    data = yf.download(
        symbol,
        period="1d",
        interval="1m",
    )

    values = chart_to_values(
        data,
        resolution="1m",
    )

    return values[-1]


@flow()
async def get_values(symbol, last_date=None, resolution="P1D"):
    if resolution in Y_RESOLUTIONS:
        resolution = Y_RESOLUTIONS[resolution]
    else:
        raise RuntimeError(f"Unsupported resolution: {resolution}")

    if last_date:
        period = None

        if isinstance(last_date, datetime):
            last_date = last_date.isoformat()

        if isinstance(last_date, str):
            if resolution in ["1d", "5d"]:
                last_date = last_date[:10]
            else:
                last_date = last_date[:19]

    else:
        last_date = None

        if resolution in ["1d", "5d"]:
            period = "6mo"
        else:
            period = "1wk"

    data = yf.download(symbol, period=period, interval=resolution, start=last_date)

    return chart_to_values(data, resolution=resolution)
