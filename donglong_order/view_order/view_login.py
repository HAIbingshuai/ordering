from django.utils import timezone
from datetime import timedelta
from ..utils.CustomTokenAuthentication import create_or_get_token
from ..utils.result import Result
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from ..utils.CustomTokenAuthentication import CustomTokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from mini_invitation_administrate.models import MiniAdmin
from ..models import Manager


@api_view(['POST'])
def admin_login(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        manager = Manager.objects.get(userName=username)
    except Manager.DoesNotExist:
        return Result.error('此管理员不存在！')

    # 账号密码不对
    if manager.userPassword != password:
        return Result.error('账号/密码不对！请检查核对。')

    now_time = timezone.localtime()
    expires = now_time + timedelta(hours=3)
    token, created = create_or_get_token(manager, expires)
    return Result.success({'token': token.key, 'managerId': manager.id})
