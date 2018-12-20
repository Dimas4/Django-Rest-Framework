import random

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from factory_boy.factory_utils import generate_objects
from factory_boy.factory_model import (
    CompanyEmployeeFactory,
    CompanyFactory,
    PersonFactory,
    SalaryFactory
)
from .exception import NoneValueError
from .validate import Validate
from .date import Date


def generate_salary(count, coef, companies_employees):
    for _ in range(count * coef):
        company_employee = random.choice(companies_employees)

        current_date = Date.random_date_from_obj(
            company_employee.work_start_dt,
            company_employee.work_end_dt
        )
        current_date = Date.convert_to_first_day(current_date)

        try:
            generate_objects(
                None,
                SalaryFactory,
                many=False,
                company_employee=company_employee,
                salary=random.randint(300, 3000),
                date=current_date)
        except IntegrityError:
            pass


def generate_company(count, companies, employees):
    return [generate_objects(None, CompanyEmployeeFactory,
                             many=False,
                             company=random.choice(companies),
                             supervisor=random.choice(employees),
                             employee=random.choice(employees),
                             ) for _ in range(count)]


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

        companies = generate_objects(company_count, CompanyFactory)
        employees = generate_objects(employees_count, PersonFactory)

        companies_employees = generate_company(
            employees_count,
            companies,
            employees
        )
        generate_salary(employees_count, 24, companies_employees)

    def add_arguments(self, parser):
        parser.add_argument('-c_c', '--company_count', nargs='+', type=int)
        parser.add_argument('-e_c', '--employees_count', nargs='+', type=int)
