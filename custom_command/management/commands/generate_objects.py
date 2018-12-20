import random

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
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
            company_employee.end_dt
        )
        current_date = Date.convert_to_first_day(current_date)

        try:
            SalaryFactory(
                company_employee=company_employee,
                salary=random.randint(300, 3000),
                date=current_date
            )
        except IntegrityError:
            pass


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

        companies = CompanyFactory.create_batch(company_count)
        employees = PersonFactory.create_batch(employees_count)
        companies_employees = CompanyEmployeeFactory.create_batch(
            employees_count,
            company=random.choice(companies),
            supervisor=random .choice(employees),
            employee=random.choice(employees),
        )
        generate_salary(employees_count, 24, companies_employees)

    def add_arguments(self, parser):
        parser.add_argument('-c_c', '--company_count', nargs='+', type=int)
        parser.add_argument('-e_c', '--employees_count', nargs='+', type=int)
