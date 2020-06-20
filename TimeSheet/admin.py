from django.contrib import admin
from .models import Comments, Events


# Register your models here.

admin.site.register(Events)
admin.site.register(Comments)