from rest_framework import serializers
from .models import Questions , UserData , Result

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Questions
        fields= ' __all__'

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserData
        fields= ' __all__'