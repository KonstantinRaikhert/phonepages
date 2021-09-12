from django.contrib import admin
from django.contrib.auth.models import Group

from corporations.models import Employee, Firm, Phone, Profession


class PhoneInlineNumber(admin.TabularInline):
    model = Employee.phone.through
    min_num = 1
    extra = 0
    verbose_name = "Телефон"
    verbose_name_plural = "Телефоны"


class UserFirmRelationAdminInline(admin.TabularInline):
    model = Firm.access_edit.through
    extra = 0
    verbose_name_plural = "Пользователи с правами администратора"
    verbose_name = "Пользователь с правами администратора"


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "profession", "firm")
    list_filter = ("firm",)
    search_fields = (
        "first_name",
        "last_name",
        "middle_name",
        "profession",
        "firm",
    )
    exclude = ("phone",)
    inlines = [PhoneInlineNumber]

    def full_name(self, obj):
        return "{} {} {}".format(
            obj.first_name,
            obj.middle_name,
            obj.last_name,
        )


class FirmAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    search_fields = ("name", "address")

    inlines = [UserFirmRelationAdminInline]


class ProfessionAdmin(admin.ModelAdmin):
    list_display = ("id", "profession")


class PhoneNumber(admin.ModelAdmin):
    list_display = ("type", "phone_number")
    list_filter = ("type",)
    search_fields = ("phone_number",)


admin.site.unregister(Group)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Firm, FirmAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Phone, PhoneNumber)
