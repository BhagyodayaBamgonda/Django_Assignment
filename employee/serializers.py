from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import Employee, Leave


class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", required=False)
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "user",
            "username",
            "password",
            "employee_id",
            "name",
            "email",
            "department",
            "mobile_number",
            "date_of_joining",
        ]
        read_only_fields = ["user"]

    def validate_mobile_number(self, value):
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError(
                "Mobile number must contain exactly 10 digits."
            )
        return value

    def validate(self, data):
        user_data = data.get("user") or {}
        username = user_data.get("username")
        employee_id = data.get("employee_id")
        target_username = username or employee_id
        instance_user = self.instance.user if self.instance else None

        if target_username:
            users = User.objects.filter(username=target_username)

            if instance_user:
                users = users.exclude(pk=instance_user.pk)

            if users.exists():
                raise serializers.ValidationError(
                    {"username": "This username is already used."}
                )

        return data

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop("password", "")
        user_data = validated_data.pop("user", {})
        username = user_data.get("username") or validated_data["employee_id"]

        user = User.objects.create_user(
            username=username,
            password=password or validated_data["employee_id"],
            email=validated_data["email"],
            first_name=validated_data["name"],
            is_staff=False
        )

        return Employee.objects.create(user=user, **validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        password = validated_data.pop("password", "")
        user_data = validated_data.pop("user", {})
        user = instance.user

        if not user:
            user = User.objects.create_user(
                username=user_data.get("username") or validated_data.get(
                    "employee_id",
                    instance.employee_id
                ),
                password=password or validated_data.get(
                    "employee_id",
                    instance.employee_id
                ),
                email=validated_data.get("email", instance.email),
                first_name=validated_data.get("name", instance.name),
                is_staff=False
            )
            instance.user = user

        if user_data.get("username"):
            user.username = user_data["username"]

        user.email = validated_data.get("email", instance.email)
        user.first_name = validated_data.get("name", instance.name)

        if password:
            user.set_password(password)

        user.save()

        return super().update(instance, validated_data)


class LeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.name", read_only=True)
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False
    )

    class Meta:
        model = Leave
        fields = [
            "id",
            "employee",
            "employee_name",
            "leave_type",
            "from_date",
            "to_date",
            "reason",
            "status",
        ]
        read_only_fields = ["status"]

    def create(self, validated_data):
        employee = self.context.get("employee")

        if employee:
            validated_data["employee"] = employee

        return super().create(validated_data)

    def validate(self, data):

        from_date = data.get("from_date")
        to_date = data.get("to_date")

        if not self.instance and not self.context.get("employee"):
            if not data.get("employee"):
                raise serializers.ValidationError(
                    {"employee": "Employee is required."}
                )

        if from_date and to_date and from_date > to_date:
            raise serializers.ValidationError(
                "From Date cannot be greater than To Date."
            )

        return data


class LeaveStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leave
        fields = ["status"]
