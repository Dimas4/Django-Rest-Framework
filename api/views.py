from datetime import datetime

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework import status

from django.db.models import Q

from .date_validation.exception.exception import EmployeeWorkError
from .models import Company, Person, CompanyEmployee, Salary
from celery_tasks.tasks import add_to_salary_cached
from .date_validation.validate import Validate
from .serializers import (
    PersonOneSerializer,
    PersonListSerializer,
    CompanyOneSerializer,
    CompanyListSerializer,
    CompanyEmployeeSerializer,
)


class CompanyOneAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Company.objects.all()
    serializer_class = CompanyOneSerializer


class PersonsByCompanyIdAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = CompanyEmployeeSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        id = self.kwargs['id']
        qs = CompanyEmployee.objects.filter(company__id=id)
        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CompanyListAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = CompanyListSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        qs = Company.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(name__icontains=query))
        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonOneAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Person.objects.all()
    serializer_class = PersonOneSerializer


class PersonListAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = PersonListSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        qs = Person.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(second_name__icontains=query))
        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SalaryListAPIView(APIView):
    def post(self, request):
        company_employee_id, salary, date = request.POST.get('id'), request.POST.get('salary'), \
                                            request.POST.get('date')

        if not company_employee_id or not salary or not date:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            datetime_object = datetime.strptime(date, '%Y-%m')
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            company_employee = CompanyEmployee.objects.get(id=company_employee_id)
        except CompanyEmployee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            Validate.validate_date(company_employee.work_start_dt, company_employee.work_end_dt, datetime_object)
        except EmployeeWorkError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        Salary.objects.update_or_create(company_employee=company_employee,
                                        date=datetime_object, defaults={'salary': salary})

        add_to_salary_cached.delay(company_employee_id, datetime_object.year)
        return Response({'status': 'ok'})
