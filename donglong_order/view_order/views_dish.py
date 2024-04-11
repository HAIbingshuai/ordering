from rest_framework.decorators import api_view
from django.db import transaction

from ..models import *
from ..service.service_dish import *
from ..utils.judgment_of_null_void import judgment_void, judgment_null
from ..utils.result import *
from django.core.paginator import Paginator
from django.utils import timezone
import json


# @csrf_exempt
@api_view(['POST'])
@transaction.atomic
def add_dish(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    required_void_fields = ['dishName', 'dishName', 'firstcategoryid', 'secondcategoryid', 'stockQuantity',
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
            'firstcategoryid_id': request.data.get('firstcategoryid'),
            'secondcategoryid_id': request.data.get('secondcategoryid'),
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
    required_void_fields = ['dishid', 'dishName', 'dishName', 'firstcategoryid', 'secondcategoryid',
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
            'id': request.data.get('dishid'),
            'dishName': request.data.get('dishName'),
            'firstcategoryid_id': request.data.get('firstcategoryid'),
            'secondcategoryid_id': request.data.get('secondcategoryid'),
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

    required_void_fields = ['dishid', 'dishStatus']
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
            'id': request.data.get('dishid'),
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

    required_void_fields = ['dishid', 'dishOrder']
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
            'id': request.data.get('dishid'),
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
        return Result.error('dishid不能为空！')

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
    try:
        id = request.data.get('dishId')
        if id in ['', None]:
            return Result.error('dishid不能为空！')
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
        firstcategoryid = request.GET.get('firstCategoryId')
        if dishName:
            query['dishname__contains'] = dishName
        if firstcategoryid:
            query['firstcategoryid_id'] = firstcategoryid
    except:
        return Result.error('请检查输入项！')

    all_results_ = []
    dishList = Dish.objects.filter(**query)
    for dishOneContent in dishList:
        dish_id = dishOneContent.id
        exists_dish_tags = DishTag.objects.filter(dishid=dish_id)
        tagsList = [one.tag1 for one in exists_dish_tags]
        if dishOneContent.dishstatus:
            dishStatus_value = '在售'
        else:
            dishStatus_value = '停售'
        dish_and_tags_dict = {
            'dishId': dishOneContent.id,
            'dishOrder': dishOneContent.dishorder,
            'dishName': dishOneContent.dishname,
            'firstcategoryid': dishOneContent.firstcategoryid.id,
            'firstCategoryName': dishOneContent.firstcategoryid.categoryname,
            'secondcategoryid': dishOneContent.secondcategoryid.id,
            'secondCategoryName': dishOneContent.secondcategoryid.categoryname,
            'stockQuantity': dishOneContent.stockquantity,
            'dishStatusValue': dishStatus_value,
            'imageUrl': dishOneContent.imageurl,
            'tagsListValue': ' '.join(tagsList),
            'tagsList': tagsList,
            'dishStatus': int(dishOneContent.dishstatus),
            'dineInDisplayStatus': int(dishOneContent.dineindisplaystatus),
            'takeoutDisplayStatus': int(dishOneContent.takeoutdisplaystatus)
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
        firstcategoryid = request.GET.get('firstcategoryid')
        secondcategoryid = request.GET.get('secondcategoryid')
        if firstcategoryid:
            query['firstcategoryid_id'] = firstcategoryid
        if secondcategoryid:
            query['secondcategoryid_id'] = secondcategoryid
    except:
        return Result.error('请检查输入项！')
    # -------------第一 查询已经关联上的
    second_dict_ = {}
    dish_list = Dish.objects.filter(**query)
    for i, dish_one in enumerate(dish_list):
        firstCategoryName = dish_one.firstcategoryid.categoryname
        secondCategoryName = dish_one.secondcategoryid.categoryname
        key_new = secondCategoryName + '【' + firstCategoryName + '】'
        if key_new in second_dict_.keys():
            second_dict_[key_new].append(dish_one.dishname)
        else:
            second_dict_[key_new] = [
                dish_one.firstcategoryid.id, dish_one.secondcategoryid.id, dish_one.dishname
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
        dish_select_list = Dish.objects.filter(firstcategoryid_id=fir_cate.id)
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
        dish_select_list = Dish.objects.filter(secondcategoryid_id=sec_cate.id)
        if len(dish_select_list) == 0:
            all_results_.append({
                'first_id': 10000,
                'second_id': sec_cate.id,  # 最大值
                'secondCategoryName': sec_cate.categoryname,
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

    dish_id = request.GET.get('dishid')
    if not dish_id:
        return Result.error('请检查，dishid须有值！')
    dish_get_one = Dish.objects.filter(id=dish_id)
    if len(dish_get_one) == 0:
        return Result.error('无此菜品信息，请联系管理员！')

    dishOne = dish_get_one[0]
    exists_dish_tags = DishTag.objects.filter(dishid=dish_id)
    tagsList = [one.tag1 for one in exists_dish_tags]
    dish_and_tags_dict = {
        'id': dishOne.id,
        'dishName': dishOne.dishname,
        'firstCategory': {dishOne.firstcategoryid.id: dishOne.firstcategoryid.categoryName},
        'secondCategory': {dishOne.secondcategoryid.id: dishOne.secondcategoryid.categoryName},
        'stockQuantity': dishOne.stockQuantity,
        'dishStatus': dishOne.dishStatus,
        'imageUrl': dishOne.imageUrl,
        'tagsList': tagsList,
        'dineInDisplayStatus': dishOne.dineInDisplayStatus,
        'takeoutDisplayStatus': dishOne.takeoutDisplayStatus,
    }

    return Result.success(data=dish_and_tags_dict)


@api_view(['GET'])
def get_dish_weekly_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    weeklyDish_list = WeeklyDish.objects.filter()
    week_list = Week.objects.filter()
    WeekidDishname_dick = {}
    for one in weeklyDish_list:
        key_name = one.weekid.weekname + '-' + one.dayname
        if key_name in WeekidDishname_dick:
            WeekidDishname_dick[key_name].append([one.dishid.dishorder, one.dishid.dishname])
        else:
            WeekidDishname_dick[key_name] = [[one.dishid.dishorder, one.dishid.dishname]]

    all_results_ = []
    for week_obj in week_list:
        day_num = week_obj.weekname
        dish_list_three = []
        for day_time in ['早餐', '午餐', '晚餐']:
            key = day_num + '-' + day_time
            if key in WeekidDishname_dick:
                dish_list = WeekidDishname_dick[day_num + '-' + day_time]
            else:
                dish_list = []
            dish_list_three.append(dish_list)

        all_results_.append({
            'weekId': week_obj.id,
            'weekName': day_num,
            'day1Name': dish_list_three[0],
            'day2Name': dish_list_three[1],
            'day3Name': dish_list_three[2],
        })
    all_results = sorted(all_results_, key=lambda x: x['weekId'], reverse=False)
    paginator = Paginator(all_results, int(request.GET.get('pageSize', 10)))
    page_number = int(request.GET.get('page', 1))
    paginated_results = paginator.get_page(page_number)
    page_results = [result for result in paginated_results]

    return Result_page.success(data=page_results, paginator=paginator, page_number=page_number,
                               page_html='dishWeek.html', request=request)
