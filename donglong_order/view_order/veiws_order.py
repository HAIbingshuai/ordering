from rest_framework.decorators import api_view
from django.db import transaction
from ..service.service_order import *
from ..service.service_picture_url import get_orderNumber
from ..utils.judgment_of_null_void import *
from ..utils.result import *
from django.core.paginator import Paginator
from ..models import Order, OrderDish
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone


@api_view(['POST'])
@transaction.atomic
def add_order(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    # orderNumber、orderStatus、createdAt
    required_void_fields = ['userId', 'roomId', 'scheduledDate',
                            'scheduledTimeStart', 'scheduledTimeEnd',
                            'bz', 'numberDiners']
    required_null_fields = ['userId', 'scheduledDate', 'scheduledTimeStart',
                            'scheduledTimeEnd']
    # 判断无字段类
    Res_boo1, Res_str1 = judgment_void(required_void_fields, request)
    if not Res_boo1:
        return Result.error(Res_str1)
    # 判断空类
    Res_boo2, Res_str2 = judgment_null(required_null_fields, request)
    if not Res_boo2:
        return Result.error(Res_str2)

    try:
        order_dict = {
            'userId_id': request.data.get('userId'),
            'roomId_id': request.data.get('roomId'),
            'scheduledDate': request.data.get('scheduledDate'),
            'scheduledTimeStart': request.data.get('scheduledTimeStart'),
            'scheduledTimeEnd': request.data.get('scheduledTimeEnd'),
            'bz': request.data.get('bz'),
            'numberDiners': request.data.get('numberDiners'),
            'orderNumber': get_orderNumber(),  # # uuid
            'createdAt': timezone.localtime(),  # + timezone.timedelta(hours=8)
            'orderStatus_id': 1,
        }
        if request.data.get('roomId'):
            order_dict['roomId_id'] = request.data.get('roomId')
        order = service_add_Order(order_dict)
        #  #  #
        order_dish_dict = request.data.get('dishContents')  # [{'dishId':xx, 'dishNum': xx},{},{}]
        order_id = order.id
        service_add_Order_Dish(order_id, order_dish_dict)

    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xx新建失败！请查看：' + str(e))
    return Result.success('xx新建完成！')


@api_view(['POST'])
@transaction.atomic
def update_order_status(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    try:
        order_id = request.data.get('orderId')
        orderStatus = request.data.get('orderStatus')
        if not (id and orderStatus):
            return Result.error('请检查，orderId、orderStatus不能为空！')
    except:
        return Result.error('请检查，缺少orderId、orderStatus！')

    try:
        order_dict = {
            'id': order_id,
            'orderStatus_id': orderStatus,
            'lastUpdatedBy_id': 1,  # request.user.id,
            'updatedAt': timezone.localtime()  # + timezone.timedelta(hours=8)
        }
        service_update_order(order_dict)
    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xxx状态更改失败！请查看：' + str(e))
    return Result.success('xxx状态更改完成！')


@api_view(['GET'])
# @authentication_classes([CustomTokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_order_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    order_number = request.GET.get('orderNumber')  # 订单编号
    created_at_start = request.GET.get('createdAtStart')  # 下单开始日期
    created_at_end = request.GET.get('createdAtEnd')  # 下单结束日期
    order_status = request.GET.get('orderStatusId')  # 订单状态

    # 构建查询条件
    query_params = {}
    if order_number:
        query_params['ordernumber__icontains'] = order_number
    if created_at_start and created_at_end:
        query_params['createdat__gte'] = created_at_start
        query_params['createdat__lte'] = created_at_end
    else:
        # 一周之内
        one_week_ago = timezone.now() - timedelta(days=30)
        query_params['createdat__gte'] = one_week_ago

    if order_status:
        query_params['orderstatus_id'] = order_status
    query_params['roomid_id'] = 5  # 堂食

    # 执行查询
    orderList = Order.objects.filter(**query_params)
    # 订单状态字典表
    orderStatusDict = service_orderStatusDict()

    # 订单查询
    all_results_ = []
    for orderOneContent in orderList:
        # 菜品关联表-获取订单所有关联菜品
        order_dict = {
            'orderId': orderOneContent.id,
            'orderNumber': orderOneContent.ordernumber,
            'userName': orderOneContent.userid.username,
            'createdAt': orderOneContent.createdat.strftime('%Y-%m-%d %H:%M:%S'),
            'phoneNumber': orderOneContent.userid.phonenumber,
            'orderDishNum': len(OrderDish.objects.filter(orderid=orderOneContent.id)),
            'roomName': orderOneContent.roomid.roomname,
            'roomLocation': orderOneContent.roomid.roomlocation,
            'orderStatus': orderOneContent.orderstatus.id,
            'orderStatusValue': orderStatusDict[orderOneContent.orderstatus.id],
            'scheduledTime': orderOneContent.scheduleddate.strftime('%Y-%m-%d'),
            'scheduledTimeStart': orderOneContent.scheduledtimestart.strftime('%H:%M:%S'),
            'scheduledTimeEnd': orderOneContent.scheduledtimeend.strftime('%H:%M:%S')
        }
        all_results_.append(order_dict)
    all_results = sorted(all_results_, key=lambda x: x['createdAt'], reverse=True)
    paginator = Paginator(all_results, int(request.GET.get('pageSize', 10)))
    page_number = int(request.GET.get('page', 1))
    paginated_results = paginator.get_page(page_number)
    page_results = [result for result in paginated_results]
    return Result_page.success(data=page_results, paginator=paginator, page_number=page_number,
                               page_html='orderPage.html', request=request)


@api_view(['GET'])
def get_dish_list_by_orderId(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    orderId = request.GET.get('orderId')  # 订单编号
    if orderId in [None, '', 'Nona']:
        return []
    orderdish_list = OrderDish.objects.filter(orderId=orderId)
    return_data_ = [
        {'dishOrder': orderdish.dishId.dishOrder,
         'dish': orderdish.dishId.id,
         'dishName': orderdish.dishId.dishName,
         'firstcategoryName': orderdish.dishId.firstCategoryId.categoryName,
         'secondcategoryName': orderdish.dishId.secondCategoryId.categoryName,
         'dishNum': orderdish.dishNum
         }
        for orderdish in orderdish_list
    ]
    return_data = sorted(return_data_, key=lambda x: x['dishOrder'], reverse=False)
    return Result.success(return_data)


@api_view(['GET'])
def get_orderandroom_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    order_number = request.GET.get('orderNumber')  # 订单编号
    created_at_start = request.GET.get('createdAtStart')  # 下单开始日期
    created_at_end = request.GET.get('createdAtEnd')  # 下单结束日期
    order_status = request.GET.get('orderStatusId')  # 订单状态
    roomId = request.GET.get('roomId')  # 房间名称

    # 构建查询条件
    query = Q()
    if order_number:
        query &= Q(ordernumber__icontains=order_number)

    if created_at_start and created_at_end:
        query &= Q(createdat__gte=created_at_start)
        query &= Q(createdat__lte=created_at_end)
    else:
        one_week_ago = timezone.now() - timedelta(days=30)
        query &= Q(createdat__gte=one_week_ago)

    if order_status:
        query &= Q(orderstatus_id=order_status)
    if roomId:
        query &= Q(roomid_id=roomId)
    else:
        query &= ~Q(roomid_id=5)

    # 执行查询
    orderList = Order.objects.filter(query)
    # 订单状态字典表
    orderStatusDict = service_orderStatusDict()
    # 订单查询
    all_results_ = []
    for orderOneContent in orderList:
        order_dict = {
            'orderId': orderOneContent.id,
            'orderNumber': orderOneContent.ordernumber,
            'userName': orderOneContent.userid.username,
            'phoneNumber': orderOneContent.userid.phonenumber,
            'createdAt': orderOneContent.createdat.strftime('%Y-%m-%d %H:%M:%S'),
            'orderDishNum': len(OrderDish.objects.filter(orderid=orderOneContent.id)),
            'roomName': orderOneContent.roomid.roomname,
            'roomLocation': orderOneContent.roomid.roomlocation,
            'orderStatus': orderOneContent.orderstatus.id,
            'numberDiners': orderOneContent.numberdiners,  # 就餐人数
            'scheduledDate': orderOneContent.scheduleddate.strftime('%Y-%m-%d'),  # 就餐日期
            'scheduledDateTime': orderOneContent.scheduledtimestart.strftime(
                '%H:%M:%S') + '-' + orderOneContent.scheduledtimeend.strftime('%H:%M:%S'),
            'orderStatusValue': orderStatusDict[orderOneContent.orderstatus.id],
            'bz': orderOneContent.bz,
        }
        all_results_.append(order_dict)
    all_results = sorted(all_results_, key=lambda x: x['createdAt'], reverse=True)
    paginator = Paginator(all_results, int(request.GET.get('pageSize', 10)))
    page_number = int(request.GET.get('page', 1))
    paginated_results = paginator.get_page(page_number)
    page_results = [result for result in paginated_results]

    return Result_page.success(data=page_results, paginator=paginator, page_number=page_number,
                               page_html='orderRoomPage.html', request=request)


@api_view(['GET'])
# @authentication_classes([CustomTokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_order(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    order_id = request.GET.get('orderId')  # 订单编号
    order_one_get = Order.objects.filter(id=order_id)
    if len(order_one_get) == 0:
        return Result.error('查无此订单信息！')

    order_one = order_one_get[0]
    OrderDish_list = OrderDish.objects.filter(orderId=order_one.id)
    dish_contents = [
        {'dishOrder': orderdish_one.dishId.dishOrder,
         'dishName': orderdish_one.dishId.dishName,
         'firstCategoryId': orderdish_one.dishId.firstCategoryId.id,
         'firstCategoryName': orderdish_one.dishId.firstCategoryId.categoryName,
         'dishNum': orderdish_one.dishNum} for orderdish_one in OrderDish_list]
    order_dict = {
        'orderId': order_one.id,  # id
        'orderNumber': order_one.orderNumber,  # 编号
        'userName': order_one.userid.userName,  # 用户
        'phoneNumber': order_one.userid.phoneNumber,  # 手机号
        'orderStatusId': order_one.orderstatus.id,  # 订单状态
        'statusName': order_one.orderStatus.statusname,  # 订单状态
        'dishContents': dish_contents,  # 菜品信息
        'bz': order_one.bz,  # 备注
        'numberDiners': order_one.numberDiners,  # 就餐人数
        'scheduledDate': order_one.scheduledDate,  # 就餐日期
        'scheduledTimeStart': order_one.scheduledTimeStart,  # 就餐日期
        'scheduledTimeEnd': order_one.scheduledTimeEnd,  # 就餐日期
        'roomName': order_one.roomId.roomname,  # 房间名
    }
    return Result.success(data=order_dict)


@api_view(['POST'])
@transaction.atomic
def del_order(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')

    if request.data.get('orderId') in ['', None]:
        return Result.error('orderId不能为空！')

    try:
        order_id = request.data.get('orderId')
        service_delete_order(order_id)
        service_delete_order_dish(order_id)
    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xxx信息删除失败！请查看：' + str(e))
    return Result.success('xxx信息删除完成！')
