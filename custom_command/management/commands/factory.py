import random

from django.db.utils import IntegrityError

from factory_boy.factory_model import SalaryFactory
from .date import Date


class Factory:
    @classmethod
    def _generate(cls, count, obj, many=True, **kwargs):
        if many:
            return [obj(**kwargs) for _ in range(count)]
        return obj(**kwargs)

    @classmethod
    def generate_objects(cls, count, obj_class, **kwargs):
        return cls._generate(count, obj_class, **kwargs)

    @classmethod
    def generate_companies_employees(
            cls,
            count,
            obj_class,
            companies,
            employees):
        return [cls.generate_objects(None, obj_class,
                                     many=False,
                                     company=random.choice(companies),
                                     supervisor=random.choice(employees),
                                     employee=random.choice(employees),
                                     ) for _ in range(count)]

    @classmethod
    def generate_salary(
            cls,
            count,
            coef,
            companies_employees,
            salary=(300, 3000)):
        for _ in range(count * coef):
            _company_employee = random.choice(companies_employees)

            _current_date = Date.random_date_from_obj(
                _company_employee.work_start_dt,
                _company_employee.work_end_dt
            )
            _current_date = Date.convert_to_first_day(_current_date)

            try:
                cls.generate_objects(
                    None,
                    SalaryFactory,
                    many=False,
                    company_employee=_company_employee,
                    salary=random.randint(*salary),
                    date=_current_date)
            except IntegrityError:
                pass
