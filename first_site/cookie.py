def check_login(func):
    @wraps(func)  # 装饰器修复技术,
    def inner(request, *args, **kwargs):
        res = request.get_signed_cookie("1234", default="0", salt='nb')
        if res == "zx":
            return func(request, *args, **kwargs)
        else:
            return redirect("/log_in/")

    return inner


name = request.POST.get('name', None)
pwd = request.POST.get('password', None)
print("name:", name)
print("pwd:", pwd)
if name == "天才" and pwd == "1234":  # 判断是否是字符串
    # return HttpResponse('登陆成功')
    res = redirect("/merchant_list/")
    # 设置加盐的cookie
    res.set_signed_cookie("1234", 'zx', salt="nb")
    return res
else:
    return render(request, "log_in.html", {"error": error})
