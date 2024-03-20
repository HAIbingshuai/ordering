from rest_framework.authentication import BaseAuthentication
from ..models import AuthtokenTokenAdmin
from django.utils import timezone


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token_key = request.META.get('HTTP_AUTHORIZATION')
        if not token_key:
            return None
        try:
            token = AuthtokenTokenAdmin.objects.get(key=token_key)
        except AuthtokenTokenAdmin.DoesNotExist:
            return None
        now_time = timezone.localtime() + timezone.timedelta(hours=8)
        if token.expires < now_time:
            return None
        return (token.user, token)


def generate_new_token(user, expires):
    # 在这里添加重新生成令牌的逻辑
    new_token, created = AuthtokenTokenAdmin.objects.get_or_create(
        manager =user,
        defaults={'expires': expires}
    )
    return new_token, created


def create_or_get_token(user, expires):
    try:
        token = AuthtokenTokenAdmin.objects.get(manager=user)
        now_time = timezone.localtime()
        if token.expires < now_time:  # 检查令牌是否过期
            token.delete()  # 删除过期令牌
            return generate_new_token(user, expires)
        return token, False  # 返回现有令牌
    except AuthtokenTokenAdmin.DoesNotExist:
        return generate_new_token(user, expires)  # 创建新令牌
