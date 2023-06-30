from django.contrib import admin

# Register your models here.
from .models import User, Vehicle, Request, Shared, Vehicle_Type

admin.site.register(User)
admin.site.register(Vehicle)
admin.site.register(Request)
admin.site.register(Shared)
admin.site.register(Vehicle_Type)