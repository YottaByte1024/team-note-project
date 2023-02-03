from django import forms

from .models import Note, Team


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


class AddTeamForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.head_id = self.user.id
        self.instance.save()
        self.instance.members.add(self.user)
        return super().save(*args, **kwargs)

    class Meta:
        model = Team
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'})
        }
