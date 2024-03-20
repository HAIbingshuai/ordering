from rest_framework.decorators import api_view
from django.db import transaction
from ..service.service_dish import *
from ..service.service_picture_url import get_pic_url
from ..utils.judgment_of_null_void import judgment_void, judgment_null
from ..utils.result import *
from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render


@api_view(['POST'])
@transaction.atomic
def add_dish(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    # -------------------------
    # 第一部分：图片处理
    # 第二部分：dish建立
    # 第三部分：标签建立
    # -------------------------

    required_void_fields = ['dishName', 'dishName', 'firstCategoryId', 'secondCategoryId', 'stockQuantity',
                            'dishStatus',
                            'dineInDisplayStatus', 'takeoutDisplayStatus', 'image', 'tagsList']
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
        # @1
        imageUrl = get_pic_url(request.data.get('image'))
        dishOrder = 1
        dish_dict = {
            'dishOrder': dishOrder,  # 新增菜品默认排序为1
            'dishName': request.data.get('dishName'),
            'stockQuantity': request.data.get('stockQuantity'),
            'dishStatus': request.data.get('dishStatus'),
            'dineInDisplayStatus': request.data.get('dineInDisplayStatus'),
            'takeoutDisplayStatus': request.data.get('takeoutDisplayStatus'),
            'imageUrl': imageUrl,
            'createdAt': timezone.localtime(),  # + timezone.timedelta(hours=8)
            'firstCategoryId_id': request.data.get('firstCategoryId'),
            'secondCategoryId_id': request.data.get('secondCategoryId'),
            'createdBy_id': 1,  # request.user.id,
        }
        dish = service_add_dish(dish_dict)
        # @3
        service_add_dishTag(dish.id, request.data.get('tagsList'))

    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xx新建失败！请查看：' + str(e))
    return Result.success('xx新建完成！')


@api_view(['POST'])
@transaction.atomic
def update_dish(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    required_void_fields = ['dishId', 'dishName', 'dishName', 'firstCategoryId', 'secondCategoryId',
                            'stockQuantity', 'dishStatus', 'dineInDisplayStatus', 'takeoutDisplayStatus',
                            'image', 'tagsList']
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
        imageUrl = get_pic_url(request.data.get('image'))
        dish_dict = {
            'id': request.data.get('dishId'),
            'dishName': request.data.get('dishName'),
            'firstCategoryId_id': request.data.get('firstCategoryId'),
            'secondCategoryId_id': request.data.get('secondCategoryId'),
            'stockQuantity': request.data.get('stockQuantity'),
            'dishStatus': request.data.get('dishStatus'),
            'dineInDisplayStatus': request.data.get('dineInDisplayStatus'),
            'takeoutDisplayStatus': request.data.get('takeoutDisplayStatus'),
            'imageUrl': imageUrl,
            'lastUpdatedBy_id': 1,  # request.user.id,
            'updatedAt': timezone.localtime()  # + timezone.timedelta(hours=8)
        }

        service_update_dish(dish_dict)
        service_add_dishTag(dish_dict['id'], request.data.get('tagsList'))

    except Exception as e:
        # 回执
        transaction.set_rollback(True)
        return Result.error('xxx信息更改失败！请查看：' + str(e))
    return Result.success('xxx信息更改完成！')


@api_view(['POST'])
@transaction.atomic
def update_dish_status(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')

    required_void_fields = ['dishId', 'dishStatus']
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
        dish_dict = {
            'id': request.data.get('dishId'),
            'dishStatus': request.data.get('dishStatus'),
            'lastUpdatedBy_id': 1,  # request.user.id,
            'updatedAt': timezone.localtime()  # + timezone.timedelta(hours=8)
        }
        service_update_dish(dish_dict)
    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xxx信息更改失败！请查看：' + str(e))
    return Result.success('xxx信息更改完成！')


@api_view(['POST'])
@transaction.atomic
def update_dish_dishOrder(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')

    required_void_fields = ['dishId', 'dishOrder']
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
        dish_dict = {
            'id': request.data.get('dishId'),
            'dishOrder': request.data.get('dishOrder'),
            'lastUpdatedBy_id': 1,  # request.user.id,
            'updatedAt': timezone.localtime()  # + timezone.timedelta(hours=8)
        }
        service_update_dish_dishOrder(dish_dict)
    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xxx信息更改失败！请查看：' + str(e))
    return Result.success('xxx信息更改完成！')


@api_view(['POST'])
@transaction.atomic
def del_dish(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')

    if request.data.get('dishId') in ['', None]:
        return Result.error('dishId不能为空！')

    try:
        id = request.data.get('dishId')
        service_delete_dish(id)
        service_delete_dishTag(id)
    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xxx信息删除失败！请查看：' + str(e))
    return Result.success('xxx信息删除完成！')


@api_view(['GET'])
def get_dish_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')
    # try:
    #     query = {
    #         'dishName__contains': request.GET.get('dishName')
    #     }
    #     firstCategoryId = request.GET.get('firstCategoryId')
    #     if firstCategoryId:
    #         query['firstCategoryId_id'] = firstCategoryId
    # except:
    #     return Result.error('请检查输入项！')
    #
    # all_results = []
    # dishList = Dish.objects.filter(**query)
    # for dishOneContent in dishList:
    #     dish_id = dishOneContent.id
    #     exists_dish_tags = DishTag.objects.filter(dishId=dish_id)
    #     tagsList = [one.tag1 for one in exists_dish_tags]
    #     dish_and_tags_dict = {
    #         'dishId': dishOneContent.id,
    #         'dishName': dishOneContent.dishName,
    #         'firstCategoryName': dishOneContent.firstCategoryId.categoryName,
    #         'secondCategoryName': dishOneContent.secondCategoryId.categoryName,
    #         'stockQuantity': dishOneContent.stockQuantity,
    #         'dishStatus': dishOneContent.dishStatus,
    #         'imageUrl': dishOneContent.imageUrl,
    #         'tagsList': tagsList,
    #     }
    #     all_results.append(dish_and_tags_dict)
    # #
    # paginator = Paginator(all_results, int(request.GET.get('pageSize', 10)))
    # paginated_results = paginator.get_page(int(request.GET.get('page', 1)))
    # page_results = [result for result in paginated_results]
    #
    # return Result_page.success(data=page_results, total=len(all_results))
    data_list_json = [{'id': 1, 'name': 'hbs', 'status': 12},
                      {'id': 12, 'name': 'hbs1', 'status': 121},
                      {'id': 13, 'name': 'hbs21', 'status': 1112}]
    print()
    return render(request, 'dish_page.html', {'data_list': data_list_json})


@api_view(['GET'])
def get_dish(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    dish_id = request.GET.get('dishId')
    if not dish_id:
        return Result.error('请检查，dishId须有值！')
    dish_get_one = Dish.objects.filter(id=dish_id)
    if len(dish_get_one) == 0:
        return Result.error('无此菜品信息，请联系管理员！')

    dishOne = dish_get_one[0]
    exists_dish_tags = DishTag.objects.filter(dishId=dish_id)
    tagsList = [one.tag1 for one in exists_dish_tags]
    dish_and_tags_dict = {
        'id': dishOne.id,
        'dishName': dishOne.dishName,
        'firstCategory': {dishOne.firstCategoryId.id: dishOne.firstCategoryId.categoryName},
        'secondCategory': {dishOne.secondCategoryId.id: dishOne.secondCategoryId.categoryName},
        'stockQuantity': dishOne.stockQuantity,
        'dishStatus': dishOne.dishStatus,
        'imageUrl': dishOne.imageUrl,
        'tagsList': tagsList,
        'dineInDisplayStatus': dishOne.dineInDisplayStatus,
        'takeoutDisplayStatus': dishOne.takeoutDisplayStatus,
    }

    return Result.success(data=dish_and_tags_dict)
