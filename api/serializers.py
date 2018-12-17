from datetime import date

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
        employees = PersonOneSerializer(
            Person.objects.get(id=obj.employee.id),
            context={'request': self.context.get("request")}
        )
        return employees.data

    def validate(self, attrs):
        start_field = attrs['work_start_dt']
        end_field = attrs.get('work_end_dt')
        after_100_years = date.today().year + 100
        if not (date(year=2000, month=1, day=1)
                <= start_field <=
                date(year=after_100_years, month=1, day=1)
                ):

            raise serializers.ValidationError(
                f'Year must be between 2000 and {after_100_years}'
            )
        if end_field > date.today():
            raise serializers.ValidationError('Date must be in the past')
        return attrs


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
    company_employee = serializers.HyperlinkedIdentityField(
        view_name='one_employee_by_company_id',
        lookup_field='id'
    )

    class Meta(CompanyListSerializer.Meta):
        fields = CompanyListSerializer.Meta.fields + [
            'company_employee',
            'created_on',
        ]


class SalaryParamsSerializer(serializers.Serializer):
    company_employee_id = serializers.IntegerField()
    salary = serializers.IntegerField()
    date = serializers.DateField(format="%Y-%m", input_formats=['%Y-%m'])

    def validate(self, attrs):
        date_field = attrs['date']
        after_100_years = date.today().year + 100
        if not (date(year=2000, month=1, day=1)
                <= date_field <=
                date(year=after_100_years, month=1, day=1)
                ):

            raise serializers.ValidationError(
                f'Year must be between 2000 and {after_100_years}'
            )
        return attrs


class WorkDateSerializer(serializers.Serializer):
    start_date = serializers.DateField(format="%Y-%m", input_formats=['%Y-%m'])
    end_date = serializers.DateField(
        allow_null=True,
        format="%Y-%m",
        input_formats=['%Y-%m']
    )
    current_date = serializers.DateField(
        format="%Y-%m",
        input_formats=['%Y-%m']
    )

    def compare_dt_year_month(self, first, second):
        if first.year < second.year:
            return True
        if first.year == second.year:
            return True if first.month <= second.month else False
        return False

    def validate(self, attrs):
        if not self.compare_dt_year_month(
                attrs['start_date'],
                attrs['current_date']):
            raise serializers.ValidationError(
                {"date": "date must be greater than the start work date"}
            )
        if attrs['end_date']:
            if not self.compare_dt_year_month(
                    attrs['current_date'],
                    attrs['end_date']):
                raise serializers.ValidationError(
                    {"current_date": "date must be less than the end work date"}
                )
        return attrs
