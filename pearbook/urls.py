"""pearbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
# 静态文件需要
from django.views.static import serve
from pearbook.settings import MEDIA_ROOT

from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'docs/', include_docs_urls(title="django")),
    # media路径配置
    url(r'^media/(?P<path>.*)', serve, {"document_root":MEDIA_ROOT}),

    # 上传系统
    path(r'api/rbac/', include('pearbook.rbac.urls')),
    # 上传系统
    path(r'api/upload/', include('pearbook.upload.urls')),
    # 商品系统
    path(r'api/goods/', include('pearbook.goods.urls')),
]
