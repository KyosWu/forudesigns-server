# -*- coding: utf-8 -*-

import uuid
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from pearbook.rbac.models import UserProfile


# 商品类别
class GoodsCategory(models.Model):
    """
    商品类别
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    category_image = models.ImageField(upload_to="category", verbose_name="图片", null=True, blank=True)
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",related_name="sub_cat",on_delete=models.CASCADE)
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 品牌名
class GoodsCategoryBrand(models.Model):
    """
    品牌名
    """
    category = models.ForeignKey(GoodsCategory, related_name='brands', null=True, blank=True, verbose_name="商品类目",on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=30, verbose_name="品牌名", help_text="品牌名")
    desc = models.TextField(default="", max_length=200, verbose_name="品牌描述", help_text="品牌描述")
    image = models.ImageField(max_length=200, upload_to="brands/")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "品牌"
        verbose_name_plural = verbose_name
        db_table = "goods_goodsbrand"

    def __str__(self):
        return self.name


# 商品
class Goods(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory, verbose_name="商品类目", related_name="goods", on_delete=models.CASCADE)
    artist = models.ForeignKey(UserProfile, verbose_name="创客", related_name="goods", on_delete=models.CASCADE)

    goods_sn = models.CharField(max_length=50, default="", verbose_name="商品唯一货号")
    name = models.CharField(max_length=100, verbose_name="商品名")

    sold_num = models.IntegerField(default=0, verbose_name="商品销售量")
    goods_num = models.IntegerField(default=0, verbose_name="库存数")
    # supplier = models.ForeignKey(, verbose_name="供应商") // 供应商
    # distribution = models.ForeignKey(, verbose_name="经销商") //经销商

    goods_brief = models.TextField(max_length=500, verbose_name="商品简短描述")
    goods_desc = UEditorField(verbose_name=u"商品详细描述", imagePath="goods/images/", width=1000, height=300,
                              filePath="goods/files/", default='')

    ship_free = models.BooleanField(default=True, verbose_name="是否承担运费")
    is_new = models.BooleanField(default=False, verbose_name="是否新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热销")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 标签
class GoodsTag(models.Model):
    """
    商品标签
    """
    name = models.CharField(max_length=100)
    goods = models.ManyToManyField("Goods", related_name='tags')


# 商品价格
class GoodsPrice(models.Model):
    """
    商品价格
    """
    goods = models.OneToOneField("Goods", on_delete=models.CASCADE, related_name='price')
    market_price = models.FloatField(default=0, verbose_name="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格")
    purchase_price = models.FloatField(default=0, verbose_name="进货价格")
    discount_price = models.FloatField(default=0, verbose_name="折扣价格")


# 商品封面图图片
class GoodsFrontImage(models.Model):
    """
    商品图片
    """
    goods = models.OneToOneField("Goods", on_delete=models.CASCADE, related_name='frontImage')
    # 只能一张
    front_image = models.ImageField(upload_to="goods/front/", null=True, blank=True, verbose_name="封面图")


# 商品详情图图片
class GoodsDetailImage(models.Model):
    """
    商品图片
    """
    goods = models.OneToOneField("Goods", on_delete=models.CASCADE, related_name='detailImage')
    detail_image = models.ImageField(upload_to="goods/detail/", null=True, blank=True, verbose_name="详情图")


# 商品动态
class GoodsShare(models.Model):
    """
    商品动态信息
    """
    goods = models.OneToOneField("Goods", on_delete=models.CASCADE, related_name='share')
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    liked_num = models.IntegerField(default=0, verbose_name="喜欢数")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    share_num = models.IntegerField(default=0, verbose_name="分享数")


# 前端-index-商品轮播图
class GoodsBannerImage(models.Model):
    """
    商品轮播图
    """
    # goods = models.ForeignKey(Goods, verbose_name="商品", related_name="images",on_delete=models.CASCADE)
    # uuid = models.UUIDField(default=uuid.uuid4, null=False, editable=False, verbose_name='商品轮播id')
    image = models.ImageField(upload_to="banner", verbose_name="图片", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


# 热搜词
class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords