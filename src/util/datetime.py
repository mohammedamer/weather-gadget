def _is_leap(y: int) -> bool:
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)


_DAYS_BEFORE_MONTH = (
    (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334),  # non-leap
    (0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335),  # leap
)


def iso_to_unix_seconds(s: str) -> int:
    # expects "YYYY-MM-DDTHH:MM"
    y = int(s[0:4])
    m = int(s[5:7])
    d = int(s[8:10])
    hh = int(s[11:13])
    mm = int(s[14:16])

    leap = 1 if _is_leap(y) else 0

    # days since 1970-01-01
    days = 0
    for yy in range(1970, y):
        days += 366 if _is_leap(yy) else 365

    days += _DAYS_BEFORE_MONTH[leap][m - 1]
    days += (d - 1)

    return days * 86400 + hh * 3600 + mm * 60


def diff_seconds(t1: str, t2: str) -> int:
    return iso_to_unix_seconds(t2) - iso_to_unix_seconds(t1)


def argmin_time(target: str, times: list[str]) -> int:

    diff = [abs(diff_seconds(target, t)) for t in times]

    argmin = None
    min_diff = float("inf")

    for idx, d in enumerate(diff):
        if d < min_diff:
            min_diff = d
            argmin = idx

    return argmin
