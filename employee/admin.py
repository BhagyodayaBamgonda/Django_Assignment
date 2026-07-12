from django.contrib import admin
from .models import Employee, Leave


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'employee_id',
        'name',
        'email',
        'department',
        'mobile_number',
        'date_of_joining'
    )

    search_fields = (
        'employee_id',
        'name'
    )


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'leave_type',
        'from_date',
        'to_date',
        'status'
    )

    list_filter = (
        'status',
        'leave_type'
    )