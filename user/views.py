from django.http import HttpResponse
from django.shortcuts import render
from user.models import User_Register
# Create your views here.


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        # 把信息存到数据库
        user = User_Register.objects.create(username=username, password= password)

        return HttpResponse('注册成功')