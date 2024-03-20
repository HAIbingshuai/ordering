from django.core.paginator import Paginator
from django.utils import timezone
from rest_framework.decorators import api_view
from django.db import transaction
from ..models import Room, Order
from ..service.service_room import *
from ..utils.judgment_of_null_void import *
from ..utils.result import *


@api_view(['POST'])
@transaction.atomic
def add_room(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')

    required_void_fields = ['roomName', 'roomConfiguration', 'roomLocation', 'status']
    required_null_fields = required_void_fields
    # 判断无字段类
    Res_boo1, Res_str1 = judgment_void(required_void_fields, request)
    if not Res_boo1:
        return Result.error(Res_str1)
    # 判断空类
    Res_boo2, Res_str2 = judgment_null(required_null_fields, request)
    if not Res_boo2:
        return Result.error(Res_str2)

    try:
        room_dict = {
            'roomName': request.data.get('roomName'),
            'roomConfiguration': request.data.get('roomConfiguration'),
            'roomLocation': request.data.get('roomLocation'),
            'status': request.data.get('status'),
            'createdBy_id': 1,  # request.user.id,
            'createdAt': timezone.localtime()
        }
        room = service_add_room(room_dict)

    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xx新建失败！请查看：' + str(e))
    return Result.success('xx新建完成！')


@api_view(['POST'])
@transaction.atomic
def update_room(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')

    required_void_fields = ['roomId', 'roomName', 'roomConfiguration', 'roomLocation', 'status']
    required_null_fields = required_void_fields
    # 判断无字段类
    Res_boo1, Res_str1 = judgment_void(required_void_fields, request)
    if not Res_boo1:
        return Result.error(Res_str1)
    # 判断空类
    Res_boo2, Res_str2 = judgment_null(required_null_fields, request)
    if not Res_boo2:
        return Result.error(Res_str2)

    try:
        room_dict = {
            'id': request.data.get('roomId'),
            'roomName': request.data.get('roomName'),
            'roomConfiguration': request.data.get('roomConfiguration'),
            'roomLocation': request.data.get('roomLocation'),
            'status': request.data.get('status'),
            'lastUpdatedBy_id': 1,  # request.user.id,
            'updatedAt': timezone.localtime()
        }
        service_update_room(room_dict)

    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xx更新失败！请查看：' + str(e))
    return Result.success('xx更新完成！')


@api_view(['POST'])
@transaction.atomic
def update_room_status(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    if request.data.get('status') in ['', None]:
        Result.error('请检查，缺少status值！')
    try:
        room_dict = {
            'id': request.data.get('roomId'),
            'status': request.data.get('status'),
        }
        service_update_room(room_dict)
    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xx状态更新失败！请查看：' + str(e))
    return Result.success('xx状态更新！')


@api_view(['POST'])
@transaction.atomic
def del_room(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    if not request.data.get('roomId'):
        Result.error('请检查，缺少roomId！')
    try:
        service_delete_room(request.data.get('roomId'))
    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xx删除失败！请查看：' + str(e))
    return Result.success('xx删除完成！')


@api_view(['GET'])
def get_room_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    try:
        roomName = request.GET.get('roomName')
    except:
        return Result.error('请检查输入项！')
    all_results = []
    roomList = Room.objects.filter(**{'roomName__contains': roomName})
    for roomOneContent in roomList:
        dish_and_tags_dict = {
            'roomId': roomOneContent.id,
            'roomName': roomOneContent.roomName,
            'roomConfiguration': roomOneContent.roomConfiguration,
            'roomLocation': roomOneContent.roomLocation,
            'status': roomOneContent.status,
            'createdBy': roomOneContent.createdBy.managerName,
        }
        all_results.append(dish_and_tags_dict)
    #
    paginator = Paginator(all_results, int(request.GET.get('pageSize', 10)))
    paginated_results = paginator.get_page(int(request.GET.get('page', 1)))
    page_results = [result for result in paginated_results]
    #
    return Result_page.success(data=page_results, total=len(all_results))


@api_view(['GET'])
def get_room(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')
    room_id = request.GET.get('roomId')
    if not room_id:
        return Result.error('请检查，roomId须有值！')
    room_get_one = Room.objects.filter(id=room_id)
    if len(room_get_one) == 0:
        return Result.error('无此房间信息，请联系管理员！')
    room = room_get_one[0]
    room_dict = {
        'id': room.id,
        'roomName': room.roomName,
        'roomConfiguration': room.roomConfiguration,
        'roomLocation': room.roomLocation,
        'status': room.status,
        'createdBy': room.createdBy.managerName,
        'createdAt': room.createdAt,
    }
    return Result_page.success(data=room_dict)


@api_view(['GET'])
def get_usage_of_room(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    room_id = request.GET.get('roomId')
    if not room_id:
        return Result.error('请检查，roomId须有值！')

    room_usage_time_list = []
    orderList = Order.objects.filter(**{'roomId__id': room_id})
    for order in orderList:
        room_usage_time_list.append([order.scheduledDate, order.scheduledTimeStart,
                                     order.scheduledTimeEnd])
    room_dict = {
        'id': str(room_id),
        'room_usage_time_list': room_usage_time_list,
    }
    return Result_page.success(data=room_dict)
