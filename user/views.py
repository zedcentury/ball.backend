from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import Pupil
from user.serializers import PupilsSerializer, LoginSerializer, UserSerializer


class LoginView(APIView):
    """
    Tizimga kirish
    """

    # permission_classes = [~IsAuthenticated]

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
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class PupilsView(ListAPIView):
    serializer_class = PupilsSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__first_name', 'user__last_name']

    def get_queryset(self):
        return Pupil.objects.prefetch_related('user')
