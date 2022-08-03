from django.shortcuts import render, HttpResponse
from . import weibo_spider as spider
from .models import weibo


# Create your views here.

def wei(request):
    return render(request, 'account/task.html')

def word_anlaies(request):
    pass
def weiaj(request):
    spider.run()
    return HttpResponse("200")


def msg(request):
    # print(request.GET.get('m'))
    code = request.GET.get('m')
    with open('code.txt', 'w') as f:
        f.write(code)
    return render(request,'account/msg.html')


def msg_get(request):
    with open('code.txt', 'r') as f:
        msg = f.read()
    # 每次获取成功都置空
    with open('code.txt', 'w') as f:
        f.write('')
    return HttpResponse(msg)
