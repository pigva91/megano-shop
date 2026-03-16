from rest_framework import serializers

from .models import Profile, Avatar


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()
    alt = serializers.CharField(read_only=True)

    class Meta:
        model = Avatar
        fields = ("src", "alt")

    def get_src(self, obj):
        if obj and obj.src:
            return obj.src.url
        return ""


class AvatarUpdateSerializer(serializers.Serializer):
    avatar = serializers.ImageField()

    def validate_avatar(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError(
                "Аватар слишком большой. Максимальный размер — 2 МБ."
            )
        return value


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]


class PasswordUpdateSerializer(serializers.Serializer):
    currentPassword = serializers.CharField()
    newPassword = serializers.CharField()

    def validate_currentPassword(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Неверный текущий пароль")
        return value
