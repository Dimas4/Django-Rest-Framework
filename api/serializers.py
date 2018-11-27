from django.core.paginator import Paginator

from rest_framework import serializers


from .models import Company, Person, CompanyEmployee


class PersonListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='one_employee',
        lookup_field='id'
    )

    class Meta:
        model = Person

        fields = [
            'id',
            'url',
            'first_name',
            'second_name',
        ]


class PersonOneSerializer(PersonListSerializer):
    class Meta(PersonListSerializer.Meta):
        fields = PersonListSerializer.Meta.fields + [
            'created_on'
        ]


class CompanyEmployeeSerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()

    class Meta:
        model = CompanyEmployee

        fields = [
            'employee',

            'work_start_dt',
            'work_end_dt'
        ]

    def get_employee(self, obj):
        employees = PersonOneSerializer(Person.objects.get(id=obj.id), context={'request': self.context.get("request")})
        return employees.data


class CompanyListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='one_company',
        lookup_field='id'
    )

    class Meta:
        model = Company

        fields = [
            'id',
            'url',
            'name',
            'description',
        ]


class CompanyOneSerializer(CompanyListSerializer):
    company_employee = serializers.SerializerMethodField()

    class Meta(CompanyListSerializer.Meta):
        fields = CompanyListSerializer.Meta.fields + [
            'company_employee',
            'created_on',
        ]

    def get_company_employee(self, obj):
        companies_employees = CompanyEmployeeSerializer(CompanyEmployee.objects.filter(company=obj),
                                                        many=True, context={'request': self.context.get("request")})

        return companies_employees.data
