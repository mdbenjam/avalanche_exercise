from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['pk', 'company', 'user']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['pk', 'name', 'data']

class CompanySerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True)
    profiles = ProfileSerializer(many=True)

    class Meta:
        model = Company
        fields = ['pk', 'name', 'projects', 'profiles']
