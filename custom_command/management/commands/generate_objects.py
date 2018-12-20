import random

from django.core.management.base import BaseCommand

from factory_boy.factory_model import (
    CompanyEmployeeFactory,
    PersonFactory,
    CompanyFactory
)
from .exception import NoneValueError, LengthObjectError
from .validate import Validate


class Command(BaseCommand):
    help = 'To clear the database and create new database objects'
    fields = ['company_count', 'employees_count']

    def handle(self, *args, **options):
        company_count = options.get('company_count')
        employees_count = options.get('employees_count')
        try:
            Validate.validate(company_count, employees_count, list, [1, 1])
        except NoneValueError:
            return f'Fields {self.fields} must be defined'
        except LengthObjectError:
            return f'Fields {self.fields} must be a single integer'
        except TypeError:
            return f'Fields {self.fields} must be integer type'

        company_count = company_count[0]
        employees_count = employees_count[0]

        companies = CompanyFactory.create_batch(company_count)
        employees = PersonFactory.create_batch(employees_count)
        CompanyEmployeeFactory.create_batch(
            employees_count,
            company=random.choice(companies),
            supervisor=random.choice(employees),
            employee=random.choice(employees),
        )

    def add_arguments(self, parser):
        parser.add_argument('-c_c', '--company_count', nargs='+', type=int)
        parser.add_argument('-e_c', '--employees_count', nargs='+', type=int)
