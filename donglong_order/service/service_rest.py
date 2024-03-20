from ..models import Restaurant,RestaurantCarousel


def service_update_rest(rest_dict):
    Restaurant.objects.filter(id=rest_dict['id']).update(rest_dict)
    return True

def service_add_carousel(carousel_dict):
    carousel = RestaurantCarousel.objects.create(**carousel_dict)
    return carousel


def service_update_carousel(carousel_dict):
    RestaurantCarousel.objects.filter(id=carousel_dict['id']).update(**carousel_dict)
