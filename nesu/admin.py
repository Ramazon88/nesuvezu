from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import Customusercreate, Customusercreates
from .models import *
from rangefilter.filters import DateRangeFilter
from import_export.admin import ImportExportModelAdmin

from .resources import OrderResource


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ["id", "admin_id", "name_model"]


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    list_display = ["id", "partner", "datetime", "done_time", "type_delever", "multiorder",
                    "name_model", "kuryer", "status", "dis_comment"]
    list_editable = ["dis_comment"]
    list_display_links = ["id", "done_time", "type_delever", "name_model", "kuryer"]
    exclude = ["step", "multiorder", "parent_delevery", "after_image", "before_image", "api", "delete_message_id",
               "shop_came", "b1", "b2", "b3", "comis"]
    list_filter = (("datetime", DateRangeFilter), "partner", "type_delever", "kuryer", "status")
    search_fields = ["partner", "datetime", "type_delever", "name_model", "kuryer", "status"]
    resource_class = OrderResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.username == "adminnesuvezu":
            return qs
        return qs.filter(partner=request.user.partner.partner)

    def less_content(self, obj):
        return obj.content[50]


@admin.register(Message)
class CustomuserAdmin(admin.ModelAdmin):
    fields = ("short_disc", "message", "image", ("operator", "dispatcher", "kuryer"))


@admin.register(Customuser)
class MessageAdmin(UserAdmin):
    UserAdmin.fieldsets += (
        (None, {"fields": ("partner", "telegram_id")}),
    )


admin.site.unregister(Group)
admin.site.register(Kuryer_step)


@admin.register(Pay_partner)
class Pay_partnerAdmin(admin.ModelAdmin):
    list_display = ["partner", "datetime", "datetime_apply", "total_a", "total_1", "total_2", "total_3", "total", "price"]
    list_editable = ["datetime", "datetime_apply"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.username == "adminnesuvezu":
            return qs
        return qs.filter(partner=request.user.partner)



@admin.register(Pay_kuryer)
class Pay_kuryerAdmin(admin.ModelAdmin):
    list_display = ["kuryer", "datetime", "datetime_apply", "total_a", "total_1", "total_2", "total_3", "average_time", "total", "price"]
    list_editable = ["datetime", "datetime_apply"]
