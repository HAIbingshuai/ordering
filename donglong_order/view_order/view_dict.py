from ..utils.result import Result, Result_page
from ..models import FirstCategory, SecondCategory, OrderStatus, Room,Week,Dish
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
def add_dict_data(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')

    categorytype = request.data.get('categorytype')
    categoryName = request.data.get('categoryName')
    if categoryName in ['', None] or categorytype in ['', None]:
        return Result.error('请检查，须有值categoryName！')
    try:
        new_dict = {
            'categoryName': categoryName
        }
        if int(categorytype) == 1:
            XXX = FirstCategory.objects.create(**new_dict)
        else:
            XXX = SecondCategory.objects.create(**new_dict)
    except Exception as e:
        return Result.error("新增失败!：" + str(e))
    return Result.success("分类新增成功!")


@api_view(['POST'])
# @authentication_classes([CustomTokenAuthentication])
# @permission_classes([IsAuthenticated])
@transaction.atomic
def update_dict_data(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    categoryId = request.data.get('categoryId')
    categorytype = request.data.get('categorytype')
    categoryName = request.data.get('categoryName')
    if categoryId in ['', None] or categoryName in ['', None] or categorytype in ['', None]:
        return Result.error('请检查，须有值categoryName！')
    try:
        new_dict = {
            'categoryName': categoryName
        }
        if categorytype == 1:
            FirstCategory.objects.filter(id=categoryId).update(**new_dict)
        else:
            SecondCategory.objects.create(id=categoryId).update(**new_dict)
    except Exception as e:
        return Result.error("管理账号创建失败!：" + str(e))
    return Result.success("管理账号创建成功!")


@api_view(['POST'])
# @authentication_classes([CustomTokenAuthentication])
# @permission_classes([IsAuthenticated])
@transaction.atomic
def del_dict_data(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    categoryId = int(request.data.get('categoryId'))
    categorytype = int(request.data.get('categorytype'))
    if categoryId in ['', None] or categorytype in ['', None]:
        return Result.error('请检查，categoryId、categorytype！')
    try:
        if categorytype == 1:
            FirstCategory.objects.filter(id=categoryId).delete()
        else:
            SecondCategory.objects.filter(id=categoryId).delete()
    except Exception as e:
        return Result.error("分类删除失败!：" + str(e))
    return Result.success("分类删除成功!")


@api_view(['GET'])
# @authentication_classes([CustomTokenAuthentication])
# @permission_classes([IsAuthenticated])
def get_dict_data_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    first_list = FirstCategory.objects.filter()
    all_list = []
    f_list = []
    for one in first_list:
        f_list.append({'categoryId': one.id,
                       "categorytype": 1,
                       "categoryName": one.categoryname,
                       })
    second_list = SecondCategory.objects.filter()
    s_list = []
    for one in second_list:
        s_list.append({'categoryId': one.id,
                       "categorytype": 2,
                       "categoryName": one.categoryname,
                       })
    all_list.append(f_list)
    all_list.append(s_list)
    return Result.success(data=all_list)


@api_view(['GET'])
def get_categoryId_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    first_list = FirstCategory.objects.filter()
    all_list = [
        {
            "firstCategoryId": one.id,
            "categoryName": one.categoryname,
        } for one in first_list
    ]
    return Result.success(data=all_list)


@api_view(['GET'])
def get_secCategoryId_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    first_list = SecondCategory.objects.filter()
    all_list = [
        {
            "secondCategoryId": one.id,
            "categoryName": one.categoryname,
        } for one in first_list
    ]
    return Result.success(data=all_list)


@api_view(['GET'])
def get_orderStatus_List(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    first_list = OrderStatus.objects.filter()
    all_list = [
        {
            "orderStatusId": one.id,
            "statusName": one.statusname,
        } for one in first_list
    ]
    return Result.success(data=all_list)


@api_view(['GET'])
def get_room_dict_List(request):
    """
    包间列表
    :param request:
    :return:
    """
    if request.method != 'GET':
        return Result.error('无效的请求方法')
    room_list = Room.objects.filter(~Q(id=5))
    all_list = [
        {
            "roomId": one.id,
            "roomName": one.roomname,
        } for one in room_list
    ]
    return Result.success(data=all_list)

@api_view(['GET'])
def get_weekid_List(request):

    if request.method != 'GET':
        return Result.error('无效的请求方法')
    week_list = Week.objects.filter()
    all_list = [
        {
            "weekId": one.id,
            "weekName": one.weekname,
        } for one in week_list
    ]
    return Result.success(data=all_list)


@api_view(['GET'])
def get_dish_list_dict(request):

    if request.method != 'GET':
        return Result.error('无效的请求方法')
    dish_list = Dish.objects.filter()
    all_list = [
        {
            "dishId": one.id,
            "dishName": one.dishname,
        } for one in dish_list
    ]
    return Result.success(data=all_list)




@api_view(['GET'])
def get_carousel_dict_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')
    all_list = [
        {
            "carouselId": 1,
            "carouselName": '环境图轮播',
        } ,
        {
            "carouselId": 2,
            "carouselName": '招牌菜轮播',
        }
    ]
    return Result.success(data=all_list)
