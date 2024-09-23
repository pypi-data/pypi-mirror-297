from __future__ import annotations

import datetime
import typing

import polars as pl
import tooltime

from . import ui_types


ui_interval_to_df_interval = {
    'date': 'day',
    'week': 'week',
    'month': 'month',
}


time_increments = {
    'all': {
        'large': '365d',
        'medium': '30d',
        'small': '7d',
    },
    '365d': {
        'large': '365d',
        'medium': '30d',
        'small': '7d',
    },
    '30d': {
        'large': '30d',
        'medium': '7d',
        'small': '1d',
    },
    '7d': {
        'large': '7d',
        'medium': '1d',
        'small': '1d',
    },
}


def _get_date_range(df: pl.DataFrame) -> tuple[int, int]:
    return (
        tooltime.timestamp_to_seconds(
            typing.cast(datetime.datetime, df['timestamp'].min())
        ),
        tooltime.timestamp_to_seconds(
            typing.cast(datetime.datetime, df['timestamp'].max())
        ),
    )


def _increment_datetime(
    dt: datetime.datetime, duration: str
) -> datetime.datetime:
    if duration == '1d':
        return dt + datetime.timedelta(days=1)
    elif duration == '7d':
        return dt + datetime.timedelta(days=7)
    elif duration == '30d':
        if dt.month == 12:
            return dt.replace(month=1, year=dt.year + 1)
        else:
            return dt.replace(month=dt.month + 1)
    elif duration == '365d':
        return dt.replace(year=dt.year + 1)
    else:
        raise Exception('invalid increment')


def _decrement_datetime(
    dt: datetime.datetime, duration: str
) -> datetime.datetime:
    if duration == '1d':
        return dt - datetime.timedelta(days=1)
    elif duration == '7d':
        return dt - datetime.timedelta(days=7)
    elif duration == '30d':
        if dt.month == 1:
            return dt.replace(month=12, year=dt.year - 1)
        else:
            return dt.replace(month=dt.month - 1)
    elif duration == '365d':
        return dt.replace(year=dt.year - 1)
    else:
        raise Exception('invalid increment')


def _ensure_time_window_exceeds_sample_interval(
    values: dict[str, str], trigger: str, shortcut: ui_types.ShortcutSpec
) -> None:
    if values['time_window'] == '7d' and values['sample_interval'] == 'weekly':
        if trigger == 'time_window-radio':
            values['sample_interval'] = 'daily'
        elif trigger == 'sample_interval-radio':
            values['time_window'] = '30d'
        elif trigger == 'keyboard' and shortcut['field'] == 'sample_interval':
            values['time_window'] = '30d'
        else:
            values['sample_interval'] = 'daily'
    elif (
        values['time_window'] == '7d' and values['sample_interval'] == 'monthly'
    ):
        if trigger == 'time_window-radio':
            values['sample_interval'] = 'daily'
        elif trigger == 'sample_interval-radio':
            values['time_window'] = '365d'
        elif trigger == 'keyboard' and shortcut['field'] == 'sample_interval':
            values['time_window'] = '365d'
        else:
            values['sample_interval'] = 'daily'
    elif (
        values['time_window'] == '30d'
        and values['sample_interval'] == 'monthly'
    ):
        if trigger == 'time_window-radio':
            values['sample_interval'] = 'weekly'
        elif trigger == 'sample_interval-radio':
            values['time_window'] = '365d'
        elif trigger == 'keyboard' and shortcut['field'] == 'sample_interval':
            values['time_window'] = '365d'
        else:
            values['sample_interval'] = 'weekly'
