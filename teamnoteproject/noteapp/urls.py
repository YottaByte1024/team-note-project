from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.notes_plug, name='note-list-view'),
    path('<uuid:team_id>/',
         views.TeamNotesDetailView.as_view(), name='teamnotes-detail-view'),
    path('<uuid:team_id>/<uuid:pk>/',
         views.NoteDetailView.as_view(), name='note-detail-view'),

]