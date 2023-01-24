from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Note


class NoteView(DetailView):
    model = Note
    queryset = Note.objects.filter().order_by('-id')
    template_name = 'noteapp/note.html'
    context_object_name = 'note'
    # pk_url_kwarg = 'note_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def notes_plug(request):
    return HttpResponse("Notes")
