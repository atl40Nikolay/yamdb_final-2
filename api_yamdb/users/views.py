from core.utils import sendmail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import (AdminCreateUser, ConfCodeSerializer,
                          SignupSerializer, UserMeSerializer)


class SignupView(APIView, LimitOffsetPagination):

    permission_classes = (AllowAny, )

    def post(self, request):
        if request.user.is_anonymous:
            use_name = request.data.get('usernme')
            use_email = request.data.get('email')
            for use in CustomUser.objects.filter(username=use_name,
                                                 email=use_email):
                confirmation_code = default_token_generator.make_token(use)
                sendmail(use_email, confirmation_code)
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            email = serializer.validated_data.get('email')
            user = get_object_or_404(CustomUser,
                                     username=serializer.data.get('username'))
            confirmation_code = default_token_generator.make_token(user)
            sendmail(email, confirmation_code)
        return Response(serializer.validated_data,
                        status=status.HTTP_200_OK)


class ConfirmRegisteredView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = ConfCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(CustomUser,
                                 username=serializer.data.get('username'))
        if default_token_generator.check_token(
                user, serializer.validated_data['confirmation_code']):
            user.save()
            token = user.get_tokens_for_user()['access']
            return Response(token, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AdmCreateUser(APIView, LimitOffsetPagination):
    permission_classes = (IsAuthenticated, )
    slug_field = 'username'

    def post(self, request):
        if request.user.is_admin or request.user.is_superuser:
            serializer = AdminCreateUser(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.validated_data,
                            status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def get(self, request, username=None):
        if username and username != 'me' and request.user.is_admin:
            user = get_object_or_404(CustomUser, username=username)
            serializer = AdminCreateUser(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif username == 'me':
            user = get_object_or_404(CustomUser,
                                     username=request.user.username)
            serializer = AdminCreateUser(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.is_admin or request.user.is_superuser:
            users = CustomUser.objects.all()
            results = self.paginate_queryset(users, request, view=self)
            serializer = AdminCreateUser(results, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, username=None):
        if request.user.is_admin and username != 'me':
            user = get_object_or_404(CustomUser, username=username)
            serializer = AdminCreateUser(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.validated_data)
        elif username == 'me':
            user = get_object_or_404(CustomUser,
                                     username=request.user.username)
            if not request.user.is_admin:
                user = request.user
                serializerme = UserMeSerializer(user, data=request.data,
                                                partial=True)
                serializerme.is_valid(raise_exception=True)
                serializerme.save()
                return Response(serializerme.data)
            else:
                serializer = AdminCreateUser(user, data=request.data,
                                             partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.validated_data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, username=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, username=None):
        if username == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if request.user.is_admin or request.user.is_superuser:
            user = get_object_or_404(CustomUser, username=username)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
