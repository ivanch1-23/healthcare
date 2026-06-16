from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'rol', 'first_name', 'last_name')
        read_only_fields = ('id', 'username', 'email', 'rol')
