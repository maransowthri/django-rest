from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    """Serializer for UsersAPI View

    Args:
        Serializer (Serializer): Generic Serializer provided by rest_framework
    """
    name = serializers.CharField(max_length=10)