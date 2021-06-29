import datetime
import enum
from collections import Counter, defaultdict

from django.shortcuts import render
from botdata import models


# Create your views here.


class LandmineEventType(enum.IntEnum):
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

    players_compare = defaultdict(lambda: defaultdict(int))

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
    landmines_qs = models.Event2021Landmines.objects.all().order_by('placed').prefetch_related('placed_by__user', 'stopped_by__user')

    words = Counter()
    total_landmines_count = 0
    tripped_landmines_count = 0
    disarmed_landmines_count = 0
    active_landmines_count = 0
    total_mines_over_time = []
    events = []
    for landmine in landmines_qs:
        placed_by = landmine.placed_by.user
        players_compare[placed_by]["placed"] += 1
        placed_at_ts = landmine.placed.timestamp() * 1000
        if landmine.stopped_at:
            stopped_at_ts = landmine.stopped_at.timestamp() * 1000
        else:
            stopped_at_ts = None

        events.append((placed_at_ts, LandmineEventType.PLACED, landmine))

        # Counts
        total_landmines_count += 1
        if landmine.tripped:
            players_compare[placed_by]["tripped"] += 1
            players_compare[landmine.stopped_by.user]["stepped"] += 1
            words[landmine.word] += 1
            events.append((stopped_at_ts, LandmineEventType.TRIPPED, landmine))
            tripped_landmines_count += 1
        elif landmine.disarmed:
            words[landmine.word] += 1
            events.append((stopped_at_ts, LandmineEventType.DISARMED, landmine))
            disarmed_landmines_count += 1
        else:
            active_landmines_count += 1

        # Timeseries
        total_mines_over_time.append((placed_at_ts, total_landmines_count))

    players_compare_graph = []
    for player_compared, player_data in players_compare.items():
        players_compare_graph.append({
            "player": str(player_compared),
            "x": player_data["placed"],
            "y": player_data["stepped"],
            "z": player_data["tripped"],
        })

    events.sort(key=lambda r: r[0])

    active_landmines_over_time = []
    active_landmines_stack = 0

    destroyed_landmines_over_time = []
    destroyed_landmines_stack = 0

    disarmed_landmines_over_time = []
    disarmed_landmines_stack = 0

    tripped_landmines_over_time = []
    tripped_landmines_stack = 0
    if events:
        # Fix to have the graph start at the same place.
        first_event_time = events[0][0]
        disarmed_landmines_over_time.append((first_event_time, 0))
        tripped_landmines_over_time.append((first_event_time, 0))

    streamgraph_series = []
    steamgraph_default = []

    for event in events:
        event_time, event_type, event_landmine = event
        if event_type == LandmineEventType.PLACED:
            active_landmines_stack += 1
        elif event_type == LandmineEventType.DISARMED:
            active_landmines_stack -= 1
            disarmed_landmines_stack += 1
            destroyed_landmines_stack += 1
            disarmed_landmines_over_time.append((event_time, disarmed_landmines_stack))
            destroyed_landmines_over_time.append((event_time, destroyed_landmines_stack))
        elif event_type == LandmineEventType.TRIPPED:
            active_landmines_stack -= 1
            tripped_landmines_stack += 1
            destroyed_landmines_stack += 1
            tripped_landmines_over_time.append((event_time, tripped_landmines_stack))
            destroyed_landmines_over_time.append((event_time, destroyed_landmines_stack))

        active_landmines_over_time.append((event_time, active_landmines_stack))

        # Streamgraph
        placed_by = event_landmine.placed_by.user
        data_added = False
        for steamgraph in streamgraph_series:
            change = 1 if event_type == LandmineEventType.PLACED else -1
            if steamgraph["pk"] == placed_by.pk:
                count = steamgraph["data"][-1][1] + change

                steamgraph["data"].append((event_time, count))
                data_added = True
            else:
                steamgraph["data"].append((event_time, steamgraph["data"][-1][1]))

        if not data_added:
            streamgraph_series.append({
                "name": f"{placed_by}",
                "pk": placed_by.pk,
                "data": steamgraph_default.copy() + [(event_time, 1)],
            })
        steamgraph_default.append((event_time, 0))

    if events:
        # Fix to have the graph end at the same place.
        last_event_time = events[-1][0]
        disarmed_landmines_over_time.append((last_event_time, disarmed_landmines_stack))
        tripped_landmines_over_time.append((last_event_time, tripped_landmines_stack))
        destroyed_landmines_over_time.append((last_event_time, destroyed_landmines_stack))
        total_mines_over_time.append((last_event_time, total_landmines_count))



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
        "most_common_words": words.most_common(),

        "players_compare_graph": players_compare_graph,

        "total_mines_over_time": total_mines_over_time,
        "active_landmines_over_time": active_landmines_over_time,
        "disarmed_landmines_over_time": disarmed_landmines_over_time,
        "tripped_landmines_over_time": tripped_landmines_over_time,
        "destroyed_landmines_over_time": destroyed_landmines_over_time,

        "streamgraph_series": streamgraph_series,
    }

    return render(request, "stats/landmines.jinja2", ctx)


class TicketEventType(enum.IntEnum):
    OPENED = enum.auto()
    CLOSED = enum.auto()


def support(request):
    tickets_qs = models.SupportTicket.objects.all().prefetch_related('closed_by').order_by('opened_at')

    total_tickets = 0
    total_open_tickets = 0
    best_closers = Counter()
    events = []
    total_tickets_over_time = []

    for ticket in tickets_qs:
        opened_at_ts = ticket.opened_at.timestamp() * 1000

        events.append((opened_at_ts, TicketEventType.OPENED, ticket))
        total_tickets += 1
        total_tickets_over_time.append((opened_at_ts, total_tickets))
        if not ticket.closed:
            total_open_tickets += 1
        else:
            closed_at_ts = ticket.closed_at.timestamp() * 1000
            events.append((closed_at_ts, TicketEventType.CLOSED, ticket))
            best_closers[ticket.closed_by] += 1

    events.sort(key=lambda r: r[0])
    opened_tickets_over_time = []
    opened_tickets_stack = 0
    for event in events:
        event_time, event_type, event_ticket = event

        if event_type == TicketEventType.OPENED:
            opened_tickets_stack += 1
        elif event_type == TicketEventType.CLOSED:
            opened_tickets_stack -= 1

        opened_tickets_over_time.append((event_time, opened_tickets_stack))

    if events:
        last_event_time = events[-1][0]
        total_tickets_over_time.append((last_event_time, total_tickets))

    best_closers_graph = []

    for best_closer, n in best_closers.most_common():
        if best_closer:
            best_closers_graph.append({
                "name": f"{best_closer}",
                "y": n,
            })
        else:
            best_closers_graph.append({
                "name": f"Automatic closing for inactivity",
                "y": n,
                "sliced": True,
                "selected": True
            })

    ctx = {
        "total_tickets": total_tickets,
        "total_open_tickets": total_open_tickets,

        "total_tickets_over_time": total_tickets_over_time,
        "opened_tickets_over_time": opened_tickets_over_time,
        "best_closers": best_closers_graph,
    }

    return render(request, "stats/support.jinja2", ctx)
