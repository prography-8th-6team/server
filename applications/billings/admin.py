from django.contrib import admin

from applications.billings.models import Billing, Settlement

admin.site.register([Billing, Settlement])
