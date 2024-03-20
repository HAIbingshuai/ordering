from django.urls import path
from .view_order.veiws_order import *
from .view_order.view_dict import *
from .view_order.views_dish import *
from .view_order.veiws_room import *
from .view_order.view_rest import *
from .view_order.view_admin import *
from .view_order.view_login import *
from .view_order.view_data import *
urlpatterns = [
    # 数据面板
    path('order/getData', get_data, name='get_data'),

    # path('order/dashboard/', dashboard, name='dashboard'),

    # 菜品管理
    path('order/addDish', add_dish, name='add_dish'),  # ---增
    path('order/updateDish', update_dish, name='update_dish'),  # ---改
    path('order/updateDishStatus', update_dish_status, name='update_dish_status'),  # ---改
    path('order/updateDishOrder', update_dish_dishOrder, name='update_dish_dishOrder'),  # ---改
    path('order/delDish', del_dish, name='del_dish'),  # ---删
    path('order/getDishList', get_dish_list, name='order_dish_list'),  # ---查list
    path('order/getDish', get_dish, name='get_dish'),  # ---查 one

    # 房间管理
    path('order/addRoom', add_room, name='add_room'),  # ---增
    path('order/updateRoom', update_room, name='update_room'),  # ---改
    path('order/updateRoomStatus', update_room_status, name='update_room_status'),  # ---改
    path('order/delRoom', del_room, name='del_room'),  # ---删
    path('order/getRoomList', get_room_list, name='get_room_list'),  # ---查
    path('order/getRoom', get_room, name='get_room'),  # ---查
    path('order/getUsageOfRoom', get_usage_of_room, name='get_usage_of_room'),  # ---查

    # 订单管理
    path('order/addOrder', add_order, name='add_order'),  # ---增
    path('order/updateOrderStatus', update_order_status, name='update_order_status'),  # ---改
    path('order/getOrderList', get_order_list, name='order_order_list'),  # ---查list
    path('order/getOrderAndroomList', get_orderAndroom_list, name='get_orderAndroom_list'),  # ---改
    path('order/getOrder', get_order, name='get_order'),  # ---查 one
    path('order/delOrder', del_order, name='del_order'),  # ---删

    # 餐厅
    path('order/getRest', get_rest, name='get_rest'),  # ---查餐厅one
    path('order/updateRest', update_rest, name='updat_rest'),  # ---改

    # 轮播
    path('order/addCarousel', add_carousel, name='add_carousel'),  # 查轮播图
    path('order/updateCarouselStatus', update_carousel_status, name='update_carousel_status'),  # 修改播图
    path('order/delCarousel', del_carousel, name='del_carousel'),  # 查轮播图LIST
    path('order/getCarouselList', get_carousel_list, name='get_carousel_list'),  # 查轮播图LIST
    path('order/getCarousel', get_carousel, name='get_carousel'),  # 查轮播图

    # 管理员-管理
    path('order/addAdmin', add_admin, name='add_admin'),
    path('order/delAdmin', del_admin, name='del_admin'),
    path('order/getAdminList', get_admin_list, name='get_admin_list'),
    path('order/getAdmin', get_admin, name='get_admin'),

    # 登录
    path('order/login', admin_login, name='admin_login'),

    # second_category 字典
    path('order/addDictData', add_dict_data, name='add_dict_data'),
    path('order/updateDictData', update_dict_data, name='update_dict_data'),
    path('order/delDictData', del_dict_data, name='del_dict_data'),
    path('order/getDictDataList', get_dict_data_list, name='get_dict_data_list'),


]
