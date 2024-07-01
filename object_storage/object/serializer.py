from rest_framework import serializers
from .models import ObjectStorage,CustomUser

class ObjectStorageSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField()
    class Meta:
        model = ObjectStorage
        fields = ['id','object_name','url_file','icon','size', 'upload_datetime', 'owner', 'accessible_users']
        read_only_fields = ['upload_datetime']

class CustomUserRetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email']
