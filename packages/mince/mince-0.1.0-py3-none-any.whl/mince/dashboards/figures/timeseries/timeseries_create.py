from __future__ import annotations

import time
import typing

import polars as pl
import plotly.graph_objects as go  # type: ignore

from .... import plotly
from ... import timestamps
from ... import ui_types
from . import timeseries_data
from . import timeseries_styles


def create_time_series_fig(
    df: pl.DataFrame,
    state: dict[str, typing.Any],
    debug: bool,
    ui_spec: ui_types.UiSpec,
) -> go.Figure:
    data_date_range = timestamps._get_date_range(df)

    # prepare data
    start_time = time.time()
    df = timeseries_data._prepare_time_series_data(df, state, ui_spec=ui_spec)
    end_time = time.time()

    # create style kwargs
    style_kwargs = timeseries_styles._get_timeseries_style_kwargs(
        state, df, data_date_range=data_date_range, ui_spec=ui_spec
    )

    # print debug messages
    if debug:
        print()
        print('filtered data')
        print(
            'data filtering took',
            '%.6f' % ((end_time - start_time) * 1000),
            'milliseconds',
        )
        print('columns:', df.columns)
        print(df)

    # plot
    if state['format'] in ['line', 'line %']:
        return plotly.plot_line(df, **style_kwargs)
    elif state['format'] in ['area', 'area %']:
        return plotly.plot_stacked_bar(df, **style_kwargs)
    else:
        raise Exception('invalid format: ' + str(state['format']))
