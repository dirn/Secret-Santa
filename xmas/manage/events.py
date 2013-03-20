"""Event-related management commands."""

import sys

from flask.ext.script import Command, prompt
from werkzeug.datastructures import MultiDict

from xmas.core import db
from xmas.forms import EventForm
from xmas.models import Event


class CreateEventCommand(Command):

    """Create an event."""

    def run(self):
        name = prompt('Name')
        slug = prompt('Slug', default='')
        begins = prompt('Begins on')
        ends = prompt('Ends on')
        active = prompt('Active? [Yn]', default='')
        number_of_recipients = prompt('Number of recipients')
        suggested_limit = prompt('Suggested limit', default='25')
        data = MultiDict({
            'name': name,
            'slug': slug,
            'begins': begins,
            'ends': ends,
            'active': active.lower() != 'n',
            'number_of_recipients': number_of_recipients,
            'suggested_limit': suggested_limit,
        })
        form = EventForm(data, csrf_enabled=False)
        if form.validate():
            event = Event(
                name=form.name.data,
                slug=form.slug.data,
                begins=form.begins.data,
                active=form.active.data,
                number_of_recipients=form.number_of_recipients.data,
                suggested_limit=form.suggested_limit.data,
            )
            db.session.add(event)
            db.session.commit()
            print('\nEvent created successfully.')
            print('Event(id={0.id} name={0.name} slug={0.slug})'.format(event))
            return
        print('\nError creating event:')
        for field, errors in form.errors.items():
            print('{}:'.format(field), '\n'.join(errors))
        sys.exit(1)
