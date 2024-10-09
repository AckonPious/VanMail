from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(MailBox)
admin.site.register(AssignedTo)
admin.site.register(Mail)