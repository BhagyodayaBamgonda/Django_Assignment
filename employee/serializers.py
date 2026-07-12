from rest_framework import serializers
from .models import Employee, Leave


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = "__all__"

    def validate_mobile_number(self, value):
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError(
                "Mobile number must contain exactly 10 digits."
            )
        return value


class LeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.name", read_only=True)

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

    def validate(self, data):

        from_date = data.get("from_date")
        to_date = data.get("to_date")

        if from_date and to_date and from_date > to_date:
            raise serializers.ValidationError(
                "From Date cannot be greater than To Date."
            )

        return data
