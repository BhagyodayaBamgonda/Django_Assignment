from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect


# GET All Employees & POST Employee
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def employee_list(request):

    if not request.user.is_staff:
        return Response(
            {"message": "Only admin can manage employees."},
            status=status.HTTP_403_FORBIDDEN
        )

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
@permission_classes([IsAuthenticated])
def employee_detail(request, pk):

    if not request.user.is_staff:
        return Response(
            {"message": "Only admin can manage employees."},
            status=status.HTTP_403_FORBIDDEN
        )

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
        linked_user = employee.user
        employee.delete()

        if linked_user:
            linked_user.delete()

        return Response(
            {"message": "Employee Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    
from .models import Leave
from .serializers import LeaveSerializer, LeaveStatusSerializer


def get_logged_employee(user):
    if user.is_staff:
        return None

    try:
        return user.employee
    except Employee.DoesNotExist:
        return None

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def leave_list(request):

    if request.method == 'GET':

        status_filter = request.GET.get('status')

        leave_type = request.GET.get('leave_type')

        leaves = Leave.objects.all()

        employee = get_logged_employee(request.user)

        if not request.user.is_staff:
            if not employee:
                return Response([])

            leaves = leaves.filter(employee=employee)

        if status_filter:
            leaves = leaves.filter(status=status_filter)

        if leave_type:
            leaves = leaves.filter(leave_type=leave_type)

        serializer = LeaveSerializer(leaves, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':

        employee = get_logged_employee(request.user)

        if not request.user.is_staff and not employee:
            return Response(
                {"message": "No employee profile is linked with this login."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = LeaveSerializer(
            data=request.data,
            context={"employee": employee}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def leave_detail(request, pk):

    try:
        leave = Leave.objects.get(pk=pk)

    except Leave.DoesNotExist:
        return Response(
            {"message": "Leave not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    employee = get_logged_employee(request.user)

    if not request.user.is_staff and leave.employee != employee:
        return Response(
            {"message": "You can access only your own leaves."},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'GET':
        serializer = LeaveSerializer(leave)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user.is_staff:
            serializer = LeaveStatusSerializer(
                leave,
                data=request.data,
                partial=True
            )
        else:
            if leave.status != "Pending":
                return Response(
                    {"message": "Only pending leaves can be edited."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = LeaveSerializer(
                leave,
                data=request.data,
                partial=True,
                context={"employee": employee}
            )

        if serializer.is_valid():
            serializer.save()
            return Response(LeaveSerializer(leave).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.is_staff and leave.status != "Pending":
            return Response(
                {"message": "Only pending leaves can be deleted."},
                status=status.HTTP_400_BAD_REQUEST
            )

        leave.delete()

        return Response(
            {"message": "Leave Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):

    if not request.user.is_staff:
        return Response(
            {"message": "Only admin can view dashboard data."},
            status=status.HTTP_403_FORBIDDEN
        )

    data = {
        "total_employees": Employee.objects.count(),
        "total_leave_applications": Leave.objects.count(),
        "pending": Leave.objects.filter(status="Pending").count(),
        "approved": Leave.objects.filter(status="Approved").count(),
        "rejected": Leave.objects.filter(status="Rejected").count(),
    }

    return Response(data)

from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache import never_cache


def is_admin(user):
    return user.is_authenticated and user.is_staff


@ensure_csrf_cookie
def login_page(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("dashboard_page")

        return redirect("leave_page")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")

        if user_type == "admin" and not user.is_staff:
            messages.error(request, "This is not an admin account.")
            return render(request, "login.html")

        if user_type == "employee" and user.is_staff:
            messages.error(request, "Please use admin login for this account.")
            return render(request, "login.html")

        login(request, user)

        if user.is_staff:
            return redirect("dashboard_page")

        return redirect("leave_page")

    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect("login_page")


@login_required(login_url="login_page")
@user_passes_test(is_admin, login_url="leave_page")
@never_cache
def dashboard_page(request):
    return render(request, "dashboard.html")


@login_required(login_url="login_page")
@user_passes_test(is_admin, login_url="leave_page")
@never_cache
@ensure_csrf_cookie
def employee_page(request):
    return render(request, "employee.html")


@login_required(login_url="login_page")
@never_cache
@ensure_csrf_cookie
def leave_page(request):
    employee = get_logged_employee(request.user)

    return render(
        request,
        "leave.html",
        {
            "is_admin": request.user.is_staff,
            "employee": employee,
        }
    )
