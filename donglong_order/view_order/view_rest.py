from rest_framework.decorators import api_view
from django.db import transaction
from ..service.service_rest import *
from ..utils.judgment_of_null_void import judgment_void, judgment_null
from ..utils.result import *
from django.core.paginator import Paginator
from django.utils import timezone
from ..models import Restaurant, RestaurantCarousel


@api_view(['GET'])
def get_restaurant_carousel_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')
    all_results_ = []
    restaurantCarouselList = RestaurantCarousel.objects.filter()
    for restCarOneContent in restaurantCarouselList:
        room_one_dict = {
            'carouselId': restCarOneContent.id,
            'carouselname': restCarOneContent.carouselname,
            'carouselimageurl': restCarOneContent.carouselimageurl,
            'carouseltimerange': restCarOneContent.carouseltimerange,
            'publishedat': restCarOneContent.publishedat.strftime('%Y-%m-%d %H:%M:%S'),
            'createdby': restCarOneContent.createdby.managername,
            'carouseltype': restCarOneContent.carouseltype,
        }
        all_results_.append(room_one_dict)

    all_results = sorted(all_results_, key=lambda x: x['carouseltype'], reverse=False)
    paginator = Paginator(all_results, int(request.GET.get('pageSize', 10)))
    page_number = int(request.GET.get('page', 1))
    paginated_results = paginator.get_page(page_number)
    page_results = [result for result in paginated_results]

    return Result_page.success(data=page_results, paginator=paginator, page_number=page_number,
                               page_html='restaurant.html', request=request)


@api_view(['POST'])
@transaction.atomic
def add_carousel(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    required_void_fields = ['addCarouselName', 'carouselType', 'timeRange', 'imageUrl']
    required_null_fields = required_void_fields
    Res_boo1, Res_str1 = judgment_void(required_void_fields, request)  # 判断无字段类
    if not Res_boo1:
        return Result.error(Res_str1)
    Res_boo2, Res_str2 = judgment_null(required_null_fields, request)  # 判断空类
    if not Res_boo2:
        return Result.error(Res_str2)

    # try:
    rest_carouserl_dict = {
        'carouselname': request.data.get('addCarouselName'),
        'carouseltype': request.data.get('carouselType'),
        'carouselimageurl': request.data.get('imageUrl'),
        'carouseltimerange': request.data.get('timeRange'),
        'status': 1,
        'publishedat': timezone.localtime(),
        'createdby_id': 1,
        'restaurantid': 1,
        'createdat': timezone.localtime(),
    }

    restaurantCarousel = RestaurantCarousel.objects.create(**rest_carouserl_dict)
    # except Exception as e:
    #     transaction.set_rollback(True)  # 回执
    #     print(str(e))
    #     return Result.error('xx新建失败！请查看：' + str(e))
    return Result.success('xx新建完成！')


@api_view(['GET'])
def get_rest(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')
    restaurantList = Restaurant.objects.filter(id=1)
    if len(restaurantList) == 0:
        return Result.error('无此店铺信息！')
    restaurantOne = restaurantList[0]
    dish_and_tags_dict = {
        'restId': restaurantOne.id,
        'restaurantName': restaurantOne.restaurantname,
        'restaurantType': restaurantOne.restauranttype,
        'openingHours': restaurantOne.openinghours,
        'restaurantPhone': restaurantOne.restaurantphone,
        'restaurantAddress': restaurantOne.restaurantaddress,
        'navigationCoordinates': restaurantOne.navigationcoordinates,
        'createdBy': restaurantOne.createdby.managername,
        'createdAt': restaurantOne.createdat,
    }
    return Result.success(data=dish_and_tags_dict)


@api_view(['POST'])
@transaction.atomic
def update_rest(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    rest_id = request.data.get('restId')
    restaurantname = request.data.get('restName')
    restauranttype = request.data.get('restType')
    openinghours = request.data.get('restTime')
    restaurantphone = request.data.get('restPhone')
    restaurantaddress = request.data.get('restAdd')
    navigationcoordinates = request.data.get('restCol')

    try:
        rest_dict = {
            'id': 1,
            'restaurantname': restaurantname,
            'restauranttype': restauranttype,
            'openinghours': openinghours,
            'restaurantphone': restaurantphone,
            'restaurantaddress': restaurantaddress,
            'navigationcoordinates': navigationcoordinates,
            'lastupdatedby_id': 1,  # request.user.id,
            'updatedat': timezone.localtime()  # + timezone.timedelta(hours=8)
        }
        service_update_rest(rest_dict)

    except Exception as e:
        transaction.set_rollback(True)
        return Result.error('餐厅信息更改失败！请查看：' + str(e))
    return Result.success('餐厅信息更改完成！')


# @api_view(['POST'])
# @transaction.atomic
# def add_carousel(request):
#     if request.method != 'POST':
#         return Result.error('无效的请求方法')
#
#     required_void_fields = ['carouselName', 'carouselImageUrl', 'carouselTimeRange',
#                             'status', 'carouselType']
#     required_null_fields = required_void_fields
#     Res_boo1, Res_str1 = judgment_void(required_void_fields, request)
#     if not Res_boo1:
#         return Result.error(Res_str1)
#     Res_boo2, Res_str2 = judgment_null(required_null_fields, request)
#     if not Res_boo2:
#         return Result.error(Res_str2)
#
#     try:
#         carousel_dict = {
#             'carouselName': request.data.get('carouselName'),
#             'carouselImageUrl': request.data.get('carouselImageUrl'),
#             'carouselTimeRange': request.data.get('carouselTimeRange'),
#             'status': request.data.get('status'),
#             'carouselType': request.data.get('carouselType'),
#             'createdBy_id': 1,  # request.user.id,  # id
#             'createdAt': timezone.localtime()  # + timezone.timedelta(hours=8)
#         }
#         carousel = service_add_carousel(carousel_dict)
#     except Exception as e:
#         transaction.set_rollback(True)  # 回执
#         return Result.error('xx新建失败！请查看：' + str(e))
#     return Result.success('xx新建完成！')
#

@api_view(['POST'])
@transaction.atomic
def update_carousel_status(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    try:
        carousel_id = request.data.get('carouselId')
        status = request.data.get('status')
        carousel_dict = {
            'id': carousel_id,
            'status': status,
        }
        if status:
            carousel_dict['publishedAt'] = timezone.localtime()
        else:
            carousel_dict['publishedAt'] = None

        service_update_carousel(carousel_dict)
    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xx更新失败！请查看：' + str(e))
    return Result.success('xx更新完成！')


@api_view(['POST'])
@transaction.atomic
def del_carousel(request):
    if request.method != 'POST':
        return Result.error('无效的请求方法')
    try:
        carousel_id = request.data.get('carouselId')
        if carousel_id in ['', None]:
            return Result.error('请检查，问题项目carouselId无值！')

        RestaurantCarousel.objects.filter(id=carousel_id).delete()
    except Exception as e:
        transaction.set_rollback(True)  # 回执
        return Result.error('xx删除失败！请查看：' + str(e))
    return Result.success('xx删除完成！')


@api_view(['GET'])
@transaction.atomic
def get_carousel_list(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')
    all_results = []
    carouselType = request.GET.get('carouselType')
    carouselList = RestaurantCarousel.objects.filter(carouselType=carouselType)
    for carouselOneContent in carouselList:
        all_results.append({
            'carouselId': carouselOneContent.id,
            'carouselName': carouselOneContent.carouselName,
            'carouselImageUrl': carouselOneContent.carouselImageUrl,
            'carouselTimeRange': carouselOneContent.carouselTimeRange,
            'createdByName': carouselOneContent.createdBy.managerName,
            'status': carouselOneContent.status,
            'carouselType': carouselOneContent.carouselType,
        })

    paginator = Paginator(all_results, int(request.GET.get('pageSize', 10)))
    paginated_results = paginator.get_page(int(request.GET.get('page', 1)))
    page_results = [result for result in paginated_results]
    #
    return Result_page.success(data=page_results, total=len(all_results))


@api_view(['GET'])
@transaction.atomic
def get_carousel(request):
    if request.method != 'GET':
        return Result.error('无效的请求方法')

    carouselId = request.GET.get('carouselId')
    carouselList = RestaurantCarousel.objects.filter(id=carouselId)
    if len(carouselList) == 0:
        return Result.error('查无此轮播信息！')
    carouselOne = carouselList[0]
    all_results = {
        'carouselId': carouselOne.id,
        'carouselName': carouselOne.carouselName,
        'carouselImageUrl': carouselOne.carouselImageUrl,
        'carouselTimeRange': carouselOne.carouselTimeRange,
        'createdByName': carouselOne.createdBy.managerName,
        'publishedAt': carouselOne.publishedAt,
        'status': carouselOne.status,
        'carouselType': carouselOne.carouselType,
    }

    return Result_page.success(data=all_results)
