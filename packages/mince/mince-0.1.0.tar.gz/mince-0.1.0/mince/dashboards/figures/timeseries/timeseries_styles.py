from __future__ import annotations

from typing import Any

import polars as pl

from ...state import get_df_metric
from ... import ui_types


def _get_timeseries_style_kwargs(
    state: dict[str, Any],
    df: pl.DataFrame,
    data_date_range: tuple[int, int],
    ui_spec: ui_types.UiSpec,
) -> dict[str, Any]:
    # get yscale
    log_y = False
    if state['format'] == 'line' and state['yscale'] == 'log':
        log_y = True

    relative_y = False
    if state['format'] == 'line' and state['yscale'] == 'relative':
        relative_y = True

    # get ytick format
    if state['format'] in ['line %', 'area %']:
        ytick_format = '%'
    elif state['metric'] in ['total_supply', 'volume']:
        ytick_format = '$'
    else:
        ytick_format = None

    # get ylabel
    ylabel = (
        ui_spec['reverse_aliases']['sample_interval'][
            state['sample_interval']
        ].lower()
        + ' '
        + ui_spec['reverse_aliases']['metric'][state['metric']].lower()
    )
    if state['format'] in ['line %', 'area %']:
        ylabel = ylabel + ' share'

    # get title
    title = ui_spec['helpers']['create_title'](
        df=df, state=state, data_date_range=data_date_range, ui_spec=ui_spec
    )

    # get xlabel
    if state['sample_interval'] == 'month':
        xlabel = 'month'
    elif state['sample_interval'] == 'week':
        xlabel = 'week'
    elif state['sample_interval'] == 'date':
        xlabel = 'date'
    else:
        raise Exception(
            'invalid selected sample_interval: ' + str(state['sample_interval'])
        )

    x = 'timestamp'
    total = False
    hover = True

    if state['format'] == 'line':
        # toggle total entry
        if state['total'] == 'total':
            total = True
        elif state['total'] == 'no total':
            total = False
        else:
            raise Exception('unknown value for total: ' + str(state['total']))

        # toggle hover
        if state['hover'] == 'hover':
            hover = True
        elif state['hover'] == 'no hover':
            hover = False
        else:
            raise Exception('unknown value for hover: ' + str(state['hover']))

        # age-specific styles
        if state['xalign'] == 'age':
            if state['sample_interval'] == 'date':
                xlabel = 'days'
            else:
                xlabel = xlabel + 's'
            xlabel = state['grouping'] + ' age (' + xlabel + ')'
            x = 'age'

        # relative styles
        if state['ynormalize'] == 'relative':
            ytick_format = '%'

    # return options based on figure type
    df_metric = get_df_metric(state, ui_spec)
    if state['format'] in ['line', 'line %']:
        return dict(
            metric=df_metric,
            grouping=state['grouping'],
            x=x,
            log_y=log_y,
            relative_y=relative_y,
            xlabel=xlabel,
            ylabel=ylabel,
            ytick_format=ytick_format,
            title=title,
            hover=hover,
            total=total,
        )
    elif state['format'] in ['area', 'area %']:
        styles: dict[str, Any] = dict(
            metric=state['metric'],
            grouping=state['grouping'],
            x=x,
            xlabel=xlabel,
            ylabel=ylabel,
            ytick_format=ytick_format,
            title=title,
        )
        if state['format'] == 'area %':
            styles['ylim'] = [0, 1]
        return styles
    else:
        raise Exception('invalid format')
