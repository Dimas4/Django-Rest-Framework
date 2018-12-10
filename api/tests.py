import random

from dateutil.relativedelta import relativedelta
from datetime import datetime

from django.test import TestCase, override_settings

from api.models import Person, Company, CompanyEmployee, Salary, SalaryCache
from celery_tasks.tasks import add_to_salary_cached


class AnimalTestCase(TestCase):
    def setUp(self):
        nikita = Person.objects.create(first_name="Nikita", second_name="Nikita")

        itechart = Company.objects.create(name='iTechArt', description='iTechArt is ...')

        nikita_work_start_dt = datetime.strptime("2016-05-05", '%Y-%m-%d')
        self.itechart_nikita = CompanyEmployee.objects.create(company=itechart, employee=nikita,
                                                              work_start_dt=nikita_work_start_dt)
        date = nikita_work_start_dt
        self.nikita_annual_salary = {}

        while date <= datetime.now():
            salary = random.randint(100, 150)
            Salary.objects.create(company_employee=self.itechart_nikita, salary=salary, date=date)
            self.nikita_annual_salary[date.year] = 0 if not self.nikita_annual_salary.get(date.year) \
                else self.nikita_annual_salary[date.year]
            self.nikita_annual_salary[date.year] += salary
            date += relativedelta(months=1)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_salarycache(self):
        for year, salary in self.nikita_annual_salary.items():
            add_to_salary_cached.delay(self.itechart_nikita.id, year)

        for year, salary in self.nikita_annual_salary.items():
            self.assertEqual(salary,
                             SalaryCache.objects.get(company_employee=self.itechart_nikita, year=year).salary)
