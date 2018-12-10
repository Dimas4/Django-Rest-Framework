import random

from dateutil.relativedelta import relativedelta
from datetime import datetime

from django.test import TestCase, override_settings

from api.models import Person, Company, CompanyEmployee, Salary, SalaryCache
from celery_tasks.tasks import add_to_salary_cached


class AnimalTestCase(TestCase):
    def setUp(self):
        ivan = Person.objects.create(first_name="Ivan", second_name="Ivan")
        andrey = Person.objects.create(first_name="Andrey", second_name="Andrey")

        itechart = Company.objects.create(name='iTechArt', description='iTechArt is ...')

        ivan_work_start_dt = datetime.strptime("2018-08-01", '%Y-%m-%d')
        self.itechart_ivan = CompanyEmployee.objects.create(company=itechart, employee=ivan,
                                                            work_start_dt=ivan_work_start_dt)

        andrey_work_start_dt = datetime.strptime("2016-05-07", '%Y-%m-%d')
        self.itechart_andrey = CompanyEmployee.objects.create(company=itechart, employee=andrey,
                                                              work_start_dt=andrey_work_start_dt)

        date = ivan_work_start_dt
        self.ivan_annual_salary = 0
        while date <= datetime.now():
            salary = random.randint(100, 150)
            Salary.objects.create(company_employee=self.itechart_ivan, salary=salary, date=date)
            self.ivan_annual_salary += salary
            date += relativedelta(months=1)

        date = andrey_work_start_dt
        self.andrey_annual_salary = 0
        while date <= datetime.now():
            salary = random.randint(400, 450)
            Salary.objects.create(company_employee=self.itechart_andrey, salary=salary, date=date)
            self.andrey_annual_salary += salary
            date += relativedelta(months=1)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_salarycache(self):
        year = 2018
        add_to_salary_cached.delay(self.itechart_ivan.id, year)
        self.assertEqual(self.ivan_annual_salary,
                         SalaryCache.objects.get(company_employee=self.itechart_ivan, year=year).salary)
