from django.core.management.base import BaseCommand

from factory_boy.factory_model import (
    CompanyEmployeeFactory,
    CompanyFactory,
    PersonFactory,
)
from .exception import NoneValueError
from .generate import Generate
from .validate import Validate


class Command(BaseCommand):
    help = 'To clear the database and create new database objects'
    fields = ['company_count', 'employees_count']

    def handle(self, *args, **options):
        company_count = options.get('company_count')
        employees_count = options.get('employees_count')
        try:
            Validate.validate(company_count, employees_count)
        except NoneValueError:
            return f'Fields {self.fields} must be defined'

        company_count = company_count[0]
        employees_count = employees_count[0]

        companies = Generate.generate_objects(company_count, CompanyFactory)
        employees = Generate.generate_objects(employees_count, PersonFactory)

        companies_employees = Generate.generate_companies_employees(
            employees_count,
            CompanyEmployeeFactory,
            companies,
            employees
        )
        Generate.generate_salary(employees_count, 24, companies_employees)

    def add_arguments(self, parser):
        parser.add_argument('-c_c', '--company_count', nargs='+', type=int)
        parser.add_argument('-e_c', '--employees_count', nargs='+', type=int)
