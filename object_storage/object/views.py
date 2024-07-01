from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ObjectStorage,CustomUser
from .serializer import ObjectStorageSerializer,CustomUserRetSerializer
from rest_framework.parsers import MultiPartParser,FormParser
from . import arvan


class ObjectStorageCreateView(APIView):
    parser_classes = [MultiPartParser,FormParser]

    def post(self, request):
        serializer = ObjectStorageSerializer(data=request.data)
        object_name = request.data['object_name']
        file_path = request.data['url_file']
        flag = arvan.uploadobject(file_path=file_path, object_name=object_name)
        if flag:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObjectStorageSingle(APIView):
    def delete(self,request,pk):
        object = ObjectStorage.objects.get(pk=pk)
        object_name = object.object_name
        flag = arvan.deleteobject(object_name=object_name)
        if flag:
            object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk):
        object = ObjectStorage.objects.get(pk=pk)
        object_name = object.object_name
        flag = arvan.download_object(object_name=object_name)
        if flag:
            serializer = ObjectStorageSerializer(object)
            return Response(serializer.data,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

class ObjectStorageManagement(APIView):
    def get(self,request,pk):
        try:

            accessible_objects = ObjectStorage.objects.filter(accessible_users__id=pk)
            serializer = ObjectStorageSerializer(accessible_objects, many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
        except ObjectStorage.DoesNotExist:
            return Response({"error": "Objects not found."}, status=status.HTTP_404_NOT_FOUND)

class ObjectStorageAccessManagement(APIView):
    def patch(self,request,action:str,pk:int):
        obj_id = request.data.get('id')
        object = ObjectStorage.objects.get(pk=obj_id)

        if action == 'add':
            object.accessible_users.add(pk)
            message = f"User {pk} added to accessible users of object {obj_id}."

        elif action == 'delete':
            object.accessible_users.remove(pk)
            message = f"User {pk} removed from accessible users of object {obj_id}."
        else:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        object.save()
        return Response({"message": message}, status=status.HTTP_200_OK)

class AllUser(APIView):
    def get(self,request):
        all_user = CustomUser.objects.all()
        serializer = CustomUserRetSerializer(all_user,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
