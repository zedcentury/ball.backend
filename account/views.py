from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import password_changed
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import LoginSerializer, UserSerializer, ChangePasswordSerializer, ProfileSerializer


class LoginView(APIView):
    """
    Tizimga kirish
    """

    permission_classes = [~IsAuthenticated]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        user = authenticate(username=serializer.validated_data.get('username'),
                            password=serializer.validated_data.get('password'))

        if user is None:
            raise ValidationError({'password': 'Login and/or password is incorrect'})

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })


class UserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(UpdateAPIView):
    """
    Foydalanuvchi parolini o'zgartirishi
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data.get('new_password'))
        user.save()
        password_changed(serializer.validated_data.get('new_password'), request.user)
        return Response({})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        obj = self.request.user
        serializer = ProfileSerializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(UserSerializer(instance).data)
