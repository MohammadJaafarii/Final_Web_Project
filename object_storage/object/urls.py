from django.urls import path
from .views import ObjectStorageCreateView,ObjectStorageSingle,ObjectStorageManagement,ObjectStorageAccessManagement,AllUser

urlpatterns = [
    path('create-object/', ObjectStorageCreateView.as_view(), name='create-object'),
    path('object/<int:pk>',ObjectStorageSingle.as_view(),name='object'),
    path('user/<int:pk>',ObjectStorageManagement.as_view(),name='user-object'),
    path('user/<str:action>/<int:pk>',ObjectStorageAccessManagement.as_view(), name='access-manage'),
    path('users/',AllUser.as_view(),name='all-users'),
]