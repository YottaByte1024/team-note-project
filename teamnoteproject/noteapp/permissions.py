from django.http import Http404

from .models import Team


class MemberPermissionsMixin:
    def has_permissions(self):
        return self.request.user in self.get_object().members.all()

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class NoteMemberPermissionsMixin(MemberPermissionsMixin):
    def has_permissions(self):
        return self.request.user in self.get_object().team.members.all()


class UserPagePermissionsMixin(MemberPermissionsMixin):
    def has_permissions(self):
        return self.request.user == self.get_object()


class NotesListMemberPermissionsMixin(MemberPermissionsMixin):
    def has_permissions(self):
        members = Team.objects.filter(id=self.kwargs['team_id']).first().members.all()
        return self.request.user in members
