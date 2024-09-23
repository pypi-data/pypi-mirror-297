from __future__ import annotations

import typing

import polars as pl
import toolstr
import plotly.graph_objects as go  # type: ignore

from .. import styles


def create_treemap(
    df: pl.DataFrame,
    title: str,
    metric: str,
    grouping: str,
    prefix: str | None = None,
    colors: typing.Mapping[str, str] = styles.colors,
) -> go.Figure:
    toolstr_kwargs: dict[str, typing.Any] = {
        'order_of_magnitude': True,
        'decimals': 1,
    }
    if prefix is not None:
        toolstr_kwargs['prefix'] = prefix

    grand_total = df['value'].sum()

    names = []
    sizes = []
    parents: list[str | None] = []
    custom_data = []

    names.append(title)
    sizes.append(grand_total)
    parents.append(None)
    custom_data.append(
        '<b>{name}</b><br>'.format(name=title)
        + toolstr.format(grand_total, **toolstr_kwargs)
        + ' total '
        + metric
    )
    top_parent = title

    if grouping == 'token':
        other_grouping = 'network'
    elif grouping == 'network':
        other_grouping = 'token'
    else:
        raise Exception('invalid grouping: ' + str(grouping))

    grouped = (
        df.group_by(grouping)
        .agg(pl.sum('value'))
        .sort('value', descending=True)
    )
    for group, value in grouped.rows():
        names.append(group)
        sizes.append(value)
        parents.append(top_parent)
        custom_data.append(
            '<b>{name}</b><br>'.format(name=group)
            + toolstr.format(value, **toolstr_kwargs)
            + ' '
            + metric
            + '<br>'
            + toolstr.format(value / grand_total, percentage=True, decimals=1)
            + ' of total'
        )

    for group, value in grouped.rows():
        other_grouped = df.filter(pl.col(grouping) == group)
        token_total = other_grouped['value'].sum()
        other_grouped = other_grouped.with_columns(
            prop=(pl.col.value / pl.col.value.sum()),
        )  # .filter(pl.col.prop > 0.001)
        if len(other_grouped) >= 2:
            for other_group, value in other_grouped[
                [other_grouping, 'value']
            ].rows():
                while other_group in names:
                    other_group = ' ' + other_group + ' '
                names.append(other_group)
                sizes.append(value)
                parents.append(group)
                if grand_total == 0:
                    grand_fraction = 0
                else:
                    grand_fraction = value / grand_total
                if token_total == 0:
                    token_fraction = 0
                else:
                    token_fraction = value / token_total
                custom_data.append(
                    (
                        '<b>{name}</b><br>'.format(
                            name=other_group + ' ' + group
                        )
                        + toolstr.format(value, **toolstr_kwargs)
                        + ' '
                        + metric
                        + '<br>'
                        + toolstr.format(
                            grand_fraction, percentage=True, decimals=1
                        )
                        + ' of total'
                        + '<br>'
                        + toolstr.format(
                            token_fraction, percentage=True, decimals=1
                        )
                        + '% of {group}'.format(group=group)
                    )
                )

    fig = go.Figure(
        go.Treemap(
            labels=names,
            parents=parents,
            values=sizes,
            textfont=dict(
                family='monospace',
                size=28,
            ),
            branchvalues='total',
            customdata=custom_data,
        ),
    )

    fig.update_traces(
        textposition='middle center',
        hovertemplate='%{customdata}<extra></extra>',
        hoverlabel={'font': {'size': 22, 'family': 'Monospace'}},
    )

    fig.update_traces(selector=dict(label=title), textfont=dict(color='red'))

    margin = 1
    fig.update_layout(
        margin=dict(t=margin, l=margin, r=margin, b=margin),
        treemapcolorway=[
            colors.get(group) for group in grouped[grouping] if group in colors
        ],
    )

    return fig
