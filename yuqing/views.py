from django.shortcuts import render, HttpResponse
from . import weibo_spider as spiderer
from .models import weibo
import jieba.analyse
from wordcloud import WordCloud

# Create your views here.

def wei(request):
    if request.method=="POST":
        str =request.POST['ck'].strip(' ')
        if str == "" or str == "请输入从浏览器抓的CK：":
            pass
        else:
            # print(str)
            with open('cookie.txt','w') as f:
                f.write(request.POST['ck'])
    return render(request, 'account/task.html')


def word_anlaies(request):
    quset = weibo.objects.all()
    result =""
    for qu in quset:
        # keywords = jieba.analyse.textrank(qu.article)
        keyword = jieba.analyse.extract_tags(qu.article)
        result += "".join(keyword)
    cut = jieba.cut(result)
    ll =['佛山科学技术学院', '科学技术', '学院','佛山','佛山科学技术']
    result = " ".join(x for x in cut if x not in ll)
    wc = WordCloud(
        font_path='steo.ttf',
        # 设置字体，不指定就会出现乱码
        # 设置背景色
        background_color='white',
        # 设置背景宽
        width=300,
        # 设置背景高
        height=250,
        # 最大字体
        max_font_size=50,
        # 最小字体
        min_font_size=10,
        mode='RGBA'
        # colormap='pink'
    )
    print(result)
    wc.generate(result)
    wc.to_file(r"wordcloud.png")
    # print()
    return HttpResponse('200')


def weiaj(request):
    spiderer.run()
    return HttpResponse("200")


def msg(request):
    # print(request.GET.get('m'))
    code = request.GET.get('m')
    with open('code.txt', 'w') as f:
        f.write(code)
    return render(request, 'account/msg.html')


def msg_get(request):
    with open('code.txt', 'r') as f:
        msg = f.read()
    # 每次获取成功都置空
    with open('code.txt', 'w') as f:
        f.write('')
    return HttpResponse(msg)
