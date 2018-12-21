from django.core.management.base import BaseCommand

from factory_boy.factory_model import (
    CompanyEmployeeFactory,
    CompanyFactory,
    PersonFactory,
)
from .factory import Factory
from .validate import Validate


class Command(BaseCommand):
    help = 'To clear the database and create new database objects'
    fields = ['company_count', 'employees_count']

    def handle(self, *args, **options):
        """
        Processes the generate_objects control command(fills the database with
        objects with random values)
        :param args: args attributes
        :param options: extra attributes
        :return: None
        """
        company_count = options.get('company_count')
        employees_count = options.get('employees_count')
        max_employees_count = options.get('max_employees_count')
        try:
            Validate.validate(company_count, employees_count)
        except ValueError:
            return f'Fields {self.fields} must be defined'

        company_count = company_count[0]
        employees_count = employees_count[0]
        max_employees_count = max_employees_count[0]

        companies = Factory.generate_objects(company_count, CompanyFactory)
        employees = Factory.generate_objects(employees_count, PersonFactory)

        companies_employees, error = Factory.generate_companies_employees(
            employees_count,
            CompanyEmployeeFactory,
            companies,
            employees,
            max_employees_count
        )

        if error:
            print(f'Invalid maximum limit! Returns only '
                  f'{len(companies_employees)} elements')

        Factory.generate_salary(employees_count, 24, companies_employees)

    def add_arguments(self, parser):
        """
        Adds new arguments to the command

        :param parser: django.core.management.base.CommandParser object
        :return: None
        """
        parser.add_argument('-c_c', '--company_count', nargs='+', type=int)
        parser.add_argument('-e_c', '--employees_count', nargs='+', type=int)
        parser.add_argument(
            '-m_e_c',
            '--max_employees_count',
            nargs='+',
            type=int
        )
