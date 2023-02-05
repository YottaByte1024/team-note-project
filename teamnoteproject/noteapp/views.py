from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AddMemberForm, AddNoteForm, AddTeamForm

from .models import Note, Team
from .permissions import MemberPermissionsMixin, NoteMemberPermissionsMixin, \
    NotesListMemberPermissionsMixin, UserPagePermissionsMixin


class NoteDetailView(NoteMemberPermissionsMixin, DetailView):
    """Show note"""
    model = Note
    template_name = 'noteapp/note.html'
    context_object_name = 'note'

    def get_queryset(self):
        team_url = self.kwargs['team_id']
        return Note.objects.filter(team_id=team_url).order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TeamNotesListView(NotesListMemberPermissionsMixin, ListView):
    """Show notes in team"""
    paginate_by = 20
    model = Note
    template_name = 'noteapp/team_notes.html'
    context_object_name = 'notes'

    def get_queryset(self):
        # show only those notes that are in the current team
        team_url = self.kwargs['team_id']
        if self.request.user in Team.objects.filter(id=team_url).first().members.all():
            return Note.objects.filter(team_id=team_url, archived=False).order_by('-date_change')
        else:
            return Note.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = Team.objects.filter(
            id=self.kwargs['team_id']).first()
        return context


class TeamArchivedNotesListView(TeamNotesListView):
    def get_queryset(self):
        # show only those notes that are in the current team
        team_url = self.kwargs['team_id']
        if self.request.user in Team.objects.filter(id=team_url).first().members.all():
            return Note.objects.filter(team_id=team_url, archived=True).order_by('-date_change')
        else:
            return Note.objects.none()


class UserTeamsDetailView(DetailView):
    """Show teams which available to user"""
    model = User
    template_name = 'noteapp/team_list.html'
    context_object_name = 'user'

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
    """Show user page"""
    model = User
    template_name = 'noteapp/user.html'
    context_object_name = 'user'

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TeamNoteCreateView(MemberPermissionsMixin, CreateView):
    """Create new note in current team"""
    model = Team
    pk_url_kwarg = 'team_id'
    form_class = AddNoteForm
    template_name = 'noteapp/add_note.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # add team_id to kwargs
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
    """Update current note"""
    model = Note
    form_class = AddNoteForm
    template_name = 'noteapp/add_note.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # add team_id to kwargs
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
    """Create new team"""
    model = Team
    form_class = AddTeamForm
    template_name = 'noteapp/add_team.html'
    login_url = reverse_lazy('note-list-view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # add user to kwargs
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


class OwnTeamsListView(ListView):
    model = Team
    template_name = 'noteapp/own_teams.html'
    context_object_name = 'teams'

    def get_queryset(self):
        return Team.objects.filter(head_id=self.request.user.id)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Own teams"
        return context


class NoteDeleteView(NoteMemberPermissionsMixin, DeleteView):
    model = Note
    
    def get_success_url(self):
         return reverse('teamnotes-list-view', kwargs={'team_id': self.kwargs['team_id']})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete note"
        context['heading'] = f"Delete note \"{context['object'].name}\"?"
        context['buttondone'] = "Delete"
        return context


class TeamDeleteView(MemberPermissionsMixin, DeleteView):
    model = Team
    pk_url_kwarg = 'team_id'
    
    def get_success_url(self):
         return reverse('userteams-detail-view', kwargs={'pk': self.request.user.id})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete team"
        context['heading'] = f"Delete team \"{context['object'].name}\"?"
        context['buttondone'] = "Delete"
        return context


class TeamAddMemberUpdateView(UpdateView):
    """Add member"""
    model = Team
    form_class = AddMemberForm
    template_name = 'noteapp/add_team.html'
    login_url = reverse_lazy('note-list-view')
    pk_url_kwarg = 'team_id'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "title"
        context['heading'] = "heading"
        context['buttondone'] = "Add"
        return context


def archive_note(request: HttpRequest, *args, **kwargs):
    note = get_object_or_404(Note, pk=kwargs['pk'])
    if not request.user.is_authenticated:
        raise Http404()
    if request.user in note.team.members.all():
        note.archived = not note.archived
        note.save()
    else:
        raise Http404()
    return redirect('note-detail-view', 
                    kwargs['team_id'],
                    kwargs['pk'])

def notes_plug(request):
    return HttpResponse("Notes")
