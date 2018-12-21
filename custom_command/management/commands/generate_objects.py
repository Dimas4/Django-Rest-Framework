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
        _company_count = options.get('company_count')
        _employees_count = options.get('employees_count')
        _max_employees_count = options.get('max_employees_count')
        min_employees_count = options.get('min_employees_count')
        try:
            Validate.validate(_company_count, _employees_count)
        except ValueError:
            return f'Fields {self.fields} must be defined'

        _company_count = _company_count[0]
        _employees_count = _employees_count[0]

        _max_employees_count = None if _max_employees_count is None else _max_employees_count[0]
        _min_employees_count = None if min_employees_count is None else min_employees_count[0]

        _companies = Factory.generate_objects(_company_count, CompanyFactory)
        _employees = Factory.generate_objects(_employees_count, PersonFactory)

        try:
            _companies_employees, _error = Factory.generate_companies_employees(
                _employees_count,
                _companies,
                _employees,
                _min_employees_count if _min_employees_count else 0,
                _max_employees_count if _max_employees_count else _employees_count,

            )
        except ValueError:
            print('Invalid limits values!')
            exit()

        if _error:
            print(f'Invalid maximum limit! Returns only '
                  f'{len(_companies_employees)} elements')

        Factory.generate_salary(_employees_count, 24, _companies_employees)

    def add_arguments(self, parser):
        """
        Adds new arguments to the command

        :param parser: django.core.management.base.CommandParser object
        :return: None
        """
        parser.add_argument('-c_c', '--company_count', nargs='+', type=int)
        parser.add_argument('-e_c', '--employees_count', nargs='+', type=int)
        parser.add_argument(
            '-mx_e_c',
            '--max_employees_count',
            nargs='+',
            type=int
        )
        parser.add_argument(
            '-mn_e_c',
            '--min_employees_count',
            nargs='+',
            type=int
        )
