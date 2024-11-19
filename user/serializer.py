from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import TokenCreateSerializer
from user.models import Customer


class UserSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = Customer
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']


class UserLoginSerializer(TokenCreateSerializer):
    class Meta(TokenCreateSerializer):
        model = Customer
        fields = ['email', 'password']
