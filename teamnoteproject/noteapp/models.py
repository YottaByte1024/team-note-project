import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, default="No name")
    # path = models.CharField(max_length=256, default="/")
    text = models.TextField(default="")
    archived = models.BooleanField(default=False)
    team = models.ForeignKey('Team', related_name='notes', on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    date_change = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('note-detail-view', args=[str(self.team_id), str(self.id)])

    class Meta:
        ordering = ['-date_change']


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    head = models.ForeignKey(User, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    date_change = models.DateTimeField(auto_now=True)

    members = models.ManyToManyField(User, related_name='teams')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('teamnotes-list-view', args=[str(self.id)])
    
    class Meta:
        ordering = ['name']
