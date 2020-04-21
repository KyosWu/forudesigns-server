from django.conf.urls import url, include
from django.urls import re_path, path

from pearbook.upload import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# 第一种方法写路由
# 商品
# router.register(r'test', views.test, basename="test")
# 商品-分类

urlpatterns = [
    re_path(r'^$', views.upload, name='upload_image'),
    path('upload_file/', views.upload_file, name='upload_file'),
    # 测试页面
    path(r'test/', views.test)
]
