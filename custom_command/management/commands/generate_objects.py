import random

from django.core.management.base import BaseCommand

from factory_boy.factory_utils import generate_objects
from factory_boy.factory_model import (
    CompanyEmployeeFactory,
    PersonFactory,
    CompanyFactory
)


class Command(BaseCommand):
    help = 'To clear the database and create new database objects'

    def handle(self, *args, **options):
        company_count = 5
        employees_count = 20

        companies_employees = []
        companies = generate_objects(company_count, CompanyFactory)
        employees = generate_objects(employees_count, PersonFactory)

        for _ in range(employees_count):
            companies_employee = generate_objects(
                _,
                CompanyEmployeeFactory,
                company=random.choice(companies),
                supervisor=random.choice(employees),
                employee=random.choice(employees),
                many=False
            )
            companies_employees.append(companies_employee)

        # salary = SalaryFactory()

