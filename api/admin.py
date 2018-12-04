from django.contrib import admin

from .models import Company, Person, CompanyEmployee, Salary, SalaryCache


class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ('second_name', 'first_name',)


class SalaryAdmin(admin.ModelAdmin):
    search_fields = ('year', 'month',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Person, EmployeeAdmin)
admin.site.register(CompanyEmployee)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(SalaryCache)
