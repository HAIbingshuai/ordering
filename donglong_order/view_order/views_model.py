from rest_framework.decorators import api_view
from django.db import transaction
from ..utils.result import *
from django.core.paginator import Paginator


@api_view(['POST'])
# @authentication_classes([CustomTokenAuthentication])
# @permission_classes([IsAuthenticated])
@transaction.atomic
def add_xxx(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    # 获取数据
    xxx = request.data.get('xxx')
    try:
        # 执行数据
        print()

    except Exception as e:
        # 回执
        transaction.set_rollback(True)
        return Result.error('xx新建失败！请查看：' + str(e))
    return Result.success('xx新建完成！')


@api_view(['POST'])
# @authentication_classes([CustomTokenAuthentication])
# @permission_classes([IsAuthenticated])
@transaction.atomic
def add_xxx(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    # 获取数据
    xxx = request.data.get('xxx')
    try:
        # 执行数据
        print()

    except Exception as e:
        # 回执
        transaction.set_rollback(True)
        return Result.error('xxx信息更改失败！请查看：' + str(e))
    return Result.success('xxx信息更改完成！')


@api_view(['get'])
# @authentication_classes([CustomTokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_xxx_list(request):
    if request.method != 'get':
        return Result.error('无效的请求方法')

    xxx = request.GET.get('xxx')
    all_results = []

    paginator = Paginator(all_results, int(request.GET.get('pageSize', 10)))
    paginated_results = paginator.get_page(int(request.GET.get('page', 1)))
    page_results = [result for result in paginated_results]

    return Result_page.success(data=page_results, total=len(all_results))


@api_view(['get'])
# @authentication_classes([CustomTokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_xxx(request):
    if request.method != 'get':
        return Result.error('无效的请求方法')

    xxx = request.GET.get('xxx')
    all_results = {}

    return Result.success(data=all_results)
