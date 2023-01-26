from django import template

register = template.Library()


@register.inclusion_tag('noteapp/navmenu.html')
def show_navmenu(current_path=None):
    nav_menu = [
        # {'title': "Home", 'url_name': 'home'},
        {'title': "Notes", 'url_name': 'note-list-view'},
        {'title': "Teams", 'url_name': 'note-list-view'},
        # {'title': "Register", 'url_name': 'register'},
        # {'title': "Login", 'url_name': 'login'},
    ]
    return {'nav_menu': nav_menu, 'current_path': current_path}
