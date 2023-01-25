from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.notes_plug, name='note-list-view'),
    path('<uuid:team_id>/notes/',
         views.TeamNotesListView.as_view(), name='teamnotes-list-view'),
    path('<uuid:team_id>/<uuid:pk>/',
         views.NoteDetailView.as_view(), name='note-detail-view'),

]