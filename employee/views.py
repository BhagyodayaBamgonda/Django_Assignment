from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer
from django.db.models import Q


# GET All Employees & POST Employee
@api_view(['GET', 'POST'])
def employee_list(request):

    if request.method == 'GET':

        search = request.GET.get('search')

        employees = Employee.objects.all()

        if search:
            employees = employees.filter(
                Q(name__icontains=search) |
                Q(employee_id__icontains=search)
            )

        serializer = EmployeeSerializer(employees, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

# GET by ID, PUT & DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, pk):

    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response(
            {"message": "Employee not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        employee.delete()
        return Response(
            {"message": "Employee Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    
from .models import Leave
from .serializers import LeaveSerializer

@api_view(['GET', 'POST'])
def leave_list(request):

    if request.method == 'GET':

        status_filter = request.GET.get('status')

        leave_type = request.GET.get('leave_type')

        leaves = Leave.objects.all()

        if status_filter:
            leaves = leaves.filter(status=status_filter)

        if leave_type:
            leaves = leaves.filter(leave_type=leave_type)

        serializer = LeaveSerializer(leaves, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = LeaveSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def leave_detail(request, pk):

    try:
        leave = Leave.objects.get(pk=pk)

    except Leave.DoesNotExist:
        return Response(
            {"message": "Leave not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = LeaveSerializer(leave)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LeaveSerializer(leave, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        leave.delete()

        return Response(
            {"message": "Leave Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    

@api_view(['GET'])
def dashboard(request):

    data = {
        "total_employees": Employee.objects.count(),
        "total_leave_applications": Leave.objects.count(),
        "pending": Leave.objects.filter(status="Pending").count(),
        "approved": Leave.objects.filter(status="Approved").count(),
        "rejected": Leave.objects.filter(status="Rejected").count(),
    }

    return Response(data)

from django.shortcuts import render

def dashboard_page(request):
    return render(request, "dashboard.html")

def employee_page(request):
    return render(request, "employee.html")

def leave_page(request):
    return render(request, "leave.html")
