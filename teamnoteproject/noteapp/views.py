from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AddNoteForm, AddTeamForm

from .models import Note, Team
from .permissions import MemberPermissionsMixin, NoteMemberPermissionsMixin, NotesListMemberPermissionsMixin, UserPagePermissionsMixin


class NoteDetailView(NoteMemberPermissionsMixin, DetailView):
    model = Note
    # queryset = Note.objects.filter().order_by('-id')
    template_name = 'noteapp/note.html'
    context_object_name = 'note'
    # pk_url_kwarg = 'note_id'

    def get_queryset(self):
        team_url = self.kwargs['team_id']
        return Note.objects.filter(team_id=team_url).order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TeamNotesListView(NotesListMemberPermissionsMixin, ListView):
    paginate_by = 20
    model = Note
    template_name = 'noteapp/team_notes.html'
    context_object_name = 'notes'
    
    def get_queryset(self):
        team_url = self.kwargs['team_id']
        if self.request.user in Team.objects.filter(id=team_url).first().members.all():
            return Note.objects.filter(team_id=team_url).order_by('-date_change')
        else:
            return Note.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_id'] = self.kwargs['team_id']
        return context


class UserTeamsDetailView(DetailView):
    model = User
    template_name = 'noteapp/team_list.html'
    context_object_name = 'user'
    # pk_url_kwarg = 'note_id'

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TeamNotesDetailView(MemberPermissionsMixin, DetailView):
    """Dead DetailView"""
    model = Team
    queryset = Team.objects.filter()
    template_name = 'noteapp/team_notes.html'
    context_object_name = 'team'
    pk_url_kwarg = 'team_id'
    

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserDetailView(UserPagePermissionsMixin, DetailView):
    model = User
    template_name = 'noteapp/user.html'
    context_object_name = 'user'

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TeamNoteCreateView(MemberPermissionsMixin, CreateView):
    model = Team
    pk_url_kwarg = 'team_id'
    form_class = AddNoteForm
    template_name = 'noteapp/add_note.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        local_query = Team.objects.filter(
            id=self.kwargs['team_id']).first().members.all()
        kwargs.update({
            'team_id': self.kwargs['team_id']
            if self.request.user in local_query else None,
        })
        return kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add note"
        context['heading'] = "Note creating"
        context['buttondone'] = "Add"
        return context


class TeamNoteUpdateView(NoteMemberPermissionsMixin, UpdateView):
    model = Note
    form_class = AddNoteForm
    template_name = 'noteapp/add_note.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        local_query = Team.objects.filter(
            id=self.kwargs['team_id']).first().members.all()
        kwargs.update({
            'team_id': self.kwargs['team_id']
            if self.request.user in local_query else None,
        })
        return kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update note"
        context['heading'] = "Note"
        context['buttondone'] = "Update"
        return context


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    # pk_url_kwarg = 'team_id'
    form_class = AddTeamForm
    template_name = 'noteapp/add_team.html'
    login_url = reverse_lazy('note-list-view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        local_query = User.objects.filter(id=self.kwargs['pk']).first()
        kwargs.update({
            'user': self.request.user
            if self.request.user == local_query else None,
        })
        return kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create team"
        context['heading'] = "Team creating"
        context['buttondone'] = "Create"
        return context


def notes_plug(request):
    return HttpResponse("Notes")
