from django.core.paginator import Paginator
from django.utils import timezone
from rest_framework.decorators import api_view
from django.db import transaction
from ..models import Room, OrderInfo
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
            'roomname': request.data.get('roomName'),
            'roomconfiguration': request.data.get('roomConfiguration'),
            'roomlocation': request.data.get('roomLocation'),
            'status': request.data.get('status'),
            'createdby_id': 1,  # request.user.id,
            'createdat': timezone.localtime(),
            'restaurantid_id':1
        }
        room = service_add_room(room_dict)

    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('包间新建失败！请查看：' + str(e))
    return Result.success('包间新建完成！')


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
            'roomname': request.data.get('roomName'),
            'roomconfiguration': request.data.get('roomConfiguration'),
            'roomlocation': request.data.get('roomLocation'),
            'status': request.data.get('status'),
            'lastupdatedby_id': 1,  # request.user.id,
            'updatedat': timezone.localtime()
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

    roomId_value = request.data.get('roomId')
    if not roomId_value:
        Result.error('请检查，缺少roomId！')
    try:
        service_delete_room(roomId_value)
    except Exception as e:
        transaction.set_rollback(True)
        return Result.error('房间删除失败！请查看：' + str(e))
    return Result.success('房间删除完成！')


@api_view(['GET'])
def get_room_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')
    roomName = request.GET.get('roomName')
    all_results_ = []
    query = {}
    if roomName:
        query['roomname__contains'] = roomName
    roomList = Room.objects.filter(**query)
    for roomOneContent in roomList:
        room_one_dict = {
            'roomId': roomOneContent.id,
            'roomName': roomOneContent.roomname,
            'roomConfiguration': roomOneContent.roomconfiguration,
            'roomLocation': roomOneContent.roomlocation,
            'status': roomOneContent.status,
            'createdBy': roomOneContent.createdby.managername,
        }
        all_results_.append(room_one_dict)

    all_results = sorted(all_results_, key=lambda x: x['roomId'], reverse=False)
    paginator = Paginator(all_results, int(request.GET.get('pageSize', 10)))
    page_number = int(request.GET.get('page', 1))
    paginated_results = paginator.get_page(page_number)
    page_results = [result for result in paginated_results]

    return Result_page.success(data=page_results, paginator=paginator, page_number=page_number,
                               page_html='roomPage.html', request=request)


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
