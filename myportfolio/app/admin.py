from django.contrib import admin

from app.models import Contact, Instrument, Project, User

admin.site.register(Instrument)
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Contact)
