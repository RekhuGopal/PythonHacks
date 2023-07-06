from rest_framework import serializers
from .models import YouTube

class YoutubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTube
        fields = '__all__'