"""first_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    url(r'^blog/index/', views.index),
    url(r'blog/(\w+)/article/(\d+)/$', views.article_detail),  # 文章详情  article_detail(request, xiaohei, 1)
    url(r'^blog/(\w+)', views.home),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^reg/', views.register),
    # 极验滑动验证码 获取验证码的url
    url(r'^pc-geetest/register', views.get_geetest),
    url(r'^is_exist/', views.is_exist),


    # media相关的路由设置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),

]
