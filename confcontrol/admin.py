from django.contrib import admin
from .models import *

admin.site.register(Dispatcher)
admin.site.register(Operator)
admin.site.register(Shop)
admin.site.register(Kuryer_group)
admin.site.register(Kuryer_came_group)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ["id", "a", "b1", "b2", "b3", "comis"]
    list_editable = ["a", "b1", "b2", "b3", "comis"]


@admin.register(Kuryer)
class KuryerAdmin(admin.ModelAdmin):
    list_display = ["kuryer_name", "inwork"]
    list_editable = ["inwork"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.exclude(kuryer_name="ИТОГО")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.exclude(partner="ИТОГО")
