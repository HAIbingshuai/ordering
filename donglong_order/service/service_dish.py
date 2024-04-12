from ..models import Dish, DishTag, WeeklyDish
from django.db.models import F
from django.utils import timezone

def service_add_dish(dish_dict):
    Dish.objects.filter(dishOrder__gte=dish_dict['dishOrder']).update(dishOrder=F('dishOrder') + 1)  # 新建dish影响其他的内容
    dish = Dish.objects.create(**dish_dict)
    return dish


def service_update_dish(dish_dict):
    Dish.objects.filter(id=dish_dict['id']).update(**dish_dict)
    return True


def service_update_dish_dishOrder(dish_dict):
    Dish.objects.filter(dishOrder__gte=dish_dict['dishOrder']).update(dishOrder=F('dishOrder') + 1)  # 新建dish影响其他的内容
    Dish.objects.filter(id=dish_dict['id']).update(**dish_dict)
    return True


def service_add_dishTag(dish_id, add_tag_list):
    exists_dish_tags_objs = DishTag.objects.filter(dishId=dish_id)
    exists_dish_tags_list = [dish_tag.tag1 for dish_tag in exists_dish_tags_objs]

    # 新增标签(新增的不在已有的，新增)
    for add_tag in add_tag_list:
        if add_tag not in exists_dish_tags_list:
            dishTag = DishTag.objects.create(dishId_id=dish_id, tag1=add_tag)

    # 删除标签（已有的不在新增里的，删除）
    for existing_tag in exists_dish_tags_list:
        if existing_tag not in add_tag_list:
            DishTag.objects.filter(dishId=dish_id, tag1=existing_tag).delete()


def service_delete_dish(dish_id):
    Dish.objects.filter(id=dish_id).delete()


def service_delete_dishTag(dish_id):
    DishTag.objects.filter(dishId=dish_id).delete()


def service_restart_order_dish():
    # 遍历所有菜品
    exists_dish_objs = Dish.objects.filter()
    # 按照 dishOrder 由小到大 排序
    sorted_dish_tags_objs = exists_dish_objs.order_by('dishOrder')
    # 遍历排序的数据，更新每个数据的dishOrder
    for index, dish_tag_obj in enumerate(sorted_dish_tags_objs, start=1):
        dish_tag_obj.dishOrder = index
        dish_tag_obj.save(update_fields=['dishOrder'])


def service_top_dish(dish_id):
    # 尝试获取指定ID的菜品对象，如果不存在则返回 None
    exists_dish_objs = Dish.objects.filter(id=dish_id).first()
    if exists_dish_objs is not None:
        # 获取原始的 dishOrder
        orgin_dishOrder = exists_dish_objs.dishorder
        # 更新其他菜品的 dishOrder，使其依次顺延
        Dish.objects.filter(dishorder__lt=orgin_dishOrder).update(dishorder=F('dishorder') + 1)
        # 将指定菜品的 dishOrder 设置为 1，即置顶
        exists_dish_objs.dishorder = 1
        exists_dish_objs.save(update_fields=['dishorder'])

def service_weekly_dish_add(dish_time,weekId,dish_list,managerId):
    for dishid in dish_list:
        data = {
            'weekid_id': weekId,
            'dayname': dish_time,
            'dishid_id': int(dishid),
            'createdat': timezone.localtime(),
            'createdby_id': managerId,
        }
        weeklyDish1 = WeeklyDish.objects.create(**data)