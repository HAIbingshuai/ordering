from django.contrib import admin
from .models import Manager,Order


class users_Manager(admin.ModelAdmin):
    list_display = ['id', 'managerName', 'createdAt', 'createdBy', 'userName', 'userPassword']

admin.site.register(Manager, users_Manager)

class order_Admin(admin.ModelAdmin):
    list_display = ['orderNumber', 'userId', 'roomId', 'orderStatus', 'scheduledDate', 'scheduledTimeStart',
                    'scheduledTimeEnd', 'createdAt', 'bz', 'numberDiners', 'lastUpdatedBy']
    search_fields = ['orderNumber', 'userId', 'roomId__roomName', 'bz']
admin.site.register(Order, order_Admin)

admin.site.site_header = '东龙集团-点餐管理后台'  # 设置 header
admin.site.site_title = '东龙集团-点餐管理后台'   # 设置 title
admin.site.index_title = '东龙集团-点餐管理后台'
