from rest_framework import serializers
from .models import Cars

class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        # field = ('id', 'mobile', 'fullname')
        fields = '__all__'