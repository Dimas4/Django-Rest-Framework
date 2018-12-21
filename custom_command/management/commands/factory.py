import random

from django.db.utils import IntegrityError

from factory_boy.factory_model import SalaryFactory
from .date import Date


class Factory:
    @classmethod
    def _generate(cls, count, obj_class, many=True, **kwargs):
        """
        Creates multiple or a single object(s) (obj type) with kwargs params

        :param count: objects count
        :param obj_class: new object class. E.g.: CompanyFactory
        :param many: to create multiple or a single object(s)
        :param kwargs: new object parameters
        :return: list of objects or one
        """
        if many:
            return [obj_class(**kwargs) for _ in range(count)]
        return obj_class(**kwargs)

    @classmethod
    def generate_objects(cls, count, obj_class, **kwargs):
        """
        Wrapper over the _generate method

        :param count: equal to the _generate method count attribute
        :param obj_class: equal to the _generate method obj_class attribute
        :param kwargs: equal to the _generate method kwargs(and many) attributes
        :return: equal to the return value of the _generate method
        """
        return cls._generate(count, obj_class, **kwargs)

    @classmethod
    def generate_companies_employees(
            cls,
            count,
            obj_class,
            companies,
            employees):
        """
        Complex method of creating CompanyEmployeeFactory objects

        :param count: objects count
        :param obj_class: new object class. E.g.: CompanyFactory
        :param companies: list of companies (select a random value
                                             for all iterations)
        :param employees: list of employees (select a random value
                                             for all iterations)
        :return: list()
                 type(list[0]) -> CompanyEmployee object
        """
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
            coefficient,
            companies_employees,
            salary=(300, 3000)):
        """
        Complex method of creating SalaryFactory objects

        :param count: objects count
        :param coefficient: the ratio for the iterations of the loop
        iterations count = count*coefficient
        :param companies_employees: list of companies_employees
        (select a random value for all iterations)
        :param salary: tuple with min/max salary
        :return:
        """
        for _ in range(count * coefficient):
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
