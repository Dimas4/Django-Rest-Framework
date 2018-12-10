from django.db.models import Sum

from api.models import Salary, SalaryCache, CompanyEmployee
from .celery_app import app


@app.task
def add_to_salary_cached(company_employee_id, year):
    qs = Salary.objects.filter(company_employee__id=company_employee_id) \
        .filter(date__year=year) \
        .aggregate(salary=Sum('salary'))

    company_employee = CompanyEmployee.objects.get(id=company_employee_id)
    SalaryCache.objects.update_or_create(company_employee=company_employee, year=year,
                                         defaults={'salary': qs['salary']})
