from rest_framework import serializers

from user.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'user_type']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6, max_length=50, error_messages={
        "min_length": "Password must contain at least 6 characters",
        "max_length": "The password can be a maximum of 50 characters"
    })
    confirm_password = serializers.CharField(required=True, min_length=6, max_length=50, error_messages={
        "min_length": "Password must contain at least 6 characters",
        "max_length": "The password can be a maximum of 50 characters"
    })

    def validate(self, data):
        errors = {}
        if not self.context.get('user').check_password(data.get('old_password')):
            errors['old_password'] = "The password was entered incorrectly"

        if data.get('new_password') != data.get('confirm_password'):
            errors['confirm_password'] = "Passwords are not entered the same"

        if data.get('new_password') == data.get('old_password'):
            errors['new_password'] = "The password is the same as the current password"

        if errors:
            raise serializers.ValidationError(errors)

        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
