# django channel 使用

from django.urls import path
# 认证中间件 集成了CookieMiddleware, SessionMiddleware, AuthMiddleware
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# 读取django.setting中设置的hosts 地址
from channels.security.websocket import AllowedHostsOriginValidator

# 引入自定义app模块
# from django3.messager.consumers import MessagesConsumer
# from django3.notifications.consumers import NotificationsConsumer

# self.scope['type']获取协议类型
# self.scope['url_route']['kwargs']['username']获取url中关键字参数
# channels routing是scope级别的，一个连接只能由一个consumer接收和处理
application = ProtocolTypeRouter({
    # 普通的HTTP请求不需要我们手动在这里添加，框架会自动加载
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                # 消息提示
                # path('ws/notifications/', NotificationsConsumer),
                # 私信信息
                # path('ws/<str:username>/', MessagesConsumer),
            ])
        )
    )
})