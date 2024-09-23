from __future__ import annotations

import datetime
from typing import Any, Literal, TypedDict
from typing_extensions import NotRequired


class UiSpec(TypedDict):
    default_state: dict[str, Any]
    invalid_states: list[dict[str, str]]
    inputs: dict[str, InputSpec]
    aliases: dict[str, dict[str, str]]
    reverse_aliases: dict[str, dict[str, str]]
    metric_types: MetricTypes
    metric_units: dict[str, str]
    submetrics: dict[str, list[str]]
    shortcuts: dict[str, ShortcutSpec]
    helpers: dict[str, Any]  # function


class InputSpec(TypedDict):
    type: Literal['button', 'date']
    description: str
    default: str
    visibility: NotRequired[InputVisibility]
    button_options: NotRequired[list[str]]
    date_options: NotRequired[tuple[datetime.datetime, datetime.datetime]]


class InputVisibility(TypedDict):
    start_hidden: NotRequired[bool]
    hide_if: NotRequired[list[dict[str, Any]]]
    show_if: NotRequired[list[dict[str, Any]]]
    f: NotRequired[Any]  # function


class MetricTypes(TypedDict):
    point_in_time: list[str]
    sum: list[str]
    unique: list[str]


class ShortcutSpec(TypedDict):
    action: Literal[
        'select',
        'cycle_next',
        'cycle_previous',
        'show_help',
        'increment',
        'decrement',
    ]
    field: str | None
    value: NotRequired[str]
    help: NotRequired[str]


def create_ui_spec(
    *,
    invalid_states: list[dict[str, str]],
    inputs: dict[str, InputSpec],
    aliases: dict[str, dict[str, str]],
    metric_types: MetricTypes,
    metric_units: dict[str, str],
    submetrics: dict[str, list[str]],
    shortcuts: dict[str, ShortcutSpec],
    helpers: dict[str, Any],
) -> UiSpec:
    reverse_aliases = {
        field: {v: k for k, v in aliases[field].items()}
        for field in aliases.keys()
    }

    default_state = {
        input: input_spec['default'] for input, input_spec in inputs.items()
    }

    ui_spec: UiSpec = {
        'default_state': default_state,
        'invalid_states': invalid_states,
        'inputs': inputs,
        'aliases': aliases,
        'reverse_aliases': reverse_aliases,
        'metric_types': metric_types,
        'metric_units': metric_units,
        'submetrics': submetrics,
        'shortcuts': shortcuts,
        'helpers': helpers,
    }

    validate_ui_spec(ui_spec)

    return ui_spec


def validate_ui_spec(ui_spec: UiSpec) -> None:
    # types match typeddict definitions
    pass

    # aliases match reverse aliases
    pass

    # every metric / submetric has a type
    pass

    # every metric present is defined
    pass
