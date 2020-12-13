import datetime
import json

import babel
from babel.dates import format_timedelta
from django.utils.safestring import mark_safe
from django.utils.timesince import timeuntil
from django_jinja import library
from django.contrib.humanize.templatetags import humanize
from django_jinja.utils import safe


@library.global_function
def intcomma(value: float):
    """
    Usage: {{ intcomma(35555) }}
    """
    return humanize.intcomma(value)


@library.global_function
def dict_to_highcharts(mydict, select_first=True):
    values = []
    item = 0
    for key, value in sorted(mydict.items(), key=lambda v: -v[1]):
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
