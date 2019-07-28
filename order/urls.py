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
from django.contrib import admin
from . import views

urlpatterns = [
    # 登陆与注销
    url(r'^log_in/', views.log_in),
    url(r'^log_out/', views.log_out),
    url(r'^admin/', admin.site.urls),
    # 商家相关的对应关系
    url(r'^merchant_list/', views.merchant_list),
    url(r'^add_merchant/', views.add_merchant),
    url(r'^delete_merchant/', views.delete_merchant),
    url(r'^edit_merchant/', views.edit_merchant),
    # 产品相关的对应关系
    url(r'^product_list/', views.product_list),
    url(r'^add_product/', views.add_product),
    url(r'^delete_product/', views.delete_product),
    url(r'^edit_product/', views.edit_product),
    # 用户相关的对应关系
    url(r'^user_list/', views.user_list),
    url(r'^add_user/', views.add_user),
    url(r'^delete_user/', views.delete_user),
    url(r'^edit_user/', views.edit_user),
    url(r'^user/', views.user),

]
