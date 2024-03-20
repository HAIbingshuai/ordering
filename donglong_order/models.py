from django.db import models
import uuid
from django.utils import timezone





# 订餐状态字典表
class OrderStatus(models.Model):
    statusName = models.CharField(max_length=20, verbose_name="状态名称")

    def __str__(self):
        return self.statusName

    class Meta:
        db_table = "order_status"
        verbose_name = "订餐状态"
        verbose_name_plural = "订餐状态"


# 菜品一级分类字典表
class FirstCategory(models.Model):
    categoryName = models.CharField(max_length=20, verbose_name="一级分类名称")

    def __str__(self):
        return self.categoryName

    class Meta:
        db_table = "first_category"
        verbose_name = "菜品一级分类"
        verbose_name_plural = "菜品一级分类"


# 菜品二级分类字典表
class SecondCategory(models.Model):
    categoryName = models.CharField(max_length=20, verbose_name="二级分类名称")

    def __str__(self):
        return self.categoryName

    class Meta:
        db_table = "second_category"
        verbose_name = "菜品二级分类"
        verbose_name_plural = "菜品二级分类"


class User(models.Model):
    userName = models.CharField(max_length=50, verbose_name="用户名")
    phoneNumber = models.CharField(max_length=15, verbose_name="手机号")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.userName

    class Meta:
        db_table = "user"
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Manager(models.Model):
    managerName = models.CharField(max_length=50, verbose_name="管理人员姓名")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    createdBy = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name="创建此管理人员的管理人ID", db_column='createdBy')
    userName = models.CharField(unique=True, max_length=100, blank=True, null=True)
    userPassword = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, verbose_name="手机号")

    def __str__(self):
        return self.managerName

    class Meta:
        db_table = "manager"
        verbose_name = "管理人员"
        verbose_name_plural = "管理人员"


class Room(models.Model):
    roomName = models.CharField(max_length=100, verbose_name="包间名称")
    roomConfiguration = models.CharField(max_length=100, null=True, verbose_name="包间配置")
    roomLocation = models.CharField(max_length=100, null=True, verbose_name="包间位置")
    status = models.BooleanField(default=True, verbose_name="状态")
    createdBy = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name="创建人", db_column='createdBy',
                                  related_name="room_createdby")
    createdAt = models.DateTimeField(verbose_name="创建时间")
    updatedAt = models.DateTimeField(null=True, verbose_name="修改时间")
    lastUpdatedBy = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, db_column='lastUpdatedBy',
                                      verbose_name="最后修改人员", related_name="room_lastUpdatedBy")

    class Meta:
        db_table = "room"
        verbose_name = "包间"
        verbose_name_plural = "包间"


class Dish(models.Model):
    dishOrder = models.IntegerField(verbose_name="菜品顺序号")
    dishName = models.CharField(max_length=100, verbose_name="菜品名称")
    firstCategoryId = models.ForeignKey(FirstCategory, on_delete=models.CASCADE, verbose_name="菜品一级分类ID",
                                        db_column='firstCategoryId')
    secondCategoryId = models.ForeignKey(SecondCategory, on_delete=models.CASCADE, verbose_name="菜品二级分类ID",
                                         db_column='secondCategoryId')
    imageUrl = models.URLField(verbose_name="菜品图片URL")
    # tagId = models.IntegerField(verbose_name="菜品标签表ID")
    stockQuantity = models.IntegerField(verbose_name="库存数量")
    dishStatus = models.BooleanField(default=True, verbose_name="菜品状态")
    dineInDisplayStatus = models.BooleanField(default=True, verbose_name="堂食显示状态")
    takeoutDisplayStatus = models.BooleanField(default=True, verbose_name="外卖显示状态")
    createdBy = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name="创建人", db_column='createdBy',
                                  related_name="dish_createdby")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updatedAt = models.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")
    lastUpdatedBy = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, db_column='lastUpdatedBy',
                                      verbose_name="最后修改人员", related_name="dish_lastUpdatedBy")

    class Meta:
        db_table = "dish"
        verbose_name = "菜品"
        verbose_name_plural = "菜品"


class Order(models.Model):
    orderNumber = models.CharField(max_length=50, verbose_name="订单编号")
    userId = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户ID", db_column='userId')
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, verbose_name="包间ID", db_column='roomId')
    orderStatus = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, verbose_name="订餐状态", db_column='orderStatus')
    scheduledDate = models.DateField(verbose_name="订单约定日期")
    scheduledTimeStart = models.DateTimeField(verbose_name="订单约定时间开始")
    scheduledTimeEnd = models.DateTimeField(verbose_name="订单约定时间结束")
    createdAt = models.DateTimeField(verbose_name="创建时间")
    bz = models.CharField(max_length=50, null=True, verbose_name="备注")
    numberDiners = models.IntegerField(null=True, verbose_name="就餐人数")
    lastUpdatedBy = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, db_column='lastUpdatedBy',
                                      verbose_name="最后修改人员", related_name="order_lastUpdatedBy")
    updatedAt = models.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        db_table = "order"
        verbose_name = "订单"
        verbose_name_plural = "订单"


class OrderDish(models.Model):
    orderId = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="订单ID", db_column='orderId')
    dishId = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name="菜品ID", db_column='dishId')
    dishNum = models.IntegerField(verbose_name="下单菜品数量")

    class Meta:
        db_table = "order_dish"
        verbose_name = "订单-菜品"
        verbose_name_plural = "订单-菜品"


class UserDish(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户ID", db_column='userId')
    dishId = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name="菜品ID", db_column='dishId')

    class Meta:
        db_table = "user_dish"
        verbose_name = "用户-菜品"
        verbose_name_plural = "用户-菜品"


class DishTag(models.Model):
    dishId = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name="菜品ID", db_column='dishId')
    tag1 = models.CharField(max_length=50, verbose_name="标签")

    class Meta:
        db_table = "dish_tag"
        verbose_name = "菜品-标签"
        verbose_name_plural = "菜品-标签"


class Restaurant(models.Model):
    restaurantName = models.CharField(max_length=100, verbose_name='餐厅名称')
    restaurantType = models.CharField(max_length=50, verbose_name='餐厅类型')
    openingHours = models.TextField(verbose_name='营业时间')
    restaurantPhone = models.CharField(max_length=20, verbose_name='餐厅电话')
    restaurantAddress = models.CharField(max_length=200, verbose_name='餐厅地址')
    navigationCoordinates = models.CharField(max_length=50, verbose_name='导航坐标')
    createdBy = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name="创建人", db_column='createdBy',
                                  related_name="rest_createdby")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    lastUpdatedBy = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, db_column='lastUpdatedBy',
                                      verbose_name="最后修改人员", related_name="rest_lastUpdatedBy")

    def __str__(self):
        return self.restaurantName

    class Meta:
        db_table = "restaurant"
        verbose_name = "餐厅表"
        verbose_name_plural = "餐厅表"


class RestaurantCarousel(models.Model):
    carouselName = models.CharField(max_length=100, verbose_name='轮播名称')
    carouselImageUrl = models.CharField(max_length=100, verbose_name='轮播图URL')
    carouselTimeRange = models.CharField(max_length=100, verbose_name='轮播时间范围')
    publishedAt = models.DateTimeField(null=True, verbose_name='发布时间')
    status = models.BooleanField(default=True, verbose_name="状态")
    carouselType = models.IntegerField(verbose_name="轮播类型")
    createdBy = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name="创建人", db_column='createdBy',
                                  related_name="carousel_createdby")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updatedAt = models.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")
    lastUpdatedBy = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, db_column='lastUpdatedBy',
                                      verbose_name="最后修改人员", related_name="carousel_lastUpdatedBy")

    def __str__(self):
        return self.carouselName

    class Meta:
        db_table = "restaurant_carousel"
        verbose_name = "轮播表"
        verbose_name_plural = "轮播表"


class AuthtokenTokenAdmin(models.Model):
    key = models.CharField(primary_key=True, max_length=40, default=uuid.uuid4)
    created = models.DateTimeField(default=timezone.now)
    manager = models.OneToOneField(Manager, models.DO_NOTHING, unique=True, db_column='manager')
    expires = models.DateTimeField()

    class Meta:
        db_table = 'authtoken_token_admin'
        verbose_name = "权限管理表"
        verbose_name_plural = "权限管理表"
