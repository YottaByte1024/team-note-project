from django.db import models
from django.urls import reverse


class Note(models.Model):
    name = models.CharField(max_length=128, default="No name")
    # path = models.CharField(max_length=256, default="/")
    text = models.TextField(default="")
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('note-detail-view', args=[str(self.id)])


class Team(models.Model):
    name = models.CharField(max_length=256)
    # head = models.ForeignKey()

