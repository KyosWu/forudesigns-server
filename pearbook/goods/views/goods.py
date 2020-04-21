# -*- coding: utf-8 -*-

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import filters

from django.http import JsonResponse,HttpResponse
from django.db.models import Q,F,Count,Prefetch

# 路由
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import viewsets
# 分页
from rest_framework.pagination import PageNumberPagination
# model
from pearbook.goods.models import GoodsBannerImage, GoodsCategory, Goods, GoodsTag
# serializer
from pearbook.goods.serializers.goods import GoodsSerializer,GoodsBannerImageSerializer, \
    CategorySerializer, CategoryPrimarySerializer, FeaturedArtistSerializer, \
    HotProductSerializer,GoodsTagSerializer

from pearbook.rbac.models import UserProfile


# 商品分页
class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


# 商品轮播图
class GoodsBanner(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品轮播列表数据
    retrieve:
        获取商品轮播图详情
    """
    queryset = GoodsBannerImage.objects.all()
    serializer_class = GoodsBannerImageSerializer


# 商品类目 所有
class Category(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


# 创客作品展示
class Featured(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        创客作品展示列表
    retrieve:
        获取创客作品展示详情
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    # def list(self, request):
    #     # 商品表取前4 新增前四字段
    #     # goods.objects.annotate(topF="id__lt=4")
    #     # i.goods.values('topF', 'name', 'artist__avatar', 'frontImage__front_image')
    #
    #     # 查找id 前8名 user
    #     user = UserProfile.objects.filter(id__lt=8).select_related('goods')
    #     # user对应的商品表
    #     arr = []
    #     # 需要分成三组
    #     # 遍历每个user 反向查询的goods信息 frontImage__front_image取前4 取前4 怎么做呢？
    #     for i in user:
    #         goods = i.goods.values('id', 'name', 'artist__avatar', 'frontImage__front_image')
    #         for j in goods:
    #             # 取前4种商品图片
    #             arr.append(j)
    #     return HttpResponse(arr)


# 商品分类 第一级类别
class CategoryPrimary(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类 第一级类别数据
    retrieve:
        获取商品分类 第一级类别详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategoryPrimarySerializer


# 热销商品
class HotProduct(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        热销商品列表
    retrieve:
        获取热销商品详情
    """
    queryset = Goods.objects.all()
    serializer_class = HotProductSerializer

    def list(self, request):
        # 实际根据销售数量前16
        good = Goods.objects.all()[:16]
        goods = good.values('id', 'name', 'frontImage__front_image')
        # arr.append(goods)
        return HttpResponse(goods)


# 商品标签
class GoodTags(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品标签列表数据
    retrieve:
        获取商品标签详情
    """
    queryset = GoodsTag.objects.all()
    serializer_class = GoodsTagSerializer


# 根据tag标签获取商品信息
class GoodTagsChoose(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        根据tag标签获取商品信息
    retrieve:
        获取tag标签商品信息
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    def retrieve(self, request, *args, **kwargs):
        # 获取tags 的标签值
        id = request.get(id)
        # 在goods表中查询关联的tags
        tagsId = GoodsTag.objects.filter(id=id)
        # 获取goods表中的数据
        GoodsTag.goods.values('id', 'name', 'tags__goods__price', 'tags__goods__frontImage')
        return HttpResponse('kk')