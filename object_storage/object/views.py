from django.shortcuts import redirect
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, LoginSerializer, TempUserSerializer
from .models import CustomUser, TempUser
from .utils import generate_email_verification_token, verify_email_verification_token
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings


class RegisterView(APIView):
    def post(self, request):
        serializer = TempUserSerializer(data=request.data)
        if serializer.is_valid():
            temp_user = serializer.save()
            token = generate_email_verification_token(temp_user.email)
            temp_user.token = token
            temp_user.save()
            verification_link = request.build_absolute_uri(f'/users/verify-email/{token}/')
            send_mail(
                'ایمیل تأیید ثبت‌نام',
                f'برای تأیید ثبت‌نام خود روی لینک زیر کلیک کنید:\n{verification_link}',
                settings.DEFAULT_FROM_EMAIL,
                [temp_user.email],
                fail_silently=False,
            )
            return Response({"message": "ثبت‌نام با موفقیت انجام شد. یک ایمیل تأیید به شما ارسال شد."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request, token):
        email = verify_email_verification_token(token)
        if email:
            try:
                temp_user = TempUser.objects.get(email=email)
                raw_password = temp_user.get_raw_password()  # دریافت پسورد اصلی
                user = CustomUser(
                    username=temp_user.username,
                    email=temp_user.email,
                    is_active=True,
                )
                print(raw_password+'-----------------------')
                user.set_password(raw_password)  # استفاده از پسورد اصلی
                user.save()
                temp_user.delete()
                return redirect('login')  # نام URL صفحه ورود خود را تنظیم کنید
            except TempUser.DoesNotExist:
                return HttpResponse('کاربر یافت نشد.', status=status.HTTP_404_NOT_FOUND)
        return HttpResponse('لینک تأیید نامعتبر است یا منقضی شده است.', status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)