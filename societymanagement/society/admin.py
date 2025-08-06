from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(MasterType)
admin.site.register(MasterValue)
admin.site.register(Complaint)