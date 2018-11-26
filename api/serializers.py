from rest_framework import serializers

from .models import Company, Person, CompanyEmployee


class PersonOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person

        fields = [
            'id',
            'first_name',
            'second_name',
            'created_on',
        ]


class PersonPutSerializer(serializers.HyperlinkedModelSerializer):
    first_name = serializers.CharField(required=False)
    second_name = serializers.CharField(required=False)

    class Meta:
        model = Person
        fields = (
            'first_name',
            'second_name',
        )


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


class CompanyOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company

        fields = [
            'id',
            'name',
            'description',
            'created_on',
        ]


class CompanyPutSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Company
        fields = (
            'name',
            'description',
        )


class CompanyEmployeeSerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()

    class Meta:
        model = CompanyEmployee

        fields = [
            'company',
            'employee',

            'work_start_dt',
            'work_end_dt'
        ]

    def get_employee(self, obj):
        employees = PersonOneSerializer(Person.objects.get(id=obj.id))
        return employees.data


class CompanyListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='one_company',
        lookup_field='id'
    )
    company_employee = serializers.SerializerMethodField()

    class Meta:
        model = Company

        fields = [
            'id',
            'url',
            'name',
            'company_employee',
            'description',
        ]

    def get_company_employee(self, obj):
        companies_employees = CompanyEmployeeSerializer(CompanyEmployee.objects.filter(company=obj), many=True)
        return companies_employees.data
