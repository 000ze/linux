from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib import auth
from geetest import GeetestLib
from blog import forms, models
from django.db.models import Count


# Create your views here.

# 使用极验滑动验证码的登录

def login(request):
    # if request.is_ajax():  # 如果是AJAX请求
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            user = auth.authenticate(username=username, password=pwd)
            if user:
                # 用户名密码正确
                # 给用户做登录
                auth.login(request, user)
                ret["msg"] = "/blog/index/"
            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"

        return JsonResponse(ret)
    return render(request, "login.html")


pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# 处理极验 获取验证码的视图
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def is_exist(request):
    ret = {"status": 0, "msg": ""}
    username = request.GET.get("username")
    is_exist = models.UserInfo.objects.filter(username=username)
    if is_exist:
        ret["status"] = 1
        ret["msg"] = "用户名已存在！"
    return JsonResponse(ret)


# 注册的视图函数
def register(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)

        # 帮我做校验
        if form_obj.is_valid():
            # username=form_obj.cleaned_data.get("username")
            # is_exist=models.UserInfo.objects.filter(username=username)
            # if is_exist:
            #     ret["status"]=1
            #     ret["msg"]="用户名已存在！"
            #     return JsonResponse(ret)
            # 校验通过，去数据库创建一个新的用户
            form_obj.cleaned_data.pop("re_password")
            avatar_img = request.FILES.get("avatar")
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            ret["msg"] = "/login/"
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            #         print(ret)
            #         print("=" * 120)
            return JsonResponse(ret)
    # # 生成一个form对象
    form_obj = forms.RegForm()
    print(form_obj.fields)
    return render(request, "register.html", {"form_obj": form_obj})


def index(request):
    # 查询所有的文章列表
    article_list = models.Article.objects.all()
    return render(request, "index.html", {"article_list": article_list})


def logout(request):
    auth.logout(request)
    return redirect("/login/")


def blog(request):
    return render(request, "blog.html")

#
# # 个人博客主页
def home(request, username):
#     print(username)
#     return HttpResponse("你好")
#     # 去UserInfo表里把用户对象取出来
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
#     # 如果用户存在需要将TA写的所有文章找出来
    blog = user.blog
#
#     # 我的文章列表
    article_list = models.Article.objects.filter(user=user)
#     # 我的文章分类及每个分类下文章数
#     # 将我的文章按照我的分类分组，并统计出每个分类下面的文章数
#     # category_list = models.Category.objects.filter(blog=blog)
#     category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
# #     # [{'title': '技术', 'c': 2}, {'title': '生活', 'c': 1}, {'title': 'LOL', 'c': 1}]
# #     # 统计当前站点下有哪一些标签，并且按标签统计出文章数
#     tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
# #
#     # 按日期归档
#     archive_list = models.Article.objects.filter(user=user).extra(
#         select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}
#     ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")

    return render(request, "home.html", {
        "username": username,
        "blog": blog,
        "article_list": article_list,
    })
#
# #
# def get_left_menu(username):
#     user = models.UserInfo.objects.filter(username=username).first()
#     blog = user.blog
# #     category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
#     tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
#     # 按日期归档
#     archive_list = models.Article.objects.filter(user=user).extra(
#         select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}
#     ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")
#
#     return category_list, tag_list, archive_list
#
#
def article_detail(request, username, pk):
#     """
#     :param username: 被访问的blog的用户名
#     :param pk: 访问的文章的主键id值
#     :return:
#     """
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    blog = user.blog
#     # 找到当前的文章
    article_obj = models.Article.objects.filter(pk=pk).first()

    article_list = models.Article.objects.all()
    return render(
        request,
        "article_detail.html",
        {
            "username": username,
            "article": article_obj,
            "blog": blog,
            "article_list": article_list,
         }
    )