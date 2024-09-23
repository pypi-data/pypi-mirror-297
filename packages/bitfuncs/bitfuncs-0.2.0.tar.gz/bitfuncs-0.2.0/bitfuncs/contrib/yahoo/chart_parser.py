import logging
from collections import defaultdict

from .constants import ALLOWED_DAY_RESOLUTIONS, ALLOWED_MIN_RESOLUTIONS

logger = logging.getLogger(__name__)


def chart_to_values(chart, resolution="P1D"):
    if resolution not in (ALLOWED_DAY_RESOLUTIONS + ALLOWED_MIN_RESOLUTIONS):
        raise RuntimeError(f"Unsupported resolution: {resolution}")

    values_dict = defaultdict(dict)

    for _, row in chart.reset_index().iterrows():
        if resolution in ["1d", "5d"]:
            dt_str = row.Date.isoformat()
        else:
            dt_str = row.Datetime.isoformat()[:19]
        values_dict[dt_str] = {
            "time": dt_str,
            "o": row.Open,
            "h": row.High,
            "l": row.Low,
            "c": row.Close,
            "v": row.Volume,
        }

    return list(values_dict.values())
