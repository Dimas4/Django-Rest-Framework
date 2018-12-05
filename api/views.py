from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.views import APIView

from django.db.models import Q

from .models import Company, Person, CompanyEmployee
from celery_tasks.tasks import add_to_salary_cached
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
    def post(self, request, id):
        add_to_salary_cached.delay(id)
        return Response({'status': 'ok'})
