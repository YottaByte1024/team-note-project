from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.notes_plug, name='note-list-view'),
    path('note/<int:pk>/', views.NoteView.as_view(), name='note-detail-view')

]