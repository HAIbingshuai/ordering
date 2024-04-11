from django.contrib import admin
from .models import Manager

admin.site.site_header = '东龙集团-点餐管理后台'  # 设置 header
admin.site.site_title = '东龙集团-点餐管理后台'  # 设置 title
admin.site.index_title = '东龙集团-点餐管理后台'
admin.site.register(Manager)
