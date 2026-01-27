from django.contrib import admin
from authentication.models import User, State, Township, Location, Employer, Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user__email', 'employee_name','is_active',)
    search_fields = ('user__email', 'employee_name',)
    list_editable = ("is_active",)

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('user__email', 'company_name','is_active',)
    search_fields = ('user__email', 'company_name',)
    list_editable = ("is_active",)
admin.site.register(User)

admin.site.register(State)
admin.site.register(Township)
admin.site.register(Location)

admin.site.register(Employer, EmployerAdmin)
admin.site.register(Employee, EmployeeAdmin)


