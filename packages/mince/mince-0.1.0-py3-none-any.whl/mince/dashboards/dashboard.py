from __future__ import annotations

from typing import Any

from dash import Dash, dcc, html  # type: ignore
import plotly.graph_objects as go  # type: ignore
import polars as pl

from . import apps
from . import figures
from . import timestamps
from . import shortcuts
from . import ui_types


class Dashboard:
    spec: ui_types.UiSpec
    dfs: dict[str, pl.DataFrame]
    date_ranges: dict[str, tuple[int, int]]
    debug: bool
    app: Dash
    n_keydowns: int

    def __init__(
        self,
        *,
        name: str,
        dfs: dict[str, pl.DataFrame],
        spec: ui_types.UiSpec,
        debug: bool = False,
        assets_folder: str | None = None,
    ):
        self.spec = spec
        self.dfs = dfs
        self.date_ranges = {
            name: timestamps._get_date_range(df) for name, df in dfs.items()
        }
        self.app = apps._create_app(
            name=name,
            dashboard=self,
            debug=debug,
            assets_folder=assets_folder,
        )
        self.n_keydowns = 0

    def run(
        self, port: str = '8052', jupyter_mode: str = 'external', **kwargs: Any
    ) -> None:
        self.app.run(jupyter_mode=jupyter_mode, port=port, **kwargs)

    def get_layout(self, inputs: dict[str, html.Div]) -> list[html.Div]:
        return [
            shortcuts._create_shortcuts_listeners(self.spec['shortcuts']),
            dcc.Location(id='url', refresh=False),
            dcc.Store(id='initial-load', data=True),
            html.Div(list(inputs.values()), className='radio-group-row'),
            dcc.Graph(id='main-chart', config={'responsive': True}),
            shortcuts._create_help_modal(self.spec['shortcuts']),
            html.Div(id='prevent-focus-trigger'),
        ]

    def get_dataset(self, state: dict[str, Any]) -> str:
        if len(self.dfs) == 1:
            return next(iter(self.dfs.keys()))
        else:
            raise NotImplementedError('get_dataset()')

    def process_shortcuts(
        self,
        state: dict[str, Any],
        help_open: bool,
        raw_shortcut: dict[str, Any],
    ) -> bool:
        return shortcuts._process_keyboard_shortcuts(
            display=state,
            help_open=help_open,
            raw_shortcut=raw_shortcut,
            data_date_range=self.date_ranges[self.get_dataset(state)],
            ui_spec=self.spec,
        )

    def create_chart(self, state: dict[str, Any]) -> go.Figure:
        data_name = self.get_dataset(state)
        df = self.dfs[data_name]
        date_range = self.date_ranges[data_name]

        if state['format'] in ['line', 'line %', 'area', 'area %']:
            return figures.create_time_series_fig(
                df, state, self.debug, ui_spec=self.spec
            )
        elif state['format'] == 'tree':
            return figures.create_tree_fig(
                df, state, ui_spec=self.spec, data_date_range=date_range
            )
        else:
            raise Exception('invalid format: ' + str(state['format']))
