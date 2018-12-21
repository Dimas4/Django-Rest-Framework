import factory
from faker import Faker
from datetime import date
import random
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DRF.settings")
django.setup()
from factory_boy.factory_model import CompanyEmployeeFactory
from api.models import Salary


class SalaryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Salary

    company_employee = factory.SubFactory(CompanyEmployeeFactory)

    salary = factory.Faker('pyint')
    date = factory.Faker('date_between', start_date="-5y", end_date="today")

