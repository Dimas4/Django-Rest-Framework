import random

from django.db.utils import IntegrityError

from factory_boy.factory_model import SalaryFactory, CompanyEmployeeFactory
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
            companies,
            employees,
            min_=0,
            max_=17):
        """
        Complex method of creating CompanyEmployeeFactory objects with max
        employees limit per company

        :param count: objects count
        :param obj_class: new object class. E.g.: CompanyFactory
        :param companies: list of companies (select a random value
                                             for all iterations)
        :param employees: list of employees (select a random value
                                             for all iterations)
        :param max_: max employees limit per company
        :param min_: min employees limit per company
        :return: tuple()
                 type(list[0]) -> list(CompanyEmployee object)
                 type(list[1]) -> bool. Indicates a restricted error
                                        False == error
        """
        if min_ >= max_:
            raise ValueError

        _companies_employees_count = {
            _company.name: [0, _company] for _company in companies
        }

        _companies_employees_list = []

        for _ in range(count):
            _min_max_validate_result = _break = False
            _while_iteration_count = 0

            while not _min_max_validate_result:
                _company = random.choice(companies)
                _company_name = _company.name
                _current_company_count = _companies_employees_count.get(
                    _company_name, 0
                )[0]
                _min_max_validate_result = cls.min_max_validate(
                    max_,
                    _current_company_count
                )
                _while_iteration_count += 1
                if _while_iteration_count > len(companies*2):
                    _break = True
                    break

            if _break:
                break

            _companies_employees_count[_company_name][0] += 1
            _companies_employees_list.append(cls.generate_objects(
                    None, CompanyEmployeeFactory,
                    many=False,
                    company=_company,
                    supervisor=random.choice(employees),
                    employee=random.choice(employees),
                )
            )

        if min_:
            cls.validate_min_employees_count(
                _companies_employees_count,
                _companies_employees_list,
                CompanyEmployeeFactory,
                employees,
                min_
            )

        if _break:
            return _companies_employees_list, True

        return _companies_employees_list, False

    @classmethod
    def validate_min_employees_count(
            cls,
            _companies_employees_count,
            _companies_employees_list,
            obj_class,
            employees,
            min_):
        for _company_name, value in _companies_employees_count.items():
            while _companies_employees_count[_company_name][0] < min_:
                _companies_employees_list.append(
                    cls.generate_objects(
                        None, obj_class,
                        many=False,
                        company=value[1],
                        supervisor=random.choice(employees),
                        employee=random.choice(employees),
                    )
                )
                _companies_employees_count[_company_name][0] += 1

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

    @classmethod
    def min_max_validate(cls, max_, count):
        """
        Checks that count < max_
        :param max_: int
        :param count: int
        :return: bool
        """
        if not count < max_:
            return False
        return True
