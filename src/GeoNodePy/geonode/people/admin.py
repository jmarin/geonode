from django.contrib import admin


class PeopleGroupMemberInline(admin.TabularInline):
    model = models.PeopleGroupMember


admin.site.register(models.PeopleGroup,
    inlines = [
        PeopleGroupMemberInline
    ]
)
