from rest_framework import serializers

from users.models import CommonUser, Customer, Employee


class CommonUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CommonUser
        fields = ("username", "email", "password", "first_name", "last_name", "patronymic",)

        lookup_field = "email"
        extra_kwargs = {
            "url": {
                "lookup_field": "email"
            }
        }


class CustomerSerializer(serializers.ModelSerializer):
    user = CommonUserSerializer()

    class Meta:
        model = Customer
        fields = ('user', 'telephone_number')

        lookup_field = "email"
        extra_kwargs = {
            "url": {
                "lookup_field": "email"
            }
        }

    def create(self, validated_data) -> (Customer, CommonUser):
        """
        Overrode 'create' method specifically for the 'customer' field with nested serializer.
        """
        CommonUser_data = validated_data.pop('user')
        NewCommonUser = CommonUser.objects.create(**CommonUser_data)
        NewCustomer = Customer.objects.create(user=NewCommonUser, email=CommonUser_data.get('email'), **validated_data)

        return NewCustomer

    def update(self, instance, validated_data):
        """
        Overrode 'update' method specifically for the 'customer' field with nested serializer.
        """
        CommonUser_data = validated_data.pop('user')
        UpdatedCommonUser = instance.user
        UpdatedCommonUser.username = CommonUser_data.get('username', UpdatedCommonUser.username)
        UpdatedCommonUser.email = CommonUser_data.get('email', UpdatedCommonUser.email)
        UpdatedCommonUser.password = CommonUser_data.get('password', UpdatedCommonUser.password)
        UpdatedCommonUser.first_name = CommonUser_data.get('first_name', UpdatedCommonUser.first_name)
        UpdatedCommonUser.last_name = CommonUser_data.get('last_name', UpdatedCommonUser.last_name)
        UpdatedCommonUser.patronymic = CommonUser_data.get('patronymic', UpdatedCommonUser.patronymic)
        UpdatedCommonUser.save()

        instance.telephone_number = validated_data.get('telephone_number', instance.telephone_number)
        instance.email = CommonUser_data.get('email', instance.email)
        instance.save()

        return instance


class EmployeeSerializer(serializers.ModelSerializer):
    user = CommonUserSerializer()

    class Meta:
        model = Employee

        fields = ('user', 'education', 'position')
