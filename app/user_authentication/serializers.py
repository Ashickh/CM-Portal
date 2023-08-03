from rest_framework import serializers
from app.user_authentication.models import *
from rest_framework.validators import ValidationError
import uuid


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id','first_name', 'last_name', 'email', 'phonenumber', 'password','address','confirm_password')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ValidationError("Those Passwords don't match")
        return attrs
            
    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.is_verfied = True
        user.full_clean()
        user.save()
        role = Role.objects.get(name='Customer')
        user_role =  UserRole.objects.create(user=user,role=role)
        user_role.full_clean()      
        user_role.save()      
        return user  


    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance



#role creation customer

#     def role_creation(request):
#         serializer = RoleSerializer(data=request.data)
#         name = request.data['name']
#         with transaction.atomic():
#             try:
#                 if Role.objects.filter(name=name).exists():
#                     role = Role.objects.get(name=name)
#                     return response(status=status.HTTP_400_BAD_REQUEST,message=messages.ROLE_ADD_DUPLICATE,data=[])
#                 if serializer.is_valid(raise_exception=True):
#                     role = serializer.save()
#                     customer_role = Role.objects.all()
#                     print(customer_role)
#                     for customer in customer_role:
#                          Role.objects.create(role=role,customer=customer)
#                     return response(status=status.HTTP_201_CREATED, message=messages.ROLE_CREATION_SUCESS, data=serializer.data)
#                 return response(status=status.HTTP_400_BAD_REQUEST,message=messages.ROLE_CREATION_FAILED,data=[])
#             except Exception as e:
#                      return response(status=status.HTTP_400_BAD_REQUEST,message=messages.ROLE_CREATION_FAILED,data=[])        

# class UserRoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserRole
#         fields = "__all__"

#     def user_role_creation(request):
#         serializer = UserRoleSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return response(status=status.HTTP_201_CREATED, message=messages.USER_ROLE_CREATION_SUCESS, data=serializer.data)
#         return response(status=status.HTTP_400_BAD_REQUEST, message=messages.USER_ROLE_CREATION_FAILED, data=[])



#3 reset password
# token get

class EmailTokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)
    class Meta:
        model = EmailToken
        fields = "__all__"

    def create(self, validated_data):
        validated_data['token'] = str(uuid.uuid4())  # Generate unique token
        return super().create(validated_data)   


#email send n access token
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Invalid email.')
        return value        


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"



class RoleFeatureSerializer(serializers.ModelSerializer):
    feature_name  = serializers.ReadOnlyField(source='feature.name')
    feature_id  = serializers.ReadOnlyField(source='feature.id')

    class Meta:
        model = RoleFeature
        fields = ['id','feature_name','feature_id','view','edit','delete','create']


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        # label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )


class UserSerializer(serializers.ModelSerializer):
    role_id = serializers.IntegerField(write_only=True)
    role_name = serializers.SerializerMethodField()

    def get_role_name(self,obj):
        return UserRole.objects.get(user=obj).role.name

    class Meta:
        model = CustomUser
        fields = ('id','first_name', 'last_name', 'email', 'phonenumber', 'is_active','role_id', 'role_name')
    
    def create(self, validated_data):
        role_id = validated_data.pop('role_id')
        user = self.Meta.model(**validated_data)
        user.set_password('P05r 0t 6u4 %9jye')
        user.is_active = True
        user.full_clean()
        user.save()
        role = Role.objects.get(id= role_id)
        user_role =  UserRole.objects.create(user=user,role=role)
        user_role.full_clean()      
        user_role.save()   
        return user  

    def update(self, instance, validated_data):
        role_id = validated_data.pop('role_id')
        role = Role.objects.get(id= role_id)
        user_role =  UserRole.objects.get(user=instance)
        user_role.role = role
        user_role.save()
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    role_id = serializers.SerializerMethodField()

    def get_role_id(self,obj):
        return UserRole.objects.get(user=obj).role.id


    class Meta:
        model = CustomUser
        fields = ('id','first_name', 'last_name', 'email', 'phonenumber','role_id','address')
    
class UserDeleteSerializer(serializers.ModelSerializer):


    class Meta:
        model = CustomUser
        fields = ('id','is_active')
    

class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ChangePasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()