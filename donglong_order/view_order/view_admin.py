from ..utils.judgment_of_null_void import judgment_void, judgment_null
from ..utils.result import Result, Result_page
from ..models import *
from django.db.models import Q
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.core.paginator import Paginator
from django.utils import timezone


@api_view(['POST'])
# @authentication_classes([CustomTokenAuthentication])
# @permission_classes([IsAuthenticated])
@transaction.atomic
def add_admin(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')

    required_void_fields = ['managerName', 'userName', 'userPassword', 'phone']
    required_null_fields = required_void_fields
    Res_boo1, Res_str1 = judgment_void(required_void_fields, request)
    if not Res_boo1: return Result.error(Res_str1)
    Res_boo2, Res_str2 = judgment_null(required_null_fields, request)
    if not Res_boo2: return Result.error(Res_str2)

    managerName = request.data.get('managerName')
    user_name = request.data.get('userName')
    user_password = request.data.get('userPassword')
    phone = request.data.get('phone')

    managerList = Manager.objects.filter(userName=user_name)
    if len(managerList) > 0:
        return Result.error('管理账号已存在（userName同名）已经有了，请重新输入一个！')

    try:
        manager_dict = {
            'managerName': managerName,
            'userName': user_name,
            'userPassword': user_password,
            'phone': phone,
            'createdBy_id': 1,  # request.user.id,
            'createdAt': timezone.localtime()
        }
        manager = Manager.objects.create(**manager_dict)
    except Exception as e:
        return Result.error("管理账号创建失败!：" + str(e))
    return Result.success("管理账号创建成功!")


@api_view(['POST'])
# @authentication_classes([CustomTokenAuthentication])
# @permission_classes([IsAuthenticated])
@transaction.atomic
def del_admin(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    # 必填项
    manager_id = request.data.get('managerId')
    if manager_id in ['', None]:
        return Result.error('name不能为空！')
    try:
        Manager.objects.filter(id=manager_id).delete()
    except:
        return Result.error('删除失败请检查！')
    return Result.success('管理员已删除成功!')


@api_view(['GET'])
# @authentication_classes([CustomTokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_admin_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    managerName = request.GET.get('managerName')
    query = Q()  # 初始化一个空的查询对象
    if managerName:
        query &= Q(managerName__icontains=managerName)

    Manager_list = Manager.objects.filter(query)
    result_admin_list = []
    for one in Manager_list:
        result_admin_list.append({'managerId': one.id,
                                  "managerName": one.managerName,
                                  "userName": one.userName,
                                  "createdByName": one.createdBy.managerName,
                                  "createdAt": one.createdAt,
                                  "phone": one.phone,
                                  })

    paginator = Paginator(result_admin_list, int(request.GET.get('pageSize', 10)))
    paginated_results = paginator.get_page(int(request.GET.get('page', 1)))
    paginated_final = [one for one in paginated_results]
    return Result_page.success(data=paginated_final, total=len(result_admin_list))


@api_view(['GET'])
# @authentication_classes([CustomTokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_admin(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    manager_id = request.GET.get('managerId')
    if manager_id is None:
        return Result.error('admin_id不能为空！')

    managerList = Manager.objects.filter(id=manager_id)
    if len(managerList) == 0:
        return Result.error('查无此管理员信息！')

    one = managerList[0]
    mini_admin_content = {
        'managerId': one.id,
        "managerName": one.managerName,
        "userName": one.userName,
        "createdByName": one.createdBy.managerName,
        "createdAt": one.createdAt,
        "phone": one.phone,
    }
    return Result.success(mini_admin_content)
