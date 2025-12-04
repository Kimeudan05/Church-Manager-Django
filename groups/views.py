from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MinistryGroup
from .forms import MinistryGroupForm


# Create your views here.
@login_required
def group_list(request):
    groups = MinistryGroup.objects.all()
    return render(request, "groups/group_list.html", {"groups": groups})


@login_required
def group_create(request):
    if request.method == "POST":
        form = MinistryGroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Group created successfully!")
            return redirect("groups:list")
    else:
        form = MinistryGroupForm()
    return render(
        request, "groups/group_form.html", {"form": form, "title": "Create Group"}
    )


@login_required
def group_update(request, pk):
    group = get_object_or_404(MinistryGroup, pk=pk)
    if request.method == "POST":
        form = MinistryGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Group updated successfully.")
            return redirect("groups:list")
    else:
        form = MinistryGroupForm(instance=group)
    return render(
        request, "groups/group_form.html", {"form": form, "title": "Update Group"}
    )


@login_required
def group_delete(request, pk):
    group = get_object_or_404(MinistryGroup, pk=pk)
    if request.method == "POST":
        group.delete()
        messages.success(request, "Group deleted successfully.")
        return redirect("groups:list")
    return render(
        request,
        "groups/group_confirm_delete.html",
        {"group": group, "title": "Delete Group"},
    )
