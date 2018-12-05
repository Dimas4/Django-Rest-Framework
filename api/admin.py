from django.utils.html import format_html
from django.core.cache import cache
from django.contrib import admin

from .models import Company, Person, CompanyEmployee, Salary


class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    readonly_fields = ('show_employee_url',)

    def show_employee_url(self, obj):
        return format_html('<a href="%s">%s</a>' % (obj.employee_url(), obj.employee_url()))

    show_employee_url.allow_tags = True


class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ('second_name', 'first_name',)
    readonly_fields = ('show_annual_salary',)

    def show_annual_salary(self, obj):
        salary = cache.get(obj.id)

        if salary or salary == 0:
            return salary
        try:
            return format_html('Can\'t find any salary information for this person. '
                               'You can try again: <a href="%s">%s</a>' %
                               (obj.get_annual_salary_url(), obj.get_annual_salary_url()))
        except Exception as err:
            return ''
    show_annual_salary.allow_tags = True


class SalaryAdmin(admin.ModelAdmin):
    search_fields = ('year', 'month',)


class CompanyEmployeeAdmin(admin.ModelAdmin):
    search_fields = ('company__id',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Person, EmployeeAdmin)
admin.site.register(CompanyEmployee, CompanyEmployeeAdmin)
admin.site.register(Salary, SalaryAdmin)
