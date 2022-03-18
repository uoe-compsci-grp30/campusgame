from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    # TODO: Provide a full profile_picture url

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "profile_picture"]
