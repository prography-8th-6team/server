from django.contrib import admin

# Register your models here.
from applications.travels.models import Travel, Member

admin.site.register(Travel)
admin.site.register(Member)
