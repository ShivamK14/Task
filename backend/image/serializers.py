from rest_framework import serializers
from .models import InputImage, OutputImage


class InputImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputImage
        fields = '__all__'


class OutputImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputImage
        fields = '__all__'