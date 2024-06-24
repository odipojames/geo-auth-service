from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from .models import CustomUser,Profile
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from .tokens import CustomAccessToken
from django.contrib.auth.password_validation import validate_password


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already taken")]
    )
    password = serializers.CharField( max_length=124, min_length=8, write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role','password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data.get('role', 'staff'),
            password=validated_data['password']
        )
        return user

class CustomTokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError({'email_passward': _('invalid email or password')})
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        attrs['user'] = user
        return attrs

   
    def create(self, validated_data):
        user = validated_data['user']
        token = CustomAccessToken(user=user)
        #token = AccessToken.for_user(user)
        return {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role':user.role,
            'token': str(token),
        }
    


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(_('User with this email address does not exist.'))

        return value

    def save(self):
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(max_length=124, min_length=8, write_only=True, validators=[validate_password])
    re_new_password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        try:
            self.token = UntypedToken(value)
            self.user = CustomUser.objects.get(id=self.token['user_id'])
        except Exception as e:
            raise serializers.ValidationError(_('Invalid token or token expired.'))

        if not self.user.is_active:
            raise serializers.ValidationError(_('User account is disabled.'))

        return value

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        re_new_password = attrs.get('re_new_password')

        if new_password != re_new_password:
            raise serializers.ValidationError({'new_password': _('Passwords do not match.')})
        return attrs

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()
        return self.user
    



class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = fields  #read-only


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    class Meta:
        model = Profile
        fields = ['id','profile_picture','user']

    def update(self, instance, validated_data):
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance



