from ..models import Room


def service_add_room(dish_dict):
    room = Room.objects.create(**dish_dict)  # Room
    return room


def service_update_room(dish_dict):
    Room.objects.filter(id=dish_dict['id']).update(**dish_dict)


def service_delete_room(room_id):
    Room.objects.filter(id=room_id).delete()
