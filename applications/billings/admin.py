from django.contrib import admin

from applications.billings.models import Billing, Settlement, BillingImage

admin.site.register([Billing, Settlement, BillingImage])
