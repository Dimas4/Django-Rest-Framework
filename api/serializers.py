from rest_framework import serializers

from .models import Company, Person


class PersonOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person

        fields = [
            'id',
            'first_name',
            'second_name',
            'profile_link',
            'created_on',
        ]


class PersonPutSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Person
        fields = (
            'profile_link',
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
            'employees',
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
