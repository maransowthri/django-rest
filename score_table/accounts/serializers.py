from rest_framework import serializers

from accounts.models import UserProfile, UserScoreTable


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'email', 'password')
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
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class UserScoreTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScoreTable
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }