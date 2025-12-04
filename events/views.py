from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from .forms import EventForm


# Create your views here.


@login_required
def event_list(request):
    events = Event.objects.all().order_by("date")
    return render(request, "events/event_list.html", {"events": events})


@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user

            # If global event, remove group value
            if event.event_type == "global":
                event.group = None

            event.save()
            messages.success(request, "Event created successfully.")
            return redirect("events:list")
    else:
        form = EventForm()
    return render(
        request, "events/event_form.html", {"form": form, "title": "Create Event"}
    )


@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            updated_event = form.save(commit=False)

            # If global event, remove group value
            if updated_event.event_type == "global":
                updated_event.group = None
            updated_event.save()
            messages.success(request, "Event updated successfully.")
            return redirect("events:list")
    else:
        form = EventForm(instance=event)
    return render(
        request, "events/event_form.html", {"form": form, "title": "Update Event"}
    )


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect("events:list")
    return render(request, "events/event_confirm_delete.html", {"event": event})
