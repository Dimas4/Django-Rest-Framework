from django.utils.html import format_html
from django.contrib import admin

from .models import Company, Person, CompanyEmployee, Salary, SalaryCache


class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    readonly_fields = ('show_employee_url',)

    def show_employee_url(self, obj):
        employee_url = obj.employee_url()
        return format_html(
            f'<a href={employee_url}>{employee_url}</a>'
        )

    show_employee_url.allow_tags = True


class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ('second_name', 'first_name',)


class SalaryAdmin(admin.ModelAdmin):
    search_fields = ('year', 'month',)


class CompanyEmployeeAdmin(admin.ModelAdmin):
    search_fields = ('company__id',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Person, EmployeeAdmin)
admin.site.register(CompanyEmployee, CompanyEmployeeAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(SalaryCache)
