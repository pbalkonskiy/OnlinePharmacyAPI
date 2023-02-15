from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import CommonUser, Customer, Employee


class CommonUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = CommonUser
        fields = ("email", "slug", "password", "first_name", "last_name", "patronymic",)

        lookup_field = "slug"
        extra_kwargs = {
            "url": {
                "lookup_field": "slug"
            }
        }


class CustomerSerializer(serializers.ModelSerializer):
    user = CommonUserSerializer()
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Customer
        fields = ('user', 'slug', 'telephone_number')

        lookup_field = "slug"
        extra_kwargs = {
            "url": {
                "lookup_field": "slug"
            }
        }

    def create(self, validated_data) -> (Customer, CommonUser):
        """
        Overrode 'create' method specifically for the 'customer' field with nested serializer.
        """

        CommonUser_data = validated_data.pop('user')
        NewCommonUser = CommonUser(**CommonUser_data)
        NewCommonUser.set_password(CommonUser_data['password'])
        NewCommonUser.save()
        NewCustomer = Customer.objects.create(user=NewCommonUser, **validated_data)
        return NewCustomer

    def update(self, instance, validated_data):
        """
        Overrode 'update' method specifically for the 'customer' field with nested serializer.
        """

        user_data = validated_data.pop('user')
        user_serializer = CommonUserSerializer(instance=instance.user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.update(instance.user, user_data)
        return super().update(instance, validated_data)


class EmployeeSerializer(serializers.ModelSerializer):
    user = CommonUserSerializer()
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Employee
        fields = ('user', 'slug', 'education', 'position')

        lookup_field = "slug"
        extra_kwargs = {
            "url": {
                "lookup_field": "slug"
            }
        }

    def create(self, validated_data) -> (Employee, CommonUser):
        """
        Overrode 'create' method specifically for the 'employee' field with nested serializer.
        """
        UserData = validated_data.pop('user')
        NewCommonUser = CommonUser(**UserData)
        NewCommonUser.set_password(UserData['password'])
        NewCommonUser.save()
        NewEmployee = Employee.objects.create(user=NewCommonUser, **validated_data)
        return NewEmployee

    def update(self, instance, validated_data):
        """
        Overrode 'update' method specifically for the 'employee' field with nested serializer.
        """
        user_data = validated_data.pop('user')
        user_serializer = CommonUserSerializer(instance=instance.user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.update(instance.user, user_data)
        return super().update(instance, validated_data)
