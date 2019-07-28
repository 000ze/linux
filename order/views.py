from django.shortcuts import HttpResponse, render, redirect
from order import models
from functools import wraps


# Create your views here.

def user(request):
    return redirect("/merchant_list2/")


def check_login(func):
    @wraps(func)  # 装饰器修复技术,
    def inner(request, *args, **kwargs):
        res = request.get_signed_cookie("1234", default="0", salt='nb')
        if res == "zx":
            return func(request, *args, **kwargs)
        else:
            return redirect("/log_in/")

    return inner


# 展示商家列表
def merchant_list(request):
    res = request.get_signed_cookie("1234", default="0", salt='nb')
    print(res, type(res))
    if res == "zx":
        # 去数据库查出所有的商家,填充到HTML中,给用户返回
        ret = models.Merchant.objects.all().order_by("id")
        return render(request, "merchant_list.html", {"merchant_list": ret})
    else:
        return redirect("/log_in/")


# 添加新的商家

def add_merchant(request):
    res = request.get_signed_cookie("1234", default="0", salt='nb')
    if res == "zx":
        error_msg = ""
        # 如果是POST请求,我就取到用户填写的数据
        if request.method == "POST":
            new_name = request.POST.get("merchant_name", None)
            if new_name:
                # 通过ORM去数据库里新建一条记录
                models.Merchant.objects.create(name=new_name)
                # 引导用户访问出版社列表页,查看是否添加成功  --> 跳转
                return redirect("/merchant_list/")
            else:
                error_msg = "商家名字不能为空!"
                # 用户第一次来,我给他返回一个用来填写的HTML页面
                return render(request, "add_merchant.html", {"error": error_msg})
        else:
            return render(request, "add_merchant.html", {"error": error_msg})

    # else:
    #     return HttpResponse("")


# 删除商家的函数
def delete_merchant(request):
    # 删除指定的数据
    # 1. 从GET请求的参数里面拿到将要删除的数据的ID值
    delete_id = request.GET.get("id", None)  # 字典取值,娶不到默认为None
    # 如果能取到id值
    if delete_id:
        # 去数据库删除当前id值的数据
        # 根据id值查找到数据
        del_obj = models.Merchant.objects.get(id=delete_id)
        # 删除
        del_obj.delete()
        # 返回删除后的页面,跳转到商家的列表页,查看删除是否成功
        return redirect("/merchant_list/")
    else:
        return HttpResponse("要删除的数据不存在!")


# 编辑商家
def edit_merchant(request):
    # 用户修改完商家的名字,点击提交按钮,给我发来新的商家名字
    if request.method == "POST":
        print(request.POST)
        # 取新商家名字
        edit_id = request.POST.get("id")
        new_name = request.POST.get("merchant_name")
        # 更新商家
        # 根据id取到编辑的是哪个商家
        edit_merchant = models.Merchant.objects.get(id=edit_id)
        edit_merchant.name = new_name
        edit_merchant.save()  # 把修改提交到数据库
        # 跳转商家列表页,查看是否修改成功
        return redirect("/merchant_list/")
        # 从列表中传来的GET请求的URL中取到id参数
    edit_id = request.GET.get("id")
    if edit_id:
        # 获取到当前编辑的商家对象
        merchant_obj = models.Merchant.objects.get(id=edit_id)
        return render(request, "edit_merchant.html", {"merchant": merchant_obj})
    else:
        return HttpResponse("请登录")


# 展示产品的列表
@check_login
def product_list(request):
    # if request.method == "POST":
    # 去数据库中查询所有的产品
    all_product = models.Product.objects.all()
    # 在HTML页面完成字符串替换(渲染数据)
    return render(request, "product_list.html", {"all_product": all_product})


# else:
#     return redirect("/log_in/")


# 删除产品

def delete_product(request):
    # 从URL里面获取要删除的产品的id值
    delete_id = request.GET.get("id")  # 从URL里面取数据
    # 去删除数据库中删除指定id的数据
    if delete_id:
        models.Product.objects.get(id=delete_id).delete()
        # 返回产品产品页面, 查看是否删除成功
        return redirect("/product_list/")
    else:
        return HttpResponse("要删除的数据不存在!")


# 添加产品
def add_product(request):
    res = request.get_signed_cookie("1234", default="0", salt='nb')
    if res == "zx":
        if request.method == "POST":
            new_title = request.POST.get("product_title")
            if new_title:
                new_merchant_id = request.POST.get("merchant")
                # 创建产品对象,自动提交
                models.Product.objects.create(title=new_title, merchant_id=new_merchant_id)
                # 返回到产品列表页
                return redirect("/product_list/")
            else:
                # 取到所有的商家
                ret = models.Merchant.objects.all()
                return render(request, "add_product.html", {"merchant_list": ret})


# 编辑产品
def edit_product(request):
    if request.method == "POST":
        # 从提交的数据里面取,产品和该产品关联的商家
        edit_id = request.POST.get("id")
        new_title = request.POST.get("product_title")
        new_merchant_id = request.POST.get("merchant")
        # 更新
        edit_product_obj = models.Product.objects.get(id=edit_id)
        edit_product_obj.title = new_title  # 更新产品名
        edit_product_obj.merchant_id = new_merchant_id  # 更新产品关联的商家
        # 将修改提交到数据库
        edit_product_obj.save()
        # 返回产品列表页面,查看是否编辑成功
        return redirect("/product_list/")
    #
    # 返回一个页面,编辑产品信息
    # 取到编辑的产品的id值
    edit_id = request.GET.get("id")
    if edit_id:
        # 根据id去数据库中把具体的产品对象拿到
        edit_product_obj = models.Product.objects.get(id=edit_id)
        print(edit_product_obj.id)
        print(edit_product_obj.title)
        print(edit_product_obj.merchant)  # 取到当前产品对象关联的商家对象
        print(edit_product_obj.merchant_id)  # 取到当前产品对象关联的商家的id值
        ret = models.Merchant.objects.all()
        return render(
            request,
            "edit_product.html",
            {"merchant_list": ret, "product_obj": edit_product_obj}
        )

    else:
        return HttpResponse("请登录")


# 用户列表
@check_login
def user_list(request):
    # if request.method == "POST":
    # 查询所有的用户
    all_user = models.User.objects.all()
    ret = models.Product.objects.all()
    return render(request, "user_list.html", {"user_list": all_user, 'products': ret})


# else:
#     return render(request, "log_in.html")


# 添加用户

# 添加用户
def add_user(request):
    res = request.get_signed_cookie("1234", default="0", salt='nb')
    if res == "zx":
        if request.method == "POST":
            print("in post...")
            # 取到提交的数据
            new_user_name = request.POST.get("user_name")
            if new_user_name:
                # post提交的数据是多个值的时候一定会要用getlist,如多选的checkbox和多选的select
                ptoduct = request.POST.getlist("ptoduct")
                # 创建用户
                new_user_obj = models.User.objects.create(name=new_user_name)
                # 把新用户和产品建立对应关系,自动提交
                new_user_obj.product.set(ptoduct)
                # 跳转到用户列表页面,查看是否添加成功!
                return redirect("/user_list/")
                # 查询所有的产品

            else:
                ret = models.Product.objects.all()
                return render(request, "add_user.html", {"product_list": ret})


# 删除用户

def delete_user(request):
    # 从URL里面取到要删除的用户id
    delete_id = request.GET.get("id")
    if delete_id:
        # 根据ID值取到要删除的用户对象,直接删除
        # 1. 去用户表把用户删了
        # 2. 去用户和产品的关联表,把对应的关联记录删除了
        models.User.objects.get(id=delete_id).delete()
        # 返回用户列表页面
        return redirect("/user_list/")
    else:
        return HttpResponse("要删除的数据不存在!")


# 编辑用户
def edit_user(request):
    # 如果编辑完提交数据过来
    if request.method == "POST":
        # 拿到提交过来的编辑后的数据
        edit_user_id = request.POST.get("user_id")
        new_user_name = request.POST.get("user_name")
        # 拿到编辑后用户关联的产品信息
        new_product = request.POST.getlist("products")
        # 根据ID找到当前编辑的用户对象
        edit_user_obj = models.User.objects.get(id=edit_user_id)
        # 更新用户的名字
        edit_user_obj.name = new_user_name
        # 更新用户关联的产品的对应关系
        edit_user_obj.product.set(new_product)
        # 将修改提交到数据库
        edit_user_obj.save()
        # 返回用户列表页,查看是否编辑成功
        return redirect("/user_list/")

    # 从URL里面取要编辑的用户的id信息
    edit_id = request.GET.get("id")
    if edit_id:
        # 找到要编辑的用户对象
        edit_user_obj = models.User.objects.get(id=edit_id)
        # 查询所有的产品对象
        ret = models.Product.objects.all()
        return render(request, "edit_user.html", {"product_list": ret, "user": edit_user_obj})
    else:
        return HttpResponse("请登录！")


def log_in(request):
    if request.method == "GET":
        return render(request, "log_in.html")
    else:
        name = request.POST.get('name', None)
        pwd = request.POST.get('password', None)
        print("name:", name)
        print("pwd:", pwd)

        if name == "1234" and pwd == "1234":  # 判断是否是字符串

            res = redirect("/merchant_list/")
            # 设置加盐的cookie
            res.set_signed_cookie("1234", 'zx', salt="nb")
            return res
        else:
            error = "登陆失败"
            # upload(request.FILES["upload_file"])
            return render(request, "log_in.html", {"error": error})
            return HttpResponse('登陆成功')
        # return HttpResponse('登陆失败', )  # 怎样失败后跳转原登陆页面


def log_out(request):
    rep = redirect("/log_in/")
    rep.delete_cookie("1234")  # 删除用户浏览器上之前设置的usercookie值
    return rep



