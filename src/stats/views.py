import datetime
import enum
from collections import Counter, defaultdict

from django.shortcuts import render
from botdata import models


# Create your views here.

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
