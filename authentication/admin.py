from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.models import User, State, Township, Location, Employer, Employee

class LocationInline(admin.StackedInline):
    model = Location
    can_delete = False

class UserAdmin(UserAdmin):
    list_display = ('email','id')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user__email', 'employee_name','is_active',)
    search_fields = ('user__email', 'employee_name',)
    list_editable = ("is_active",)

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'company_name', 'is_active')
    search_fields = ('user__email', 'company_name')
    list_editable = ('is_active',)
    inlines = [LocationInline]

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'


admin.site.register(User,UserAdmin)
admin.site.register(State)
admin.site.register(Township)
admin.site.register(Location)

admin.site.register(Employer, EmployerAdmin)
admin.site.register(Employee, EmployeeAdmin)