import pendulum

from django.db.models import Sum

from api.models import Person, Salary, SalaryCache
from .celery_app import app


@app.task
def add_to_salary_cached(id):
    qs = Salary.objects.filter(company_employee__employee__id=id) \
        .filter(month__gte=pendulum.now().subtract(years=1)) \
        .aggregate(salary=Sum('salary'))

    try:
        salary_cache = SalaryCache.objects.get(employee__id=id)
        salary_cache.delete()
    except SalaryCache.DoesNotExist:
        print('Does not exist')

    SalaryCache.objects.create(employee=Person.objects.get(id=id), salary=qs['salary'])
