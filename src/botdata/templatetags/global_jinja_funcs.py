import datetime
import json
import re
from typing import Union, List, Dict, Any

from babel.dates import format_timedelta
from babel.lists import format_list
from django.utils.safestring import mark_safe
from django_jinja import library
from django.contrib.humanize.templatetags import humanize
from botdata.models import DUCKS_COLORS

_paragraph_re = re.compile(r"(?:\r\n|\r(?!\n)|\n){2,}")


@library.filter
def nl2br(value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace(u'\r\n', u'<br/>') for p in _paragraph_re.split(value))
    return mark_safe(result)


@library.global_function
def intcomma(value: float):
    """
    Usage: {{ intcomma(35555) }}
    """
    return humanize.intcomma(value)


@library.global_function
def humanize_list(value: list):
    """
    Usage: {{ humanize_list(list) }}
    """
    return format_list(value, locale='en_US')


@library.global_function
def dict_to_highcharts(mydict, select_first=True, reverse=False):
    values = []
    item = 0

    ordered_items = sorted(mydict.items(), key=lambda v: -v[1])
    if reverse:
        ordered_items.reverse()

    for key, value in ordered_items:
        point = {
            'name': key.title(),
            'y': round(value, 3)
        }

        if select_first and item == 0:
            point['sliced'] = True
            point['selected'] = True

        values.append(point)
        item += 1

    return mark_safe(json.dumps(values))


@library.global_function
def show_timestamp(timestamp: int):
    td = datetime.datetime.now() - datetime.datetime.fromtimestamp(timestamp)
    return format_timedelta(td, locale="en_US", threshold=1.1, format="short")


@library.global_function
def ducks_names_to_colors(ducks: Union[str, List[str], Dict[Any, int]], reverse=False):
    if isinstance(ducks, str):
        return DUCKS_COLORS[ducks]
    elif isinstance(ducks, dict):
        sorted_items = sorted(ducks.items(), key=lambda v: -v[1])
        if reverse:
            sorted_items.reverse()
        return [DUCKS_COLORS[name] for name, value in sorted_items]
    else:
        return [DUCKS_COLORS[name] for name in ducks]


@library.global_function
def titleize(strings: List[str]):
    return [string.title() for string in strings]


@library.global_function
def values_from_keys(keys: List[str], dict_: dict):
    return [dict_[key] for key in keys]


@library.global_function
def format_settings_value(value):
    if isinstance(value, bool):
        if value:
            return "✅"
        else:
            return "❌"
