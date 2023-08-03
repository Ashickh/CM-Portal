from dataclasses import fields
from rest_framework import serializers
from app.user_authentication.models import *
from app.space_management.models import *
from app.role_management.models import *
import uuid

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"
    

class RoleFeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoleFeature
        fields = "__all__"

class UserSerializer1(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email","address", "phonenumber", "first_name","last_name"]

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    role = serializers.IntegerField()
    # def get_role(self,obj):
    #     print(obj["role"])
    #     return obj["role"]
    class Meta:
        model = CustomUser
        fields = ['first_name','email','phonenumber','password','is_active','role']
        read_only_fields = ['role']
  
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        data = validated_data.pop('role')
        print(data)
        for attr, value in validated_data.items():
            
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    
class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = "__all__"


class EmailTokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)
    class Meta:
        model = EmailToken
        fields = "__all__"

    def create(self, validated_data):
        validated_data['token'] = str(uuid.uuid4())  # Generate unique token
        return super().create(validated_data)

   

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Invalid email.')
        return value
