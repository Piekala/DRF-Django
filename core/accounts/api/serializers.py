"""Serializers da API de contas para entrada e saida JSON."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import UserProfile
from accounts.services import create_user_with_profile


class UserProfileSerializer(serializers.ModelSerializer):
    """Expone apenas os campos de perfil relevantes para a API."""

    class Meta:
        model = UserProfile
        fields = ('role', 'phone', 'department', 'bio')


class UserSerializer(serializers.ModelSerializer):
    """Serializa o usuario junto com seu perfil de negocio."""

    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile')


class UserCreateSerializer(serializers.Serializer):
    """Valida os dados minimos para cadastro de um novo usuario."""

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=UserProfile.Role.choices)
    phone = serializers.CharField(required=False, allow_blank=True)
    department = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        """Encaminha a criacao para a camada de servico."""
        return create_user_with_profile(**validated_data)

    def to_representation(self, instance):
        """Reaproveita o serializer de leitura para manter a saida consistente."""
        return UserSerializer(instance).data


class CurrentUserSerializer(serializers.ModelSerializer):
    """Serializer enxuto para o endpoint de usuario autenticado."""

    role = serializers.CharField(source='profile.role', read_only=True)
    phone = serializers.CharField(source='profile.phone', read_only=True)
    department = serializers.CharField(source='profile.department', read_only=True)
    bio = serializers.CharField(source='profile.bio', read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'phone',
            'department',
            'bio',
        )
