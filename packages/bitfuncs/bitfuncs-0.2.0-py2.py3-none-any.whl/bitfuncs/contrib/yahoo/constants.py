ALLOWED_DAY_RESOLUTIONS = [f"{n}d" for n in (1, 5)]
ALLOWED_MIN_RESOLUTIONS = [f"{n}m" for n in (1, 2, 5, 15, 30, 60, 90)]

ALLOWED_PERIODS = ["1h", "1w"]
ALLOWED_PERIODS += [f"{n}mo" for n in (1, 3)]
ALLOWED_PERIODS += [f"{n}d" for n in (1, 5)]
ALLOWED_PERIODS += [f"{n}m" for n in (1, 2, 5, 15, 30, 60, 90)]

DT_FMT_SEC = "%Y-%m-%dT%H:%M:%S"

Y_RESOLUTIONS = {
    "P1D": "1d",
    "P7D": "5d",
    "PT1M": "1m",
    "PT2M": "2m",
    "PT5M": "5m",
    "PT15M": "15m",
    "PT30M": "30m",
    "PT60M": "60m",
}
