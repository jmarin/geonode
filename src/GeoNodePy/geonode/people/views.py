from django.shortcuts import render_to_response
from django.template import RequestContext

from geonode.people.models import PeopleGroup


def people_group_list(request):
    ctx = {
        "object_list": PeopleGroup.objects.all(),
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("people/group_list.html", ctx)