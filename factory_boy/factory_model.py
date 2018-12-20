import factory.fuzzy
import factory

from .factory_utils import (
    generate_date_or_none,
    clear_database,
)

from api.models import Person, Company, CompanyEmployee, Salary


clear_database(Person, Company, CompanyEmployee, Salary)
date_choice = generate_date_or_none()


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person

    first_name = factory.Faker('first_name')
    second_name = factory.Faker('last_name')


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker('company')
    description = factory.Faker('sentence')


class CompanyEmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CompanyEmployee

    company = factory.SubFactory(CompanyFactory)

    supervisor = factory.SubFactory(PersonFactory)
    employee = factory.SubFactory(PersonFactory)

    work_start_dt = factory.Faker(
        'date_between',
        start_date="-7y",
        end_date="-4y"
    )
    work_end_dt = factory.fuzzy.FuzzyChoice(date_choice)


class SalaryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Salary

    company_employee = factory.SubFactory(CompanyEmployeeFactory)

    salary = factory.Faker('pyint')
    date = factory.Faker('date_between', start_date="-4y", end_date="today")
