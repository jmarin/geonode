from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from geonode.people.models import PeopleGroup


def people_group_list(request):
    ctx = {
        "object_list": PeopleGroup.objects.all(),
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("people/group_list.html", ctx)


def people_group_detail(request, slug):
    group = get_object_or_404(PeopleGroup, slug=slug)
    
    if group.access == "private" and (request.user.is_authenticated() and group.user_is_member(request.user)):
        raise Http404()
    
    ctx = {
        "object": group,
        "maps": [], # @@@
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("people/group_detail.html", ctx)


def people_group_members(request, slug):
    group = get_object_or_404(PeopleGroup, slug=slug)
    
    if group.access == "private" and (request.user.is_authenticated() and group.user_is_member(request.user)):
        raise Http404()
    
    ctx = {
        "object": group,
        "members": group.member_queryset(),
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("people/group_members.html", ctx)
