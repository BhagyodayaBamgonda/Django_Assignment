from django.urls import path
from . import views

urlpatterns = [

    # Dashboard
    path('dashboard/', views.dashboard),

    # Employee APIs
    path('employees/', views.employee_list),
    path('employees/<int:pk>/', views.employee_detail),

    # Leave APIs
    path('leaves/', views.leave_list),
    path('leaves/<int:pk>/', views.leave_detail),
    path("employees-page/", views.employee_page, name="employee_page"),
    path("leaves-page/", views.leave_page, name="leave_page"),
]