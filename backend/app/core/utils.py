import datetime
import typing

import sqlalchemy as sa

from app.core.config import settings

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo  # type: ignore


def get_current_timezone() -> zoneinfo.ZoneInfo:
    """Get the project's timezone as defined in settings.TIMEZONE default to 'UTC'"""
    tzname = settings.TIMEZONE or "UTC"
    if isinstance(tzname, datetime.timezone):
        tzname = str(tzname)
    return zoneinfo.ZoneInfo(tzname)


def now() -> datetime.datetime:
    """Get the current datetime"""
    return datetime.datetime.now(get_current_timezone())


def build_conditions(
    filters: typing.Mapping[str, typing.Any],
    model: type,
    in_for_iterable: bool = False,
) -> typing.List[sa.BinaryExpression[typing.Any]]:
    conditions: typing.List[sa.BinaryExpression[typing.Any]] = []
    if not filters:
        return conditions

    for key, value in filters.items():
        if not hasattr(model, key):
            continue
        column = getattr(model, key)
        if in_for_iterable and isinstance(value, (list, tuple, set)):
            conditions.append(column.in_(value))
        elif isinstance(value, bool):
            conditions.append(column.is_(value))
        else:
            conditions.append(column == value)
    return conditions
