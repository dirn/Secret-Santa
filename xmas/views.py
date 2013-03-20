# from functools import wraps

# from flask import (abort, flash, redirect, render_template, request, session,
#                    url_for)
# from flask.ext.login import (current_user, login_required, login_user,
#                              logout_user)
# from flask.ext.simon import get_or_404
# import when

# from . import app
# from .forms import LoginForm, ProfileForm, RegisterForm
# from .models import Event, User, login_manager


# def guest_required(f):
#     @wraps(f)
#     def _inner(*args, **kwargs):
#         if current_user.is_authenticated():
#             return redirect(url_for('.index'))
#         return f(*args, **kwargs)
#     return _inner


# @app.route('/event/<string:slug>')
# @login_required
# def event(slug):
#     event = get_or_404(Event, slug=slug)

#     if current_user.id not in event.users:
#         abort(403)

#     if 'events' in current_user:
#         takers = current_user.events.get(str(event.id))['takers']
#         recipients = [User.get(id=id) for id in takers]

#     return render_template('events/index.html', event=event,
#                            recipients=recipients)


# @app.route('/')
# @login_required
# def index():
#     now = when.now(utc=True)
#     events = Event.find(users=current_user.id, active=True,
#                         begins__lte=now, ends__gt=now)

#     if len(events) == 1:
#         return redirect(url_for('.event', slug=events[0].slug))

#     return render_template('index.html', events=events)


# @app.route('/login/', methods=('GET', 'POST'))
# @guest_required
# def login():
#     form = LoginForm(request.form)
#     if form.validate_on_submit():
#         login_user(form.user)
#         return redirect(request.args.get('next') or url_for('.index'))
#     return render_template('login.html', form=form)


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('.index'))


# @app.route('/profile', methods=('GET', 'POST'))
# @login_required
# def profile():
#     form = ProfileForm(request.form, **current_user._document)
#     if form.validate_on_submit():
#         current_user.update(**form.data)
#         flash('Your profile has been updated.', 'success')
#         return redirect(url_for('.profile'))
#     return render_template('profile.html', form=form)


# @app.route('/register', methods=('GET', 'POST'))
# @guest_required
# def register():
#     form = RegisterForm(request.form)
#     if form.validate_on_submit():
#         user = User(**form.data)
#         user.set_password(str(form.password.data))
#         user.save()

#         login_user(user)

#         flash('Thank you for signing up.')
#         return redirect(request.args.get('next') or url_for('.index'))
#     return render_template('register.html', form=form)


# @app.route('/event/<string:slug>/wishlist')
# @login_required
# def wishlist(slug):
#     event = get_or_404(Event, slug=slug)

#     if current_user.id not in event.users:
#         abort(403)

#     return render_template('events/wishlist.html', event=event)


# @login_manager.unauthorized_handler
# def login_prompt():
#     session['login_redirect'] = request.path
#     return redirect(url_for('.login'))


# from .admin import *
