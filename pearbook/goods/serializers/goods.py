# -*- coding: utf-8 -*-

from rest_framework import serializers

from pearbook.rbac.models import UserProfile
from pearbook.goods.models import Goods, GoodsBannerImage,\
    GoodsCategory, GoodsFrontImage, GoodsDetailImage,GoodsTag


# 商品
class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = "__all__"


# 商品轮播图
class GoodsBannerImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsBannerImage
        fields = ("image", )


# 商品类目第三级别
class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


# 商品类目第二级别
class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


# 商品类目第一级别
class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


# 商品类目 仅且 第一级
class CategoryPrimarySerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategory
        fields = "__all__"


#  创客作品展示子级
class FeaturedArtistAndGoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', 'avatar')


#  商品前端图
class GoodsFrontImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsFrontImage
        fields = ('id', 'front_image')


#  商品详情图
class GoodsDetailImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsDetailImage
        fields = ('id', 'detail_image')


#  创客作品展示父级
class FeaturedArtistSerializer(serializers.ModelSerializer):
    artist = FeaturedArtistAndGoodsSerializer()
    frontImage = GoodsFrontImageSerializer()
    detailImage = GoodsDetailImageSerializer()
    goods = GoodsSerializer()

    class Meta:
        # model = Goods
        # fields = ('id', 'name', 'image', 'artist', 'image', )
        # fields  = "__all__"
        model = Goods
        fields = "__all__"


#  前端-index-热搜产品
class HotProductSerializer(serializers.ModelSerializer):
    frontImage = GoodsFrontImageSerializer()

    class Meta:
        model = Goods
        field = ('id', 'name', 'frontImage', )


# 商品标签
class GoodsTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsTag
        field = "__all__"