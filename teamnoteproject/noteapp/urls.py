from django.urls import path
from . import views

urlpatterns = [
    path('notes/',
         views.notes_plug, name='note-list-view'),
    path('<int:pk>/',
         views.UserDetailView.as_view(), name='user-detail-view'),
    path('<int:pk>/create_team/',
         views.TeamCreateView.as_view(), name='team-create-view'),
    path('<int:pk>/teams/',
         views.UserTeamsDetailView.as_view(), name='userteams-detail-view'),
    path('<uuid:team_id>/',
         views.TeamNotesDetailView.as_view(), name='teamnotes-detail-view'),
    path('<uuid:team_id>/add_note/',
         views.TeamNoteCreateView.as_view(), name='teamnote-create-view'),
    path('<uuid:team_id>/<uuid:pk>/',
         views.NoteDetailView.as_view(), name='note-detail-view'),
    path('<uuid:team_id>/<uuid:pk>/update/',
         views.TeamNoteUpdateView.as_view(), name='note-update-view'),
]
