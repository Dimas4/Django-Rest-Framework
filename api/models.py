from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)

    created_on = models.DateTimeField(auto_now_add=True)

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
    company = models.ForeignKey(
        Company,
        related_name='company_employee',
        on_delete=models.CASCADE
    )
    employee = models.ForeignKey(Person, on_delete=models.CASCADE)

    work_start_dt = models.DateField(auto_now_add=False, auto_now=False)
    work_end_dt = models.DateField(
        auto_now_add=False,
        auto_now=False,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"<CompanyEmployee id={self.id}>"


class Salary(models.Model):
    company_employee = models.ForeignKey(
        CompanyEmployee,
        on_delete=models.CASCADE
    )

    salary = models.PositiveSmallIntegerField()
    date = models.DateField()

    class Meta:
        unique_together = ("company_employee", "date",)

    def __str__(self):
        return f"<Salary salary={self.salary} date={self.date}>"


class SalaryCache(models.Model):
    company_employee = models.ForeignKey(
        CompanyEmployee,
        on_delete=models.CASCADE
    )

    year = models.PositiveIntegerField(
            validators=[
                MinValueValidator(2000),
                MaxValueValidator(2068)])

    salary = models.PositiveSmallIntegerField(null=True)

    class Meta:
        unique_together = ("company_employee", "year",)

    def __str__(self):
        return f"<SalaryCache salary={self.salary} year={self.year}>"
