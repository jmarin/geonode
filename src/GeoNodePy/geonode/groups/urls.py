from django.conf.urls.defaults import *


urlpatterns = patterns('geonode.groups.views',
    url(r'^$', 'group_list', name="group_list"),
    url(r'^create/$', 'group_create', name="group_create"),
    url(r'^group/(?P<slug>[-\w]+)/$', 'group_detail', name='group_detail'),
    url(r'^group/(?P<slug>[-\w]+)/update/$', 'group_update', name='group_update'),
    url(r'^group/(?P<slug>[-\w]+)/members/$', 'group_members', name='group_members'),
    url(r'^group/(?P<slug>[-\w]+)/invite/$', 'group_invite', name='group_invite'),
    url(r'^group/[-\w]+/invite/(?P<token>[\w]{40})/$', 'group_invite_response', name='group_invite_response'),
)
