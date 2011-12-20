from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required

from geonode.groups.forms import GroupInviteForm, AddGroupMapForm, AddGroupLayerForm
from geonode.groups.models import Group, GroupInvitation

from geonode.maps.models import Layer, Map, GroupLayer, GroupMap


def group_list(request):
    ctx = {
        "object_list": Group.objects.all(),
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("groups/group_list.html", ctx)


def group_detail(request, slug):
    group = get_object_or_404(Group, slug=slug)
    
    if not group.can_view(request.user):
        raise Http404()
        
    maps = GroupMap.maps_for_group(group)
    layers = GroupLayer.layers_for_group(group)
    
    ctx = {
        "object": group,
        "maps": maps,
        "layers": layers,
        "members": group.member_queryset(),
        "is_member": group.user_is_member(request.user),
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("groups/group_detail.html", ctx)


def group_members(request, slug):
    group = get_object_or_404(Group, slug=slug)
    ctx = {}
    
    if not group.can_view(request.user):
        raise Http404()
    
    if group.access in ["public-invite", "private"] and group.user_is_role(request.user, "manager"):
        ctx["invite_form"] = GroupInviteForm()
    
    ctx.update({
        "object": group,
        "members": group.member_queryset(),
        "is_member": group.user_is_member(request.user),
        "is_manager": group.user_is_role(request.user, "manager"),
    })
    ctx = RequestContext(request, ctx)
    return render_to_response("groups/group_members.html", ctx)


@require_POST
def group_invite(request, slug):
    group = get_object_or_404(Group, slug=slug)
    
    if not group.can_invite(request.user):
        raise Http404()
    
    form = GroupInviteForm(request.POST)
    
    if form.is_valid():
        for user in form.cleaned_data["users"]:
            group.invite(user, request.user, role=form.cleaned_data["role"])
    
    return redirect("group_members", slug=group.slug)


@login_required
def group_invite_response(request, token):
    invite = get_object_or_404(GroupInvitation, token=token)
    
    if request.method == "POST":
        if "accept" in request.POST:
            invite.accept(request.user)
        
        if "decline" in request.POST:
            invite.decline()
        
        return redirect("group_detail", slug=invite.group.slug)
    else:
        return render_to_response("groups/group_invite_response.html")


@login_required
def group_add_layers(request, slug):
    group = get_object_or_404(Group, slug=slug)
    
    ctx = {}
    if request.method == "POST":
        form = AddGroupLayerForm(request.POST)
        
        if form.is_valid():
            ctx["layers_added"] = []
            for l in form.cleaned_data["layers"]:
                GroupLayer.objects.get_or_create(layer=l, group=group)
                ctx["layers_added"].append(l.title)
    else:
        layers = Layer.objects.filter(owner=request.user)
        form = AddGroupLayerForm()
        form.fields["layers"].queryset = layers
        
    ctx["form"] = form
    ctx.update({
        "object": group,
        "members": group.member_queryset(),
        "is_member": group.user_is_member(request.user),
        "is_manager": group.user_is_role(request.user, "manager"),
    })
    ctx = RequestContext(request, ctx)
    return render_to_response("groups/group_add_layers.html", ctx)


@login_required
def group_add_maps(request, slug):
    group = get_object_or_404(Group, slug=slug)
    
    ctx = {}
    if request.method == "POST":
        form = AddGroupMapForm(request.POST)
        
        if form.is_valid():
            ctx["maps_added"] = []
            for m in form.cleaned_data["maps"]:
                GroupMap.objects.get_or_create(map=m, group=group)
                ctx["maps_added"].append(m.title)
    else:
        maps = Map.objects.filter(owner=request.user)
        maps.exclude
        form = AddGroupMapForm()
        form.fields["maps"].queryset = maps
        
    ctx["form"] = form
    ctx.update({
        "object": group,
        "members": group.member_queryset(),
        "is_member": group.user_is_member(request.user),
        "is_manager": group.user_is_role(request.user, "manager"),
    })
    ctx = RequestContext(request, ctx)
    return render_to_response("groups/group_add_maps.html", ctx)
