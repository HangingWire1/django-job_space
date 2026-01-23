from django.contrib import admin
from authentication.models import User, State, Township, Location, Employer

admin.site.register(User)

admin.site.register(State)
admin.site.register(Township)
admin.site.register(Location)

admin.site.register(Employer)
