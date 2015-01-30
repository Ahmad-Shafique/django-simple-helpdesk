# -*- encoding: utf-8 -*-
from django.conf import settings

HELPDESK_DEFAULTS = {
    'username': None,
    'password': None,
    'from_email': settings.DEFAULT_FROM_EMAIL,
}

SETTINGS = HELPDESK_DEFAULTS.copy()
SETTINGS.update(getattr(settings, 'HELPDESK', {}))


class Filter(object):
    def __init__(self, request):
        super(Filter, self).__init__()
        self.request = request

    def save(self, key, value):
        self.request.session[key] = value

    def delete(self, key):
        try:
            del self.request.session[key]
        except KeyError:
            pass

    def by_assignee(self, value):
        if value not in ['me', 'all']:
            value = 'me'
        self.save('assignee', value)

    def by_state(self, value):
        if value is None:
            value = 'all'
        else:
            value = value.machine_name
        self.save('state', value)

    def by_project(self, value):
        if value is None:
            value = 'all'
        else:
            value = value.machine_name
        self.save('project', value)

    def get_form_init(self):
        init = {
            'assignee': self.request.session.get('assignee', 'all'),
            'state': self.request.session.get('state', 'all'),
            'project': self.request.session.get('project', 'all')
        }
        return init

    def get_filters(self):
        filters = {}
        assignee = self.request.session.get('assignee', 'all')
        if not self.request.user.has_perm('helpdesk.view_all_tickets'):
            assignee = 'me'
        if assignee == 'me':
            filters['assignee'] = self.request.user

        state = self.request.session.get('state', 'all')
        if state != 'all':
            filters['state__machine_name'] = state

        project = self.request.session.get('project', 'all')
        if project != 'all':
            filters['project__machine_name'] = project

        return filters