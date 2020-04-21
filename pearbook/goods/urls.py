from django.conf.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

# views视图
from pearbook.goods.views.goods import GoodsBanner, Category, CategoryPrimary, Featured, HotProduct

# 注册路由
router = DefaultRouter()
# 商品轮播图
router.register(r'banner', GoodsBanner, basename="GoodsBanner")
# 所有分类商品
router.register(r'category', Category, basename="Category")
# 商品分类 第一级别
router.register(r'categoryPrimary', Category, basename="CategoryPrimary")
# 创客作品展示
router.register(r'featured', Featured, basename="Featured")
# 热销产品前16
router.register(r'hotproduct', HotProduct, basename="HotProduct")

urlpatterns = [
    path(r'', include(router.urls)),
]