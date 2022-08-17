# -*- coding:utf-8 -*-
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
        token['is_staff'] = user.is_staff

        # 주의 : 익명의 아이디로 접속하면 수산과학관으로 자동으로 변경 !
        if user.username == 'anonymous':
            token['user_id'] = 5

        return token


