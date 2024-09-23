from __future__ import annotations

import urllib.parse
import tooltime


def parse_url(
    url_search: str,
    display: dict[str, str],
    defaults: dict[str, str],
) -> None:
    parsed = urllib.parse.parse_qs(urllib.parse.urlparse(url_search).query)
    for key in defaults.keys():
        if key in parsed:
            display[key] = parsed[key][0]
    if 'now' in parsed:
        display['now'] = parsed['now'][0]


def create_new_url(display: dict[str, str], defaults: dict[str, str]) -> str:
    params: list[str] = []
    for key, value in defaults.items():
        if display[key] != value:
            params.append(key + '=' + display[key])

    current_now = display.get('now')
    if current_now is not None and tooltime.timestamp_to_seconds(
        current_now[:10]
    ) != tooltime.timestamp_to_seconds(defaults['now']):
        params.append('now=' + tooltime.timestamp_to_date(current_now[:10]))

    return '?' + '&'.join(params) if params else ''
