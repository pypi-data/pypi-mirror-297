from __future__ import annotations

import typing

import tooltime
import polars as pl
import plotly.graph_objects as go  # type: ignore

from ... import plotly
from .. import state as state_module
from .. import ui_types
from .. import timestamps


def create_tree_fig(
    df: pl.DataFrame,
    state: dict[str, typing.Any],
    ui_spec: ui_types.UiSpec,
    data_date_range: tuple[int, int],
) -> go.Figure:
    df = _prepare_treemap_data(df, state, ui_spec=ui_spec)
    styles = _get_treemap_styles(df, state, ui_spec, data_date_range)
    return plotly.create_treemap(df=df, **styles)


def _prepare_treemap_data(
    df: pl.DataFrame, state: dict[str, typing.Any], ui_spec: ui_types.UiSpec
) -> pl.DataFrame:
    # filter by metric
    metric = state_module.get_df_metric(state, ui_spec)
    df = df.filter(pl.col.metric == metric)

    if metric in ui_spec['metric_types']['point_in_time']:
        now = tooltime.timestamp_to_seconds(state['now']) * 1e6
        df = df.filter(pl.col.timestamp == now)

    elif metric in ui_spec['metric_types']['unique']:
        # filter sample_interval
        ui_interval = state['sample_interval']
        interval = timestamps.ui_interval_to_df_interval[ui_interval]
        df = df.filter(pl.col.interval == interval)

        # select the closest point to now
        time_values = df['timestamp'].sort().unique()
        now = tooltime.timestamp_to_seconds(state['now']) * 1e6
        time_index = time_values.cast(pl.Int64).search_sorted(now)
        if time_index == len(time_values):
            time_index = -1
        time = time_values[time_index]
        df = df.filter(pl.col.timestamp == time)

    else:
        df = df.filter(pl.col.interval == 'day')

        # filter time window
        end_time = tooltime.timestamp_to_seconds(state['now'])
        if state['time_window'] == 'all':
            df = df.filter(pl.col.timestamp <= end_time * 1e6)
        else:
            window = tooltime.timelength_to_seconds(state['time_window'])
            start_time = end_time - window
            df = df.filter(
                pl.col.timestamp > start_time * 1e6,
                pl.col.timestamp <= end_time * 1e6,
            )

        # aggregate
        df = (
            df.filter(pl.col.metric == metric)
            .group_by('token', 'network')
            .agg(
                pl.sum('value'),
                min_timestamp=pl.min('timestamp'),
                max_timestamp=pl.max('timestamp'),
            )
        )

    return df


def _get_treemap_styles(
    df: pl.DataFrame,
    state: dict[str, typing.Any],
    ui_spec: ui_types.UiSpec,
    data_date_range: tuple[int, int],
) -> dict[str, typing.Any]:
    # create title
    title = ui_spec['helpers']['create_title'](
        df, state, data_date_range=data_date_range, ui_spec=ui_spec
    )

    # get prefix
    metric = state_module.get_df_metric(state, ui_spec=ui_spec)
    if ui_spec['metric_units'].get(metric) == '$':
        prefix = '$'
    else:
        prefix = None

    return {
        'title': title,
        'grouping': state['grouping'],
        'metric': metric,
        'prefix': prefix,
    }
