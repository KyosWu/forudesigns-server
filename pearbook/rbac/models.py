# -*- coding: utf-8 -*-

import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

# from pearbook.goods.models import Goods


# 菜单
class Menu(models.Model):
    """
    菜单
    """
    name = models.CharField(max_length=30, unique=True, verbose_name="菜单名")
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="图标")
    path = models.CharField(max_length=158, null=True, blank=True, verbose_name="链接地址")
    is_frame = models.BooleanField(default=False, verbose_name="外部菜单")
    is_show = models.BooleanField(default=True, verbose_name="显示标记")
    sort = models.IntegerField(null=True, blank=True, verbose_name="排序标记")
    component = models.CharField(max_length=200, null=True, blank=True, verbose_name="组件")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父菜单")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 权限
class Permission(models.Model):
    """
    权限
    """
    name = models.CharField(max_length=30, unique=True, verbose_name="权限名")
    method = models.CharField(max_length=50, null=True, blank=True, verbose_name="方法")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父权限")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 角色
class Role(models.Model):
    """
    角色
    """
    name = models.CharField(max_length=32, unique=True, verbose_name="角色")
    permissions = models.ManyToManyField("Permission", blank=True, verbose_name="权限")
    menus = models.ManyToManyField("Menu", blank=True, verbose_name="菜单")
    desc = models.CharField(max_length=50, blank=True, null=True, verbose_name="描述")


# 组织架构
class Organization(models.Model):
    """
    组织架构
    """
    organization_type_choices = (
        ("company", "公司"),
        ("department", "部门"),
        ("artist", "创客"),
        ("other", "普通用户"),
    )
    name = models.CharField(max_length=60, verbose_name="名称")
    type = models.CharField(max_length=20, choices=organization_type_choices, default="company", verbose_name="类型")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父类组织")

    class Meta:
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 重写用户模型
class UserProfile(AbstractUser):
    '''
    用户
    '''
    uuid = models.UUIDField(default=uuid.uuid4, null=False, editable=False, verbose_name='用户id')
    username = models.CharField(unique=True, max_length=20, null=False, blank=False, verbose_name="姓名")
    # mobile = models.CharField(max_length=11, verbose_name="手机号码")
    email = models.EmailField(unique=True, max_length=50, verbose_name="邮箱")
    image = models.ImageField(upload_to="avatar/%Y/%m", default="image/default.png",
                              max_length=100, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatar/%Y/%m", default="avatar/default/default.png",
                              max_length=100, null=True, blank=True)
    department = models.ForeignKey("Organization", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="部门")
    position = models.CharField(max_length=50, null=True, blank=True, verbose_name="职位")
    superior = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="上级主管")
    #
    roles = models.ManyToManyField("Role", verbose_name="角色", blank=True)
    # goods = models.ManyToManyField(Goods, verbose_name="商品", blank=True)
    #
    # gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="male", verbose_name="性别")
    # birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    # introduction = models.TextField(blank=True, null=True, verbose_name='简介')
    #
    # picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name='头像')
    # location = models.CharField(max_length=50, null=True, blank=True, verbose_name='城市')
    # personal_url = models.URLField(max_length=255, null=True, blank=True, verbose_name='个人链接')
    #
    # weibo = models.URLField(max_length=255, null=True, blank=True, verbose_name='微博链接')
    # zhihu = models.URLField(max_length=255, null=True, blank=True,verbose_name='知乎链接')
    # github = models.URLField(max_length=255, null=True, blank=True, verbose_name='Github链接')
    # linkedin = models.URLField(max_length=255, null=True, blank=True, verbose_name='LinkedIn链接')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username

