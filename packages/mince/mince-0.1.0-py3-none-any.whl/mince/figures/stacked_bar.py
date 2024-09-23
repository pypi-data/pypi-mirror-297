from __future__ import annotations

from .. import styles

import typing

import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import polars as pl
import toolstr


def plot_stacked_bar(
    df: pl.DataFrame,
    metric: str,
    grouping: str,
    x: str = 'x',
    xlabel: str | None = None,
    ylabel: str | None = None,
    ytick_format: typing.Literal['$', '%'] | None = None,
    ylim: tuple[int | float | None, int | float | None] | None = None,
    title: str | None = None,
) -> go.Figure:
    # create formatted values
    if ytick_format == '$':
        toolstr_kwargs = {
            'order_of_magnitude': True,
            'decimals': 1,
            'prefix': '$',
        }
    elif ytick_format == '%':
        toolstr_kwargs = {'percentage': True, 'decimals': 1}
    else:
        toolstr_kwargs = {'order_of_magnitude': True, 'decimals': 1}
    df = df.with_columns(
        formatted_value=pl.col.value.map_elements(
            lambda x: toolstr.format(x, **toolstr_kwargs),  # type: ignore
            return_dtype=pl.String,
        )
    )

    fig = px.bar(
        df,
        x=x,
        y='value',
        color=grouping,
        color_discrete_map=styles.colors,
        custom_data=['formatted_value'],
    )

    if df['interval'][0] == 'month':
        for trace in fig.data:
            widths = trace['x'][1:] - trace['x'][:-1]
            widths = [item.total_seconds() * 1000 for item in widths]
            widths = widths + [widths[0]]
            trace.width = widths
            trace.offset = -1000 * 86400 * 15

    label_font = {
        'size': 18,
        'color': 'black',
        'family': 'monospace',
    }
    if title is None:
        title = metric
    title_kwargs = {
        'text': title,
        'y': 0.99,
        'font': {'size': 28, 'color': 'black', 'family': 'monospace'},
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    }
    axis = {
        'showgrid': True,
        'gridcolor': '#DFDFDF',
        'gridwidth': 1,
        'griddash': 'dot',
    }
    if ylabel is None:
        ylabel = metric
    yaxis = dict(axis, title=ylabel)
    if ylim is not None:
        yaxis['range'] = ylim
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        dragmode='zoom',
        xaxis=axis,
        yaxis=yaxis,
        bargap=0,
        bargroupgap=0,
        xaxis_fixedrange=True,
        xaxis_type='category',
        xaxis_title=None,
        yaxis_fixedrange=True,
        legend_title=None,
        legend_font={'size': 18, 'color': 'black', 'family': 'monospace'},
        # legend_traceorder='reversed',
        title=title_kwargs,
        hovermode='x unified',
    )
    if xlabel is not None:
        fig.update_layout(
            xaxis=dict(title=xlabel),
        )
    fig.update_traces(
        marker_line_width=0.1,
        marker_line_color='black',
        hoverinfo='text+x+y',
    )
    fig.update_layout(
        hoverlabel={
            'font_size': 12,
        },
    )

    label_font = {
        'size': 18,
        'color': 'black',
        'family': 'monospace',
    }
    fig.update_xaxes(
        title_font=label_font,
        tickfont=label_font,
        showspikes=True,
        spikesnap='cursor',
        spikemode='across',
        spikethickness=1,
        spikecolor='black',
        spikedash='solid',
    )
    if df[x].dtype == pl.Datetime:
        fig.update_xaxes(
            nticks=7,
            # autotickangles=[90],
        )
        fig.update_layout(
            xaxis=dict(
                tickformat='%Y-%m-%d',
                type='date',
            ),
        )
    fig.update_yaxes(
        title_font=label_font,
        tickfont=label_font,
        showspikes=True,
        spikesnap='cursor',
        spikemode='across',
        spikethickness=1,
        spikecolor='black',
        spikedash='solid',
    )

    # set ytick format
    if ytick_format is not None:
        if ytick_format == '$':
            fig.update_yaxes(tickprefix='$')
        elif ytick_format == '%':
            fig.update_yaxes(tickformat='.0%')
        else:
            raise Exception('invalid yformat: ' + str(ytick_format))

    fig.update_traces(
        hovertemplate='%{fullData.name} %{customdata[0]}<extra></extra>'
    )

    return fig
