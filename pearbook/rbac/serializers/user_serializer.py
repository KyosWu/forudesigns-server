from rest_framework import serializers
from ..models import UserProfile
import re


class UserListSerializer(serializers.ModelSerializer):
    '''
    用户列表的序列化
    '''
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return obj.roles.values()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'image', 'department', 'position', 'superior',
                  'is_active','roles', 'avatar']
        depth = 1


class UserModifySerializer(serializers.ModelSerializer):
    '''
    用户编辑的序列化
    '''
    mobile = serializers.CharField(max_length=11)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'mobile', 'email', 'image', 'department', 'position', 'superior',
                  'is_active', 'roles']

    # 校验手机号码
    def validate_mobile(self, mobile):
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")
        return mobile


# 创建用户序列化
class UserCreateSerializer(serializers.ModelSerializer):
    '''
    创建用户序列化
    '''
    username = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)
    # mobile = serializers.CharField(max_length=11)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'roles',]


    # 验证用户名
    # def validate_username(self, username):
    #     if UserProfile.objects.filter(username=username):
    #         raise serializers.ValidationError(username + ' 账号已存在')
    #     return username

    # 验证邮箱
    def validate_email(self, email):
        if UserProfile.objects.filter(email=email):
            raise serializers.ValidationError(email + ' 邮箱已存在')
        return email

    # 验证手机号码
    # def validate_mobile(self, mobile):
    #     REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
    #     if not re.match(REGEX_MOBILE, mobile):
    #         raise serializers.ValidationError("手机号码不合法")
    #     if UserProfile.objects.filter(mobile=mobile):
    #         raise serializers.ValidationError("手机号已经被注册")
    #     return mobile


class UserInfoListSerializer(serializers.ModelSerializer):
    '''
    公共users
    '''
    class Meta:
        model = UserProfile
        fields = ('username', 'mobile', 'email')