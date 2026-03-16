import json

from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.models import User
from django.utils.text import get_valid_filename
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Avatar, Profile
from .serializers import (
    AvatarSerializer,
    AvatarUpdateSerializer,
    PasswordUpdateSerializer,
    ProfileSerializer,
)


class SignInAPIView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        username = body.get("username")
        password = body.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpAPIView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        name = body.get("name")
        username = body.get("username")
        password = body.get("password")

        try:
            user = User.objects.create_user(
                username=username, password=password
            )
            Profile.objects.create(user=user, fullName=name)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignOutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(
            profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def user_avatar_directory_path(instance: "Profile", filename: str) -> str:
    return f"avatars/user_{instance.user.pk}/{filename}"


class AvatarAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = AvatarUpdateSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data["avatar"]
            profile = Profile.objects.get(user=request.user)

            avatar, created = Avatar.objects.get_or_create(
                profile=profile, defaults={"alt": "avatar"}
            )

            filename = get_valid_filename(file.name)
            custom_path = user_avatar_directory_path(profile, filename)
            file.name = custom_path

            # avatar = Avatar.objects.create(alt=filename)
            avatar.src.save(custom_path, file, save=True)
            avatar.alt = filename
            avatar.save(update_fields=["src", "alt"])

            profile.avatar = avatar
            profile.save(update_fields=["avatar"])

            return Response(
                AvatarSerializer(avatar).data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordUpdateSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.data.get("newPassword"))
            user.save()
            update_session_auth_hash(request, user)
            return Response(
                data={"detail": "Пароль успешно изменён"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
