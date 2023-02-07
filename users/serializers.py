from rest_framework import serializers

from users.models import CommonUser, Customer, Employee


class CommonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonUser

        fields = ("first_name", "last_name", "patronymic", "email")


class CustomerSerializer(serializers.ModelSerializer):
    user = CommonUserSerializer()

    class Meta:
        model = Customer

        fields = ('user', 'telephone_number')


class EmployeeSerializer(serializers.ModelSerializer):
    user = CommonUserSerializer()

    class Meta:
        model = Employee

        fields = ('user', 'education', 'position')
