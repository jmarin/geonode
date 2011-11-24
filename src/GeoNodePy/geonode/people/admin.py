from django.contrib import admin

import geonode.people.models


class PeopleGroupMemberInline(admin.TabularInline):
    model = geonode.people.models.PeopleGroupMember


admin.site.register(geonode.people.models.PeopleGroup,
    inlines = [
        PeopleGroupMemberInline
    ]
)
