from datetime import datetime

from django.shortcuts import render, HttpResponse
from . import weibo_spider as spiderer
from .models import weibo
import jieba.analyse
from wordcloud import WordCloud

# Create your views here.
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
import warnings
import dateparser
# Ignore dateparser warnings regarding pytz
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)
# 实例化调度器
scheduler = BackgroundScheduler()
# 调度器使用默认的DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore())


# 注册定时任务并开始
def test1():
    # 具体要执行的代码
    print('[APScheduler][Task]-{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
    print("爬取任务开始")
    spiderer.run()


# try:
#     scheduler.add_job(test1, 'interval',minutes=30, timezone='Asia/Shanghai', id="微博", args=())
#     scheduler.start()
# except:
#     pass
# scheduler.remove_job("微博")

def wei(request):
    if request.method == "POST":
        str = request.POST['ck'].strip(' ')
        if str == "" or str == "请输入从浏览器抓的CK：":
            pass
        else:
            # print(str)
            with open('cookie.txt', 'w') as f:
                f.write(request.POST['ck'])
    return render(request, 'account/task.html')


def word_anlaies(request):
    quset = weibo.objects.all()
    result = ""
    for qu in quset:
        # keywords = jieba.analyse.textrank(qu.article)
        keyword = jieba.analyse.extract_tags(qu.article)
        result += "".join(keyword)
    cut = jieba.cut(result)
    ll = ['佛山科学技术学院', '科学技术', '学院', '佛山', '佛山科学技术']
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
