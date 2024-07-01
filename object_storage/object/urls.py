from django.urls import path
from .views import ObjectStorageCreateView,ObjectStorageSingle,ObjectStorageManagement,ObjectStorageAccessManagement,AllUser,RegisterView, VerifyEmailView, LoginView

urlpatterns = [
    path('create-object/', ObjectStorageCreateView.as_view(), name='create-object'),
    path('object/<int:pk>',ObjectStorageSingle.as_view(),name='object'),
    path('user/<int:pk>',ObjectStorageManagement.as_view(),name='user-object'),
    path('user/<str:action>/<int:pk>',ObjectStorageAccessManagement.as_view(), name='access-manage'),
    path('users/',AllUser.as_view(),name='all-users'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    ]
    
