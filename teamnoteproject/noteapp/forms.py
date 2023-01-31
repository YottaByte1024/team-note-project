from django import forms

from noteapp.models import Note


class AddNoteForm(forms.ModelForm):

    def __init__(self, team_id, *args, **kwargs):
        self.team_id = team_id
        super().__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.instance.team_id = self.team_id
        return super().save(*args, **kwargs)
    
    class Meta:
        model = Note
        fields = ('name', 'text')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'text': forms.Textarea(attrs={'class': 'form-textarea'})
        }