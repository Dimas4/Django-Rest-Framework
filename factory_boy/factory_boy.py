import random
import os

import factory
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DRF.settings")
django.setup()


from api.models import Person, Company, CompanyEmployee, Salary


def clear_database(*args):
    for model in args:
        model.objects.all().delete()


def generate_objects(count, obj, many=True, **kwargs):
    if many:
        return [obj(**kwargs) for _ in range(count)]
    return obj(**kwargs)


clear_database(Person, Company, CompanyEmployee, Salary)


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

    work_start_dt = factory.Faker('date')


class SalaryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Salary

    company_employee = factory.SubFactory(CompanyEmployeeFactory)

    salary = factory.Faker('pyint')
    date = factory.Faker('date_between', start_date="-5y", end_date="today")


company_count = 5
employees_count = 20

companies = generate_objects(company_count, CompanyFactory)
employees = generate_objects(employees_count, PersonFactory)

for _ in range(employees_count):
    companies_employees = generate_objects(
        _,
        CompanyEmployeeFactory,
        company=random.choice(companies),
        supervisor=random.choice(employees),
        employee=random.choice(employees),
        many=False
    )


# salary = SalaryFactory()
