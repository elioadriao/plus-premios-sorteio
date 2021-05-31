from django.contrib import admin

from .models import Raffle, Quota, QuotaOrder


admin.site.register(Raffle)
admin.site.register(Quota)
admin.site.register(QuotaOrder)
