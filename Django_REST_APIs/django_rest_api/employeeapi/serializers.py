from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        # field = ('id', 'mobile', 'fullname')
        fields = '__all__'