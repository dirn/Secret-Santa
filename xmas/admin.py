# from datetime import date, datetime, time

# from bson import ObjectId
# from flask import redirect, request, url_for
# from flask.ext.admin import Admin, AdminIndexView, expose
# from flask.ext.admin.model import BaseModelView
# from flask.ext.login import current_user

# from . import app
# from . import forms
# from .models import Event, User


# def date_formatter(context, model, name):
#     return getattr(model, name).strftime('%b %d, %Y')


# class AdminPermissionMixin(object):
#     def is_accessible(self):
#         return current_user.is_admin()


# class AdminIndex(AdminPermissionMixin, AdminIndexView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/index.html')


# class AdminModelView(AdminPermissionMixin, BaseModelView):
#     create_template = 'xmas/admin/model/create.html'
#     edit_template = 'xmas/admin/model/edit.html'

#     column_list = ('name',)

#     def create_model(self, form):
#         item = self.model.create(**form.data)
#         return 'id' in item

#     def delete_model(self, model):
#         model.delete()
#         return True

#     def get_one(self, id):
#         try:
#             model = self.model.get(id=id)
#         except self.model.NoDocumentFound:
#             return None
#         else:
#             return model

#     def get_list(self, page, sort_field, sort_desc, search, filters):
#         things = self.model.all()
#         if sort_field:
#             if sort_desc:
#                 sort_field = '-' + sort_field
#             things = things.sort(sort_field)
#         items = things.limit(self.page_size)
#         if page:
#             items = items.skip((page - 1) * self.page_size)

#         return things.count(), items

#     def get_pk_value(self, model):
#         return getattr(model, 'id')

#     def scaffold_form(self):
#         return getattr(forms, '{}Form'.format(self.model.__name__))

#     def scaffold_list_columns(self):
#         return self.column_list

#     def scaffold_sortable_columns(self):
#         return ('name',)

#     def update_model(self, form, model):
#         model.update(**form.data)
#         return True


# class EventAdminModelView(AdminModelView):
#     column_formatters = {
#         'begins': date_formatter,
#         'ends': date_formatter,
#     }
#     column_labels = {
#         'number_of_recipients': 'Number of Recipients',
#     }
#     column_list = ('name', 'number_of_recipients', 'begins', 'ends', 'active')

#     list_template = 'xmas/admin/model/event/list.html'

#     @expose('/assign/', methods=('GET', 'POST'))
#     def assign_recipients(self):
#         return_url = request.args.get('url') or url_for('.index_view')

#         if not self.can_edit:
#             return redirect(return_url)

#         id = request.args.get('id')
#         if id is None:
#             return redirect(return_url)

#         model = self.get_one(id)

#         if model is None:
#             return redirect(return_url)

#         try:
#             model.assign_recipients()
#         except:
#             return redirect(url_for('.assign_recipients', id=id,
#                                     url=return_url))
#         else:
#             return redirect(return_url)

#     def create_model(self, form):
#         return self._create_or_update(form, self.model())

#     def _create_or_update(self, form, model):
#         for k, v in form.data.items():
#             if k == 'users':
#                 v = [ObjectId(x) for x in v]
#             elif isinstance(v, date) and not isinstance(v, datetime):
#                 v = datetime.combine(v, time())
#             setattr(model, k, v)

#         model.save(safe=True)

#         return True

#     @expose('/lock/', methods=('GET', 'POST'))
#     def lock(self):
#         return_url = request.args.get('url') or url_for('.index_view')

#         if not self.can_edit:
#             return redirect(return_url)

#         id = request.args.get('id')
#         if id is None:
#             return redirect(return_url)

#         model = self.get_one(id)

#         if model is None:
#             return redirect(return_url)

#         model.lock()

#         return redirect(return_url)

#     def scaffold_sortable_columns(self):
#         return ('name', 'begins', 'ends',)

#     def update_model(self, form, model):
#         return self._create_or_update(form, model)


# class UserAdminModelView(AdminModelView):
#     column_list = ('name', 'email')

#     def _create_or_update(self, form, model):
#         data = form.data.copy()
#         password = data.pop('password', None)
#         data.pop('confirm_password')

#         for k, v in data.teritems():
#             setattr(model, k, v)
#         if password:
#             model.set_password(str(password))

#         model.save(safe=True)

#         return True

#     def create_model(self, form):
#         return self._create_or_update(form, self.model())

#     def update_model(self, form, model):
#         return self._create_or_update(form, model)


# admin = Admin(app, name='Secret Santa Admin', index_view=AdminIndex())
# admin.add_view(EventAdminModelView(Event, name='Events', endpoint='events'))
# admin.add_view(UserAdminModelView(User, name='Users', endpoint='users'))
