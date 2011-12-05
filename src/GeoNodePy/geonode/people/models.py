import datetime
import itertools

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
    
    def member_queryset(self):
        return self.peoplegroupmember_set.all()
    
    def user_is_member(self, user):
        if not user.is_authenticated():
            return False
        return user.id in self.member_queryset().values_list("user", flat=True)
    
    def user_is_role(self, user, role):
        return self.member_queryset().filter(user=user, role=role).exists()
    
    def can_view(self, user):
        if self.access == "private":
            return user.is_authenticated() and self.user_is_member(user)
        else:
            return True
    
    def can_invite(self, user):
        if not user.is_authenticated():
            return False
        return self.user_is_role(user, "manager")
    
    def join(self, user, **kwargs):
        PeopleGroupMember(group=self, user=user, **kwargs).save()
    
    def invite(self, user, role="member", send=True):
        params = dict(role=role)
        if isinstance(user, User):
            params["user"] = user
            params["email"] = user.email
        else:
            params["email"] = user
        invitation = self.invitations.create(**params)
        if send:
            invitation.send()
        return invitation


class PeopleGroupMember(models.Model):
    
    group = models.ForeignKey(PeopleGroup)
    user = models.ForeignKey(User)
    role = models.CharField(max_length=10, choices=[
        ("manager", "Manager"),
        ("member", "Member"),
    ])
    joined = models.DateTimeField(default=datetime.datetime.now)


class PeopleGroupInvitation(models.Model):
    
    group = models.ForeignKey(PeopleGroup, related_name="invitations")
    email = models.EmailField()
    user = models.ForeignKey(User, null=True)
    role = models.CharField(max_length=10, choices=[
        ("manager", "Manager"),
        ("member", "Member"),
    ])
    state = models.CharField(
        max_length = 10,
        choices = zip(*itertools.tee([
            "sent",
            "accepted",
            "declined",
        ])),
        default = "sent",
    )
    created = models.DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        unique_together = [("group", "email")]
    
    def send(self):
        # send to self.email
        pass
    
    def accept(self, user):
        self.group.join(user, role=self.role)
        self.state = "accepted"
        self.user = user
        self.save()
    
    def decline(self):
        self.state = "declined"
        self.save()
