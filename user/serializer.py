from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

from user.models import Customer


class UserSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = Customer
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
