from django.shortcuts import render, HttpResponse
from . import wei


# Create your views here.

def weibo(request):
    wei.run()
    return HttpResponse("执行成功")


def msg(request):
    # print(request.GET.get('m'))
    code=request.GET.get('m')
    with open('code.txt','w') as f:
        f.write(code)
    return HttpResponse("收到")

def msg_get(request):
    with open('code.txt', 'r') as f:
        msg = f.read()
    return HttpResponse(msg)
