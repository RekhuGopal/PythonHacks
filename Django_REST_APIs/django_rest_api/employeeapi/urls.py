from django.urls import path
from .viewsets import EmployeeViewset


urlpatterns = [
    path('employeeapi/', EmployeeViewset.as_view()),
    path('employeeapi/<int:id>', EmployeeViewset.as_view())
]