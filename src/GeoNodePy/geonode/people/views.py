from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.http import require_POST

from geonode.people.forms import PeopleGroupInviteForm
from geonode.people.models import PeopleGroup


def people_group_list(request):
    ctx = {
        "object_list": PeopleGroup.objects.all(),
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("groups/group_list.html", ctx)


def people_group_detail(request, slug):
    group = get_object_or_404(PeopleGroup, slug=slug)
    
    if not group.can_view(request.user):
        raise Http404()
    
    ctx = {
        "object": group,
        "maps": [], # @@@
        "members": group.member_queryset(),
        "is_member": group.user_is_member(request.user),
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("groups/group_detail.html", ctx)


def people_group_members(request, slug):
    group = get_object_or_404(PeopleGroup, slug=slug)
    ctx = {}
    
    if not group.can_view(request.user):
        raise Http404()
    
    if group.access in ["public-invite", "private"] and group.user_is_role(request.user, "manager"):
        ctx["invite_form"] = PeopleGroupInviteForm()
    
    ctx.update({
        "object": group,
        "members": group.member_queryset(),
        "is_member": group.user_is_member(request.user),
        "is_manager": group.user_is_role(request.user, "manager"),
    })
    ctx = RequestContext(request, ctx)
    return render_to_response("groups/group_members.html", ctx)


@require_POST
def people_group_invite(request, slug):
    group = get_object_or_404(PeopleGroup, slug=slug)
    
    if not group.can_invite(request.user):
        raise Http404()
    
    form = PeopleGroupInviteForm(request.POST)
    
    if form.is_valid():
        for user in form.cleaned_data["users"]:
            group.invite(user, role=form.cleaned_data["role"])
    
    return redirect("people_group_members", slug=group.slug)
