from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from user.models import User_Register
# Create your views here.
import hashlib


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password = encryption(request.POST.get('password'))

        print(username, password)
        # 把信息存到数据库
        user = User_Register.objects.create(username=username, password=password)


        # 如果客户注册了，重定向到登录页面
        return redirect('/login/')


def login(request):
    # 如果是get访问返回登录页面
    if request.method == 'GET':
        # 设置cookie之后  客户下次get访问页面  获取cookie里的数据
        username = request.COOKIES.get('username')
        #  context 向html页面添加内容  里面传入字典  就是  html里面标签属性name和对应的value
        return render(request, 'login.html', context={'username': username})
    # 如果是post访问，判断用户名和密码和数据库里面的是否一样，根据结果返回不同的页面
    else:
        # post访问,获取username和password
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')   # 是否记住账号
        # 和数据库里面的验证
        try:
            user = User_Register.objects.get(username=username, password=password)
            # print(user)   返回对象
        except User_Register.DoesNotExist:

            return JsonResponse({'message': "defeated"})
        else:
            # 如果账号密码正确，记住用户名
            if remember == 'true':
                # 创建响应对象
                response = JsonResponse({'message': "success"})
                # 响应对象里面设置cookie发送给客户端浏览器
                response.set_cookie('username', username, 14 * 24 * 3600)
                return response


def encryption(password):
    """对密码进行加密"""
    md5_pwd = hashlib.md5()
    md5_pwd.update(password.encode('utf-8'))
    new_pwd = md5_pwd.hexdigest()
    salt = 'Nixxxxxxxx'
    md5_pwd.update(salt.encode('utf-8'))
    new_salt = md5_pwd.hexdigest()

    return new_salt + new_pwd