from django.db import models

from django.contrib.auth.models import User


class PeopleGroup(models.Model):
    
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    logo = models.FileField(upload_to="people_peoplegroup")
    description = models.TextField()
    access = models.CharField(max_length=15, choices=[
        ("public", "Public"),
        ("public-invite", "Public (invite-only)"),
        ("private", "Private"),
    ])


class PeopleGroupMember(models.Model):
    
    group = models.ForeignKey(PeopleGroup)
    user = models.ForeignKey(User)
    role = models.CharField(choices=[
        ("manager", "Manager"),
        ("member", "Member"),
    ])
