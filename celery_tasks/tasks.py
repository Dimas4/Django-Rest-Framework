import pendulum

from django.core.cache import cache
from django.db.models import Sum

from api.models import Salary
from .celery_app import app


@app.task
def add_to_salary_cached(id):
    qs = Salary.objects.filter(company_employee__employee__id=id) \
        .filter(month__gte=pendulum.now().subtract(years=1)) \
        .aggregate(salary=Sum('salary'))
    print(qs['salary'])
    cache.set(id, qs['salary'])
    print(cache.get(id))
    print(cache.get(id))
    print(cache.get(id))
