from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import UniqueValidator


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message="Email already exists")]
    )
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone','image', 'password']
        extra_kwargs = {
            'password': {'write_only':True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        
        
