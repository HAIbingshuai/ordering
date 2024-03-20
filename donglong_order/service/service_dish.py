from ..models import Dish, DishTag, FirstCategory, SecondCategory, Manager
from django.db.models import F


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
