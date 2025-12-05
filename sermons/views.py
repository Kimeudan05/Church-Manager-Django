from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models


# Create your views here.

from .models import Sermon
from .forms import SermonForm
from events.models import Event


# Helper for pastor
def pastor_required(function):
    def wrapper(request, *args, **kwargs):
        if (
            request.user.profile.role != "pastor"
            and request.user.profile.role != "admin"
        ):
            messages.error(request, "Access Denied")
            return redirect("dashboard:index")
        return function(request, *args, **kwargs)

    return wrapper


@login_required
@pastor_required
def sermons_list(request):
    sermons = Sermon.objects.all().order_by("-date")  # date desc
    return render(request, "sermons/sermon_list.html", {"sermons": sermons})


@login_required
@pastor_required
def sermon_create(request):
    if request.method == "POST":
        form = SermonForm(request.POST, request.FILES)
        if form.is_valid():
            sermon = form.save(commit=False)
            sermon.created_by = request.user
            sermon.save()
            messages.success(request, "Sermon created successfully.")
            return redirect("sermons:list")
    else:
        form = SermonForm()

    return render(
        request, "sermons/sermon_form.html", {"form": form, "title": "Add Sermon"}
    )


@login_required
@pastor_required
def sermon_update(request, pk):
    sermon = get_object_or_404(Sermon, pk=pk)

    if request.method == "POST":
        form = SermonForm(request.POST, request.FILES, instance=sermon)
        if form.is_valid():
            sermon = form.save(commit=False)
            sermon.created_by = request.user
            sermon.save()
            messages.success(request, "Sermon updated successfully.")
            return redirect("sermons:list")
    else:
        form = SermonForm(instance=sermon)

    return render(
        request, "sermons/sermon_form.html", {"form": form, "title": "Update Sermon"}
    )


@login_required
@pastor_required
def sermon_delete(request, pk):
    sermon = get_object_or_404(Sermon, pk=pk)
    if request.method == "POST":
        sermon.delete()
        messages.success(request, "Sermon deleted successfully.")
        return redirect("sermons:list")
    return render(request, "sermons/sermon_confirm_delete.html", {"sermon": sermon})


@login_required
def sermon_detail(request, pk):
    sermon = get_object_or_404(Sermon, pk=pk)
    return render(request, "sermons/sermon_detail.html", {"sermon": sermon})
