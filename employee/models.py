from django.db import models


class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=10)
    date_of_joining = models.DateField()

    def __str__(self):
        return self.name


class Leave(models.Model):

    LEAVE_TYPE = [
        ('Casual', 'Casual'),
        ('Sick', 'Sick'),
        ('Earned', 'Earned'),
    ]

    STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    leave_type = models.CharField(
        max_length=20,
        choices=LEAVE_TYPE
    )

    from_date = models.DateField()
    to_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Pending'
    )

    def __str__(self):
        return f"{self.employee.name} - {self.leave_type}"