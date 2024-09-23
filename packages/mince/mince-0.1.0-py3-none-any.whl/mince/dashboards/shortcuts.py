from __future__ import annotations

from typing import Any

from dash import html  # type: ignore
import dash_extensions  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
import tooltime

from . import timestamps
from . import ui_types


def _create_shortcuts_listeners(
    shortcuts: dict[str, ui_types.ShortcutSpec],
) -> dash_extensions.Keyboard:
    return dash_extensions.Keyboard(
        captureKeys=list(shortcuts.keys()), id='keyboard', n_keydowns=1
    )


def _create_help_modal(
    shortcuts: dict[str, ui_types.ShortcutSpec],
) -> dbc.Modal:
    rows = []
    for key, shortcut in shortcuts.items():
        field = shortcut['field']
        if field is not None:
            field = field.replace('_', ' ')
        # get description
        if 'help' in shortcut:
            description = shortcut['help']
        elif shortcut['action'] == 'show_help':
            description = 'toggle help'
        elif shortcut['action'] == 'select':
            description = html.Div(
                ['set ', field, ' to ', html.B(shortcut['value'])]
            )
        elif shortcut['action'] == 'cycle_next':
            description = html.Div(['go to next ', html.B(field)])
        elif shortcut['action'] == 'cycle_previous':
            description = html.Div(['go to previous ', html.B(field)])
        else:
            raise Exception('invalid shortcut action')

        # get key string
        if key == 'ArrowRight':
            key_str = '→'
        elif key == 'ArrowLeft':
            key_str = '←'
        else:
            key_str = key

        # build table row
        row = [
            html.Td(' '),
            html.Td(html.B(key_str)),
            html.Td(' '),
            html.Td(' '),
            html.Td(' '),
            html.Td(description),
            html.Td(' '),
        ]
        rows.append(row)

    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle('Keyboard Shortcuts')),
            dbc.ModalBody(
                html.Table(html.Tbody([html.Tr(row) for row in rows])),
            ),
        ],
        id='help-modal',
        size='sm',
        is_open=False,
    )


def _process_keyboard_shortcuts(
    display: dict[str, Any],
    help_open: bool,
    raw_shortcut: dict[str, Any],
    data_date_range: tuple[tooltime.Timestamp, tooltime.Timestamp],
    ui_spec: ui_types.UiSpec,
) -> bool:
    shortcut = ui_spec['shortcuts'][raw_shortcut['key']]
    field = shortcut['field']
    if shortcut['action'] == 'select' and field is not None:
        display[field] = shortcut['value']
    elif shortcut['action'] == 'cycle_next' and field is not None:
        options = ui_spec['inputs'][field]['button_options']
        index = options.index(display[field])
        if index + 1 == len(options):
            display[field] = options[0]
        else:
            display[field] = options[index + 1]
    elif shortcut['action'] == 'cycle_previous' and field is not None:
        options = ui_spec['inputs'][field]['button_options']
        index = options.index(display[field])
        if index == 0:
            display[field] = options[-1]
        else:
            display[field] = options[index - 1]
    elif (
        shortcut['action'] in ['increment', 'decrement']
        and shortcut['field'] == 'now'
    ):
        if raw_shortcut['ctrlKey'] or raw_shortcut['shiftKey']:
            value = 'medium'
        elif raw_shortcut['ctrlKey'] and raw_shortcut['shiftKey']:
            value = 'small'
        else:
            value = 'large'

        duration = timestamps.time_increments[display['time_window']][value]
        new_now_dt = tooltime.timestamp_to_datetime(display['now'][:10])
        if shortcut['action'] == 'increment':
            new_now_dt = timestamps._increment_datetime(new_now_dt, duration)
        elif shortcut['action'] == 'decrement':
            new_now_dt = timestamps._decrement_datetime(new_now_dt, duration)
        else:
            raise Exception()
        new_now = tooltime.timestamp_to_date(new_now_dt)

        # check that new time is valid
        min_now = tooltime.timestamp_to_date(data_date_range[0])
        if new_now < min_now:
            new_now = min_now
        max_now = tooltime.timestamp_to_date(data_date_range[1])
        if new_now > max_now:
            new_now = max_now

        display['now'] = new_now
    elif shortcut['action'] == 'show_help':
        help_open = not help_open
    else:
        raise Exception('invalid shortcut action')

    return help_open
