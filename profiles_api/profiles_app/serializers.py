from rest_framework import serializers

from profiles_app.models import UserProfile, ProfileFeedItem


class TestSerializer(serializers.Serializer):
    """Serializer for UsersAPI View

    Args:
        Serializer (Serializer): Generic Serializer provided by rest_framework
    """
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        # fields ='__all__'
        fields = ('id', 'name', 'email', 'password')
        model = UserProfile
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }   
            }
        }
    
    def create(self, validated_data):
        name = validated_data['name']
        email = validated_data['email']
        password = validated_data['password']
        user = UserProfile.objects.create_user(name=name, email=email, password=password)
        return user
    
    def update(self, instance, validated_data):
        """Updates user data

        Args:
            instance (UserProfile): user data
            validated_data (dict): Validated input data
        """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        
        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializer for Profile Feed Item

    Args:
        serializers (Serializer): Generic serializer provided by rest framework
    """
    class Meta:
        model = ProfileFeedItem
        fields = '__all__'
        extra_kwargs = {
            'user_profile': {
                'read_only': True
            }
        }