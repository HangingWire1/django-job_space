from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    # 1. This string tells Django to look for a method with this name
    list_display = ('is_archived_by_user', 'get_employee_name', 'get_job_title', 'status','id')

    search_fields = ('employee__employee_name', 'job__title')
    list_filter = ('status',)

    # 2. Django finds this method because the name matches the string above.
    #    'obj' here is the Application instance for the current row.
    @admin.display(description='Employee')  # This sets the column header
    def get_employee_name(self, obj):
        return obj.employee.employee_name

    # Same principle for the job title
    @admin.display(description='Job Title')
    def get_job_title(self, obj):
        return obj.job.title

