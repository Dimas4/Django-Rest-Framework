from django.urls import reverse
from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)

    created_on = models.DateTimeField(auto_now_add=True)

    def get_annual_salary_url(self):
        return reverse("salary", kwargs={'id': self.id})

    def __str__(self):
        return f"<Employee(name={self.first_name} {self.second_name})>"


class Company(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)

    def employee_url(self):
        return reverse("admin:api_companyemployee_changelist") + f'?q={self.id}'

    def __str__(self):
        return f"<Company(name={self.name})>"


class CompanyEmployee(models.Model):
    company = models.ForeignKey(Company, related_name='company_employee', on_delete=models.CASCADE)
    employee = models.ForeignKey(Person, on_delete=models.CASCADE)

    work_start_dt = models.DateField(auto_now_add=False, auto_now=False)
    work_end_dt = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)

    def __str__(self):
        return f"<CompanyEmployee id={self.id}>"


class Salary(models.Model):
    company_employee = models.ForeignKey(CompanyEmployee, on_delete=models.CASCADE)

    salary = models.PositiveSmallIntegerField()
    month = models.DateField()

    def __str__(self):
        return f"<Salary salary={self.salary} month={self.month}>"
