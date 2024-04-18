from ..utils.result import Result, Result_page
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from ..models import OrderInfo, OrderDish
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import render


@api_view(['GET'])
def get_data(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')
    # 待处理订单量
    dcl_obj_list = OrderInfo.objects.filter(orderstatus=1)
    dcldd_num = len(dcl_obj_list)
    # 订单总量
    ddzl_obj_list = OrderInfo.objects.filter()
    ddzl_num = len(ddzl_obj_list)
    # 总接待人次,总包间预定个数     # 堂食与包间比例
    zjdrs, zbj_num, ztangshi_num = 0, 0, 0
    for one in ddzl_obj_list:
        if one.numberdiners:  # 就餐人数
            zjdrs += one.numberdiners
        else:
            zjdrs += 1
        if one.roomid.id == 5:  # 就餐包间
            ztangshi_num += 1
        else:
            zbj_num += 1
    # 本月订单数据
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    orders_per_day = OrderInfo.objects.filter(
        createdat__gte=thirty_days_ago,  # 筛选创建时间大于等于30天前的订单
        createdat__lte=today             # 筛选创建时间小于等于今天的订单
    ).annotate(
        order_count=Count('id')          # 统计每天订单的数量
    ).values(
        'createdat__date',  # 按日期进行分组
        'order_count'  # 统计的订单数
    ).order_by('createdat__date')  # 按日期升序排列
    orders_per_day_list = [[str(date['createdat__date']), date['order_count']] for date in orders_per_day]

    # 菜品欢迎程度排名
    top_dishes = OrderDish.objects.values('dishid__dishname').annotate(
        total_quantity=Sum('dishnum')
    ).order_by('-total_quantity')[:10]
    dish_love_list = [[str(dish['dishid__dishname']), dish['total_quantity']] for dish in top_dishes]

    # 包间欢迎程度排名
    top_rooms = OrderInfo.objects.filter(roomid__isnull=False).values('roomid__roomname').annotate(
        order_count=Count('id')
    ).order_by('-order_count')[:10]
    room_love_list = [[str(room['roomid__roomname']), room['order_count']] for room in top_rooms]

    data_all_dict = {
        'pendingOrderCount': dcldd_num,
        'totalOrderCount': ddzl_num,
        'totalGuestsCount': zjdrs,  # 总接待人次：
        'totalRoomReservationsCount': zbj_num,  # 总包间预定个数
        'dineInToRoomRatio': [zbj_num, ztangshi_num],  # 堂食与包间比例
        'currentMonthOrderData': orders_per_day_list,  # 本月订单数据
        'topRoomsByPopularity': room_love_list,  # 包间欢迎程度排名
        'topDishesByPopularity': dish_love_list  # 饭菜欢迎程度排名
    }

    # return Result_page.success(data=data_all_dict)
    context = {'user_count': data_all_dict['pendingOrderCount'], 'task_count': data_all_dict['totalOrderCount']}
    return render(request, 'dashboard.html', context)
