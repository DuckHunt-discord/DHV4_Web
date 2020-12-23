import datetime
import json
from typing import Union, List, Dict, Any

import babel
from babel.dates import format_timedelta
from django.utils.safestring import mark_safe
from django.utils.timesince import timeuntil
from django_jinja import library
from django.contrib.humanize.templatetags import humanize
from django_jinja.utils import safe

from botdata.models import DUCKS_COLORS


@library.global_function
def intcomma(value: float):
    """
    Usage: {{ intcomma(35555) }}
    """
    return humanize.intcomma(value)


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
            'y': value
        }

        if select_first and item == 0:
            point['sliced'] = True
            point['selected'] = True

        values.append(point)
        item += 1

    return mark_safe(json.dumps(values))


@library.global_function
def show_timestamp(timestamp:int):
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



