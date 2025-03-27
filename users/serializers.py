from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration with password hashing."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password", "role", "phone_number")

    def create(self, validated_data):
        """Create user with hashed password and auto-generated username if missing."""
        username = validated_data.get("username")
        if not username:
            validated_data["username"] = validated_data["email"].split("@")[0]

        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            role=validated_data["role"],
            phone_number=validated_data.get("phone_number"),
        )
        user.set_password(validated_data["password"])  # Hash password
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer for JWT tokens to include additional user data."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["email"] = user.email
        token["phone_number"] = user.phone_number if user.phone_number else ""
        return token
