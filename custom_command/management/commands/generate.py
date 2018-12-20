import random

from django.db.utils import IntegrityError

from factory_boy.factory_utils import generate_objects
from factory_boy.factory_model import SalaryFactory
from .date import Date


class Generate:
    @classmethod
    def generate_objects(cls, count, obj_class):
        return generate_objects(count, obj_class)

    @classmethod
    def generate_companies_employees(
            cls,
            count,
            obj_class,
            companies,
            employees):
        return [generate_objects(None, obj_class,
                                 many=False,
                                 company=random.choice(companies),
                                 supervisor=random.choice(employees),
                                 employee=random.choice(employees),
                                 ) for _ in range(count)]

    @classmethod
    def generate_salary(cls, count, coef, companies_employees):
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
