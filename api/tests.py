import random

from dateutil.relativedelta import relativedelta
from datetime import datetime

from django.test import TestCase

from api.models import Person, Company, CompanyEmployee, Salary, SalaryCache


class AnimalTestCase(TestCase):
    def setUp(self):
        ivan = Person.objects.create(first_name="Ivan", second_name="Ivan")
        andrey = Person.objects.create(first_name="Andrey", second_name="Andrey")

        itechart = Company.objects.create(name='iTechArt', description='iTechArt is ...')

        ivan_work_start_dt = datetime.strptime("2018-08-01", '%Y-%m-%d')
        itechart_ivan = CompanyEmployee.objects.create(company=itechart, employee=ivan,
                                                       work_start_dt=ivan_work_start_dt)

        andrey_work_start_dt = datetime.strptime("2016-05-07", '%Y-%m-%d')
        itechart_andrey = CompanyEmployee.objects.create(company=itechart, employee=andrey,
                                                         work_start_dt=andrey_work_start_dt)

        date = ivan_work_start_dt
        while date <= datetime.now():
            Salary.objects.create(company_employee=itechart_ivan, salary=random.randint(100, 150),
                                  date=date)
            date += relativedelta(months=1)

        date = andrey_work_start_dt
        c = 1
        while date <= datetime.now():
            c += 1
            Salary.objects.create(company_employee=itechart_andrey, salary=random.randint(400, 450),
                                  date=date)
            date += relativedelta(months=1)
