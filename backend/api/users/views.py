from . import serializers
from django.contrib.auth import logout, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from rest_framework import views, viewsets, status, filters
from rest_framework.response import Response
from users import models
from rest_framework.authentication import TokenAuthentication
from users import permissions
from rest_framework.authtoken.views import ObtainAuthToken, Token
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from users.forms import UserSignUpForm
from users.token import account_activation_token


class UserProfileView(views.APIView):
    """Handle creating and updating view sets"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    http_method_names = ['post']
    search_fields = ('name', 'email',)
    form_class = UserSignUpForm

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            print("FORM VALID", serializer.validated_data)
            user = serializer.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })
            print("YOOOO")
            to_email = serializer.data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return Response('We have sent you an email, please confirm your email address to complete registration')
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateAccountView(views.APIView):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = models.UserProfile.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return Response('Thank you for your email confirmation. Now you can login your account.')
        else:
            return Response('Activation link is invalid')


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'name': user.name})


class LogoutView(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response("Logged Out Successfully")
