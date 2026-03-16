from django.urls import path

from .views import (
    SignUpAPIView,
    SignInAPIView,
    SignOutAPIView,
    ProfileAPIView,
    AvatarAPIView,
    PasswordUpdateAPIView,
)


app_name = "profiles"

urlpatterns = [
    path("sign-in/", SignInAPIView.as_view(), name="sign-in"),
    path("sign-up/", SignUpAPIView.as_view(), name="sign-up"),
    path("sign-out/", SignOutAPIView.as_view(), name="sign-out"),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path(
        "profile/avatar/",
        AvatarAPIView.as_view(),
        name="avatar-update",
    ),
    path(
        "profile/password/",
        PasswordUpdateAPIView.as_view(),
        name="password-update",
    ),
]
