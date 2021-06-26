import datetime
import enum

from django.shortcuts import render
from botdata import models
# Create your views here.


class EventType(enum.IntEnum):
    PLACED = enum.auto()
    TRIPPED = enum.auto()
    DISARMED = enum.auto()


def landmines(request):
    # Players
    players_qs = models.Event2021UserData.objects.all()

    total_messages_sent = 0
    total_words_sent = 0
    total_points_won = 0
    total_points_recovered = 0
    total_points_acquired = 0
    total_points_current = 0
    total_points_exploded = 0
    total_points_spent = 0

    for player in players_qs:
        total_messages_sent += player.messages_sent
        total_words_sent += player.words_sent
        total_points_won += player.points_won
        total_points_recovered += player.points_recovered
        total_points_acquired += player.points_acquired
        total_points_current += player.points_current
        total_points_exploded += player.points_exploded
        total_points_spent += player.points_spent

    # Landmines
    landmines_qs = models.Event2021Landmines.objects.all().order_by('placed')

    total_landmines_count = 0
    tripped_landmines_count = 0
    disarmed_landmines_count = 0
    active_landmines_count = 0
    total_mines_over_time = []
    events = []
    for landmine in landmines_qs:
        placed_at_ts = landmine.placed.timestamp() * 1000
        if landmine.stopped_at:
            stopped_at_ts = landmine.stopped_at.timestamp() * 1000
        else:
            stopped_at_ts = None

        events.append((placed_at_ts, EventType.PLACED, landmine))

        # Counts
        total_landmines_count += 1
        if landmine.tripped:
            events.append((stopped_at_ts, EventType.TRIPPED, landmine))
            tripped_landmines_count += 1
        elif landmine.disarmed:
            events.append((stopped_at_ts, EventType.DISARMED, landmine))
            disarmed_landmines_count += 1
        else:
            active_landmines_count += 1

        # Timeseries
        total_mines_over_time.append((placed_at_ts, total_landmines_count))

    events.sort(key=lambda r: r[0])

    active_landmines_over_time = []
    active_landmines_stack = 0

    disarmed_landmines_over_time = []
    disarmed_landmines_stack = 0

    tripped_landmines_over_time = []
    tripped_landmines_stack = 0
    for event in events:
        event_time, event_type, event_landmine = event
        if event_type == EventType.PLACED:
            active_landmines_stack += 1
        elif event_type == EventType.DISARMED:
            active_landmines_stack -= 1
            disarmed_landmines_stack += 1
            disarmed_landmines_over_time.append((event_time, disarmed_landmines_stack))
        elif event_type == EventType.TRIPPED:
            active_landmines_stack -= 1
            tripped_landmines_stack += 1
            tripped_landmines_over_time.append((event_time, tripped_landmines_stack))

        active_landmines_over_time.append((event_time, active_landmines_stack))

    if events:
        # Fix to have the graph end at the same place.
        last_event_time = events[-1][0]

        disarmed_landmines_over_time.append((last_event_time, disarmed_landmines_stack))
        tripped_landmines_over_time.append((last_event_time, tripped_landmines_stack))

    ctx = {
        "total_messages_sent": total_messages_sent,
        "total_words_sent": total_words_sent,
        "total_points_won": total_points_won,
        "total_points_recovered": total_points_recovered,
        "total_points_acquired": total_points_acquired,
        "total_points_current": total_points_current,
        "total_points_exploded": total_points_exploded,
        "total_points_spent": total_points_spent,

        "total_landmines_count": total_landmines_count,
        "tripped_landmines_count": tripped_landmines_count,
        "disarmed_landmines_count": disarmed_landmines_count,
        "active_landmines_count": active_landmines_count,

        "total_mines_over_time": total_mines_over_time,
        "active_landmines_over_time": active_landmines_over_time,
        "disarmed_landmines_over_time": disarmed_landmines_over_time,
        "tripped_landmines_over_time": tripped_landmines_over_time,
    }

    return render(request, "stats/landmines.jinja2", ctx)
