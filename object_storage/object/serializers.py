from rest_framework import serializers
from .models import CustomUser, TempUser
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
import re

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        username = data.get('username', '').lower()
        email = data.get('email', '').lower()
        password = data.get('password', '')

        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("نام کاربری انتخاب شده قبلا استفاده شده است.")
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("این ایمیل قبلا ثبت شده است.")

        if len(username) < 4:
            raise serializers.ValidationError("نام کاربری باید حداقل 4 کاراکتر باشد.")
        if not re.match("^[a-zA-Z]*$", username):
            raise serializers.ValidationError("نام کاربری باید فقط شامل حروف انگلیسی باشد.")
        if len(password) < 6:
            raise serializers.ValidationError("رمز عبور باید حداقل 6 کاراکتر باشد.")
        if not re.search("[a-z]", password):
            raise serializers.ValidationError("رمز عبور باید شامل حداقل یک حرف کوچک باشد.")
        if not re.search("[A-Z]", password):
            raise serializers.ValidationError("رمز عبور باید شامل حداقل یک حرف بزرگ باشد.")
        if not re.search("[0-9]", password):
            raise serializers.ValidationError("رمز عبور باید شامل حداقل یک عدد باشد.")
        if not re.search("[@!#$%&]", password):
            raise serializers.ValidationError("رمز عبور باید شامل حداقل یک کاراکتر خاص مانند @!#$%& باشد.")

        return data

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'].lower(),
            email=validated_data['email'].lower(),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username_or_email = data.get('username_or_email').lower()
        password = data.get('password')

        try:
            if '@' in username_or_email:
                user = CustomUser.objects.get(email=username_or_email)
            else:
                user = CustomUser.objects.get(username=username_or_email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid UserName or Email")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid Password")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        data['user'] = user
        return data

class TempUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempUser
        fields = ['id', 'username', 'email', 'password', 'raw_password', 'token', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'raw_password': {'write_only': True},
            'token': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError('نام کاربری باید حداقل 4 کاراکتر باشد.')
        if not re.match("^[a-zA-Z]*$", value):
            raise serializers.ValidationError('نام کاربری باید فقط شامل حروف انگلیسی باشد.')
        if CustomUser.objects.exclude(pk=self.instance.pk if self.instance else None).filter(username=value.lower()).exists()\
                or TempUser.objects.exclude(pk=self.instance.pk if self.instance else None).filter(username=value.lower()).exists():
            raise serializers.ValidationError('نام کاربری انتخاب شده قبلا استفاده شده است.')
        return value.lower()

    def validate_email(self, value):
        if CustomUser.objects.exclude(pk=self.instance.pk if self.instance else None).filter(email=value.lower()).exists() \
                or TempUser.objects.exclude(pk=self.instance.pk if self.instance else None).filter(email=value.lower()).exists():
            raise serializers.ValidationError('این ایمیل قبلا ثبت شده است.')
        return value.lower()

    def validate_raw_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('رمز عبور باید حداقل 6 کاراکتر باشد.')
        if not re.search("[a-z]", value):
            raise serializers.ValidationError('رمز عبور باید شامل حداقل یک حرف کوچک باشد.')
        if not re.search("[A-Z]", value):
            raise serializers.ValidationError('رمز عبور باید شامل حداقل یک حرف بزرگ باشد.')
        if not re.search("[0-9]", value):
            raise serializers.ValidationError('رمز عبور باید شامل حداقل یک عدد باشد.')
        if not re.search("[@!#$%&]", value):
            raise serializers.ValidationError('رمز عبور باید شامل حداقل یک کاراکتر خاص مانند @!#$%& باشد.')
        return value

    def create(self, validated_data):
        raw_password = validated_data.pop('raw_password', None)
        user = super().create(validated_data)
        if raw_password:
            user.set_password(raw_password)
            user.save()
        return user

    def update(self, instance, validated_data):
        raw_password = validated_data.pop('raw_password', None)
        instance = super().update(instance, validated_data)
        if raw_password:
            instance.set_password(raw_password)
            instance.save()
        return instance