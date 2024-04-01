from rest_framework.decorators import api_view
from django.db import transaction
from ..service.service_dish import *
from ..service.service_picture_url import get_pic_url
from ..utils.judgment_of_null_void import judgment_void, judgment_null
from ..utils.result import *
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json


# @csrf_exempt
@api_view(['POST'])
@transaction.atomic
def add_dish(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    required_void_fields = ['dishName', 'dishName', 'firstCategoryId', 'secondCategoryId', 'stockQuantity',
                            'dishStatus', 'dineInDisplayStatus', 'takeoutDisplayStatus', 'imageUrl', 'tagsList']
    required_null_fields = required_void_fields

    Res_boo1, Res_str1 = judgment_void(required_void_fields, request)  # 判断无字段类
    if not Res_boo1:
        return Result.error(Res_str1)

    Res_boo2, Res_str2 = judgment_null(required_null_fields, request)  # 判断空类
    if not Res_boo2:
        return Result.error(Res_str2)

    try:
        dish_dict = {
            # 前端获取项
            'dishName': request.data.get('dishName'),
            'stockQuantity': request.data.get('stockQuantity'),
            'dishStatus': request.data.get('dishStatus'),
            'dineInDisplayStatus': request.data.get('dineInDisplayStatus'),
            'takeoutDisplayStatus': request.data.get('takeoutDisplayStatus'),
            'imageUrl': request.data.get('imageUrl'),
            'firstCategoryId_id': request.data.get('firstCategoryId'),
            'secondCategoryId_id': request.data.get('secondCategoryId'),
            # 后端生成项
            'dishOrder': 1,  # 新增菜品默认排序为1
            'createdBy_id': 1,  # request.user.id,
            'restaurantId_id': 1,
            'createdAt': timezone.localtime(),  # + timezone.timedelta(hours=8)
        }

        dish = service_add_dish(dish_dict)
        service_add_dishTag(dish.id, json.loads(request.data.get('tagsList')))

    except Exception as e:
        transaction.set_rollback(True)  # 回执
        print(str(e))
        return Result.error('xx新建失败！请查看：' + str(e))
    return Result.success('xx新建完成！')


@api_view(['POST'])
@transaction.atomic
def update_dish(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    required_void_fields = ['dishId', 'dishName', 'dishName', 'firstCategoryId', 'secondCategoryId',
                            'stockQuantity', 'dishStatus', 'dineInDisplayStatus', 'takeoutDisplayStatus',
                            'imageUrl', 'tagsList']
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
            'dishName': request.data.get('dishName'),
            'firstCategoryId_id': request.data.get('firstCategoryId'),
            'secondCategoryId_id': request.data.get('secondCategoryId'),
            'stockQuantity': request.data.get('stockQuantity'),
            'dishStatus': request.data.get('dishStatus'),
            'dineInDisplayStatus': request.data.get('dineInDisplayStatus'),
            'takeoutDisplayStatus': request.data.get('takeoutDisplayStatus'),
            'imageUrl': request.data.get('imageUrl'),
            'lastUpdatedBy_id': 1,  # request.user.id,
            'updatedAt': timezone.localtime()  # + timezone.timedelta(hours=8)
        }

        service_update_dish(dish_dict)
        service_add_dishTag(dish_dict['id'], json.loads(request.data.get('tagsList')))
    except Exception as e:
        transaction.set_rollback(True)  # 回执
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
        service_delete_dish(id)  # 删除对应数据
        service_restart_order_dish()
        service_delete_dishTag(id)
    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xxx信息删除失败！请查看：' + str(e))
    return Result.success('xxx信息删除完成！')


@api_view(['POST'])
@transaction.atomic
def top_dish(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')

    if request.data.get('dishId') in ['', None]:
        return Result.error('dishId不能为空！')

    try:
        id = request.data.get('dishId')
        service_top_dish(id)
    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xxx信息删除失败！请查看：' + str(e))
    return Result.success('xxx信息删除完成！')


@api_view(['GET'])
def get_dish_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    try:
        query = {}
        dishName = request.GET.get('dishName')
        firstCategoryId = request.GET.get('firstCategoryId')
        if dishName:
            query['dishName__contains'] = dishName
        if firstCategoryId:
            query['firstCategoryId_id'] = firstCategoryId
    except:
        return Result.error('请检查输入项！')

    all_results_ = []
    dishList = Dish.objects.filter(**query)
    for dishOneContent in dishList:
        dish_id = dishOneContent.id
        exists_dish_tags = DishTag.objects.filter(dishId=dish_id)
        tagsList = [one.tag1 for one in exists_dish_tags]
        if dishOneContent.dishStatus:
            dishStatus_value = '在售'
        else:
            dishStatus_value = '停售'
        dish_and_tags_dict = {
            'dishId': dishOneContent.id,
            'dishOrder': dishOneContent.dishOrder,
            'dishName': dishOneContent.dishName,
            'firstCategoryId': dishOneContent.firstCategoryId.id,
            'firstCategoryName': dishOneContent.firstCategoryId.categoryName,
            'secondCategoryId': dishOneContent.secondCategoryId.id,
            'secondCategoryName': dishOneContent.secondCategoryId.categoryName,
            'stockQuantity': dishOneContent.stockQuantity,
            'dishStatusValue': dishStatus_value,
            'imageUrl': dishOneContent.imageUrl,
            'tagsListValue': ' '.join(tagsList),
            'tagsList': tagsList,
            'dishStatus': int(dishOneContent.dishStatus),
            'dineInDisplayStatus': int(dishOneContent.dineInDisplayStatus),
            'takeoutDisplayStatus': int(dishOneContent.takeoutDisplayStatus)
        }
        all_results_.append(dish_and_tags_dict)
    all_results = sorted(all_results_, key=lambda x: x['dishOrder'], reverse=False)
    paginator = Paginator(all_results, int(request.GET.get('pageSize', 10)))
    page_number = int(request.GET.get('page', 1))
    paginated_results = paginator.get_page(page_number)
    page_results = [result for result in paginated_results]

    return Result_page.success(data=page_results, paginator=paginator, page_number=page_number,
                               page_html='dishPage.html', request=request)


@api_view(['GET'])
def get_dish_class_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    try:
        query = {}
        firstCategoryId = request.GET.get('firstCategoryId')
        secondCategoryId = request.GET.get('secondCategoryId')
        if firstCategoryId:
            query['firstCategoryId_id'] = firstCategoryId
        if secondCategoryId:
            query['secondCategoryId_id'] = secondCategoryId
    except:
        return Result.error('请检查输入项！')
    # -------------第一 查询已经关联上的
    second_dict_ = {}
    dish_list = Dish.objects.filter(**query)
    for i, dish_one in enumerate(dish_list):
        firstCategoryName = dish_one.firstCategoryId.categoryName
        secondCategoryName = dish_one.secondCategoryId.categoryName
        key_new = secondCategoryName + '【' + firstCategoryName + '】'
        if key_new in second_dict_.keys():
            second_dict_[key_new].append(dish_one.dishName)
        else:
            second_dict_[key_new] = [
                dish_one.firstCategoryId.id, dish_one.secondCategoryId.id, dish_one.dishName
            ]
    all_results_ = []
    for key_s_f in second_dict_:
        all_results_.append({
            'first_id': second_dict_[key_s_f][0],
            'second_id': second_dict_[key_s_f][1],
            'secondCategoryName': key_s_f.split('【')[0],
            'firstCategoryName': key_s_f.split('【')[1][:-1],
            'dishNum': len(second_dict_[key_s_f]) - 2,
            'dishNameList': '、'.join(second_dict_[key_s_f][2:])
        })
    # 查询未关联上的
    fir_cate_list = FirstCategory.objects.filter()
    for fir_cate in fir_cate_list:
        dish_select_list = Dish.objects.filter(firstCategoryId_id=fir_cate.id)
        if len(dish_select_list) == 0:
            all_results_.append({
                'first_id': fir_cate.id,
                'second_id': 10000,  # 最大值
                'secondCategoryName': '-',
                'firstCategoryName': fir_cate.categoryName,
                'dishNum': 0,
                'dishNameList': ''
            })

    sec_cate_list = SecondCategory.objects.filter()
    for sec_cate in sec_cate_list:
        dish_select_list = Dish.objects.filter(secondCategoryId_id=sec_cate.id)
        if len(dish_select_list) == 0:
            all_results_.append({
                'first_id': 10000,
                'second_id': sec_cate.id,  # 最大值
                'secondCategoryName': sec_cate.categoryName,
                'firstCategoryName': '-',
                'dishNum': 0,
                'dishNameList': ''
            })

    all_results = sorted(all_results_, key=lambda x: x['first_id'], reverse=False)
    paginator = Paginator(all_results, int(request.GET.get('pageSize', 10)))
    page_number = int(request.GET.get('page', 1))
    paginated_results = paginator.get_page(page_number)
    page_results = [result for result in paginated_results]

    return Result_page.success(data=page_results, paginator=paginator, page_number=page_number,
                               page_html='dishClassPage.html', request=request)


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
