from __future__ import annotations

import plotly.graph_objects as go  # type: ignore
from dash import Dash, Input, Output, State  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore

from . import dashboard
from . import inputs as inputs_module
from . import ui_types
from . import urls
from . import state as state_module


def _create_app(
    name: str,
    dashboard: dashboard.Dashboard,
    assets_folder: str | None = None,
    debug: bool = False,
    external_stylesheets: list[str] = [dbc.themes.BOOTSTRAP],
) -> Dash:
    # create app
    if assets_folder is None:
        assets_folder = '/home/storm/repos/stables/assets'
    app = Dash(
        name,
        assets_folder=assets_folder,
        external_stylesheets=external_stylesheets,
    )
    app.title = name
    n_keydowns = 0

    # create inputs
    inputs = inputs_module.create_inputs(dashboard.spec, dashboard.dfs)

    # create layout
    app.layout = dashboard.get_layout(inputs)

    # add serverside callbacks
    update_ui_args, update_chart_args = _compute_decorator_args(dashboard.spec)

    @app.callback(*update_ui_args)  # type: ignore
    def update_ui(*args) -> list[str | bool]:
        # parse input args
        *raw_display, url, initial_load, _n_keydowns, shortcut, help_open = args
        display = dict(zip(list(inputs.keys()), raw_display))

        # load from url
        if initial_load:
            urls.parse_url(url, display, dashboard.spec['default_state'])
            initial_load = False

        # process keyboard shortcuts
        nonlocal n_keydowns
        if _n_keydowns <= n_keydowns:
            shortcut = None
        else:
            help_open = dashboard.process_shortcuts(
                display, help_open, shortcut
            )
        n_keydowns = _n_keydowns

        # based on most recent selection, fix any invalid button values
        state_module._fix_invalid_inputs(display, shortcut, dashboard.spec)

        # update url based on radio button values
        url = urls.create_new_url(
            display, defaults=dashboard.spec['default_state']
        )

        # Update visibility of interval, time, and yscale radio buttons
        raw_classes = inputs_module.compute_input_classes(
            display, dashboard.spec
        )
        classes = list(raw_classes.values())

        return list(display.values()) + classes + [url, initial_load, help_open]

    # add chart callback
    @app.callback(*update_chart_args)  # type: ignore
    def update_chart(*args) -> go.Figure:
        kwargs = dict(zip(inputs.keys(), args))
        kwargs['now'] = kwargs['now'][:10]
        state = state_module.build_state(
            _fix=False, _ui_spec=dashboard.spec, **kwargs
        )
        dashboard.create_chart(state)

    # add clientside callbacks
    inputs_module._prevent_button_focus(app)

    return app


def _compute_decorator_args(
    ui_spec: ui_types.UiSpec,
) -> tuple[list[Input | Output | State], list[Input | Output | State]]:
    dash_input_values = []
    dash_output_values = []
    dash_output_classes = []
    for name, input_spec in ui_spec['inputs'].items():
        if input_spec['type'] == 'button':
            dash_input_values.append(Input(name + '-radio', 'value'))
            dash_output_values.append(Output(name + '-radio', 'value'))
            dash_output_classes.append(Output(name + '-radio', 'className'))
        elif input_spec['type'] == 'date':
            dash_input_values.append(Input('date-picker', 'date'))
            dash_output_values.append(Output('date-picker', 'date'))
            dash_output_classes.append(Output('date-picker', 'className'))
        else:
            raise Exception('invalid type')

    update_ui_args = [
        dash_output_values,
        dash_output_classes,
        [
            Output('url', 'search'),
            Output('initial-load', 'data'),
            Output('help-modal', 'is_open'),
        ],
        dash_input_values,
        [
            Input('url', 'search'),
            State('initial-load', 'data'),
            Input('keyboard', 'n_keydowns'),
            State('keyboard', 'keydown'),
            State('help-modal', 'is_open'),
        ],
    ]

    update_chart_args = [Output('main-chart', 'figure'), dash_input_values]

    return update_ui_args, update_chart_args
