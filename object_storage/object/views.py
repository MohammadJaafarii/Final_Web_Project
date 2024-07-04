import mimetypes

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ObjectStorage,CustomUser,UploadedFile
from .pagination import CustomPageNumberPagination
from .serializer import ObjectStorageSerializer,CustomUserRetSerializer,UploadedFileSerializer
from rest_framework.parsers import MultiPartParser,FormParser
from django.http import HttpResponseRedirect
from . import arvan
from django.shortcuts import redirect
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, LoginSerializer, TempUserSerializer
from .models import CustomUser, TempUser
from .utils import generate_email_verification_token, verify_email_verification_token
from django.contrib.auth import login
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages


class ObjectStorageCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get('file')
        owner = request.data.get('owner')
        accessible_users = list(request.data.get('accessible_users'))
        print('---------', file)
        print('---------', owner)
        print('---------', accessible_users)

        if file:
            # دریافت نوع فایل با استفاده از mimetypes
            file_type, _ = mimetypes.guess_type(file.name)
            if file_type is None:
                file_type = 'application/octet-stream'  # مقدار پیش‌فرض در صورت عدم شناسایی نوع فایل

            file_data = {
                'file': file,
                'file_name': file.name,
                'file_type': file_type,
                'file_size': file.size,
                'owner': owner,
                'accessible_users': accessible_users,
            }
            serializer = UploadedFileSerializer(data=file_data)
            path = f'C:\\Users\\ok\\PycharmProjects\\final web\\Final_Web_Project\\object_storage\\media\\uploads\\{file.name}'
            if serializer.is_valid():
                saved_instance = serializer.save()
                flag = arvan.uploadobject(file_path=path, object_name=file.name)
                if flag:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                saved_instance.delete()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)


class ObjectStorageSingle(APIView):
    def delete(self,request,pk):
        object = UploadedFile.objects.get(pk=pk)
        object_name = object.file_name
        flag = arvan.deleteobject(object_name=object_name)
        if flag:
            object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk):
        object = UploadedFile.objects.get(pk=pk)
        object_name = object.file_name
        flag = arvan.download_object(object_name=object_name)
        if flag:
            serializer = UploadedFileSerializer(object)
            return Response(serializer.data,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

class ObjectStorageManagement(APIView):
    def get(self,request,pk):
        try:

            accessible_objects = UploadedFile.objects.filter(accessible_users__id=pk)
            paginator = CustomPageNumberPagination()
            paginated_objects = paginator.paginate_queryset(accessible_objects, request)
            serializer = UploadedFileSerializer(paginated_objects, many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
        except UploadedFile.DoesNotExist:
            return Response({"error": "Objects not found."}, status=status.HTTP_404_NOT_FOUND)

class ObjectStorageAccessManagement(APIView):
    def post(self,request,pk:int):
        user = request.data.get('values')
        object = UploadedFile.objects.get(pk=pk)
        object.accessible_users.set(user)
        object.save()
        for id in user:
            us = CustomUser.objects.get(pk=id)
            email = EmailMultiAlternatives(
                'ایمیل دسترسی دادن به شی',
                f'شما به ابجکت {object.file_name} دسترسی پیدا کردید.',
                settings.DEFAULT_FROM_EMAIL,
                [us.email]
            )
            email.send()

        return Response({"message": 'successful'}, status=status.HTTP_200_OK)

class AllUser(APIView):
    def get(self,request):
        all_user = CustomUser.objects.all()
        serializer = CustomUserRetSerializer(all_user,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        serializer = TempUserSerializer(data=request.data)
        if serializer.is_valid():
            temp_user = serializer.save()
            token = generate_email_verification_token(temp_user.email)
            temp_user.token = token
            temp_user.save()
            verification_link = request.build_absolute_uri(f'/users/verify-email/{token}/')
            context = {
                'verification_link': verification_link,
                'username': temp_user.username.capitalize()
            }
            # Render the HTML email template
            html_message = render_to_string('email.html', context)
            plain_message = strip_tags(html_message)

            email = EmailMultiAlternatives(
                'ایمیل تأیید ثبت‌نام',
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [temp_user.email]
            )
            email.attach_alternative(html_message, "text/html")
            email.send()
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
                user.set_password(raw_password)  # استفاده از پسورد اصلی
                user.save()
                temp_user.delete()
                return HttpResponseRedirect('http://127.0.0.1:5500/verify.html')
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

