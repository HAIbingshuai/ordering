from ..models import Order, OrderDish, OrderStatus


def service_add_Order(order_dict):
    order = Order.objects.create(**order_dict)
    return order


def service_add_Order_Dish(order_id, order_dish_dict):  # [{'dishId':xx, 'dishNum': xx},{},{}]
    for order_dish in order_dish_dict:
        OrderDish.objects.create(**{
            'orderId_id': order_id,
            'dishId_id': order_dish['dishId'],
            'dishNum': order_dish['dishNum']
        })


def service_update_order(order_dict):
    Order.objects.filter(id=order_dict['id']).update(**order_dict)


def service_delete_order(order_id):
    Order.objects.filter(id=order_id).delete()


def service_delete_order_dish(order_id):
    OrderDish.objects.filter(orderId=order_id).delete()


def service_orderStatusDict():
    orderstatus_list = OrderStatus.objects.filter()
    orderstatus_dict = {}
    for one in orderstatus_list:
        orderstatus_dict[one.id] = one.statusname
    return orderstatus_dict
