from django.urls import path
from django.urls import include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('profile', views.UserProfileViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', views.UserProfileView.as_view()),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),
    path('login/', views.UserLoginApiView.as_view()),
    path('logout/', views.LogoutView.as_view()),
]
