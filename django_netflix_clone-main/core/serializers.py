from .models import Movie, CustomUser, Profile
from rest_framework import serializers

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title','id')

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username','email')

class ProfileSerializer:
    class Meta:
        model = Profile
        fields = ('name','age_limit')