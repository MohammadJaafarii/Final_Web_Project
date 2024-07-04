from rest_framework import serializers
from .models import ObjectStorage,CustomUser,UploadedFile

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

class UploadedFileSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()

    class Meta:
        model = UploadedFile
        fields = '__all__'
        read_only_fields = ['upload_date']

    def get_icon_url(self, obj):
        return obj.get_icon_url()
