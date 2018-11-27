from rest_framework import serializers

from .models import Company, Person, CompanyEmployee


class PersonOneSerializer(serializers.ModelSerializer):
    company_url = serializers.HyperlinkedIdentityField(
        view_name='one_company',
        lookup_field='id'
    )

    class Meta:
        model = Person

        fields = [
            'id',
            'company_url',
            'first_name',
            'second_name',
            'created_on',
        ]


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
        employees = PersonOneSerializer(Person.objects.get(id=obj.id), context = {'request': self.context.get("request")})
        return employees.data


class CompanyOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company

        fields = [
            'id',
            'name',
            'description',
            'created_on',
        ]


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
        companies_employees = CompanyEmployeeSerializer(CompanyEmployee.objects.filter(company=obj),
                                                        many=True, context={'request': self.context.get("request")})
        return companies_employees.data
