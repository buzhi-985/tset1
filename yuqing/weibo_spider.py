import os, json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import requests
import pickle
from .models import *

url = 'https://m.weibo.cn/p/index?containerid=100808165ef5c505a4b4f59142bc0a0f0aafae&luicode=10000011&lfid=100103type%3D1%26q%3D%E4%BD%9B%E5%B1%B1%E7%A7%91%E5%AD%A6%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2'
# chrrome版本大于88
opt = Options()
opt.add_argument("--disable-blink-features=AutomationControlled")
opt.add_argument("--disable-gpu")


# opt.add_argument('--headless')


# 控制页面滑动
def scrob(driver):
    time.sleep(2)
    try:
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
        print("以滑动")
    except:
        print("滑动失败")


# 获取全文内容
def get_all_text(driver, elem):
    try:
        # 判断是否有“全文内容”，若有则将内容存储在weibo_content中
        href = elem.find_element_by_link_text('全文').get_attribute('href')
        driver.execute_script('window.open("{}")'.format(href))
        driver.switch_to.window(driver.window_handles[1])
        weibo_content = driver.find_element_by_class_name('weibo-text').text
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        weibo_content = elem.find_elements_by_css_selector('div.weibo-text')[0].text
    return weibo_content


def iselement(elem, css_sel, istest=False):
    """
    实现判断元素是否存在
    :param elem: 浏览器对象
    :param css_sel: css_selector表达式
    :param istest: 如果为True,如果元素存在返回内容将为元素文本内容
    :return: 是否存在
    """
    try:
        target = elem.find_elements_by_css_selector(css_sel)
    except exceptions.NoSuchElementException:
        return False
    else:
        if istest:
            text = ""
            for i in range(len(target)):
                text += target[i].text
            return text
        return True


def insert_weibo(user_name, weibo_content, likes, comments, shares, tim, links_text):
    weibo.objects.create(
        username=user_name,
        article=weibo_content,
        likes_num=int(likes),
        comment_num=int(comments),
        transmit_num=int(shares),
        c_time=tim,
        pic_links=links_text,
    )
    pk = weibo.objects.get(username=user_name, article=weibo_content).pk
    return pk


def insert_first(user, comment, art_id):
    FirstComment.objects.create(
        username=user,
        context=comment,
        art_id=art_id,
    )
    return FirstComment.objects.get(
        username=user,
        context=comment
    ).pk


def insert_sec(user, reply, fir_id):
    SecondComment.objects.create(
        username=user,
        context=reply,
        com_id=fir_id,
    )
    return SecondComment.objects.get(
        username=user,
        context=reply
    ).pk


# 获取评论
def get_comments(driver, elem, num, art_id):
    try:
        # print("获取评论")
        elem.find_elements_by_css_selector('i.m-font.m-font-comment')[0].click()
        # https://m.weibo.cn/detail/4761425735847382
        print("点击了")
        time.sleep(4)
        # 根据评论数进行滑动并再获取0
        for i in range(int(num / 20)):
            scrob(driver)
        # 页面跳转

        pinluns_qu = driver.find_elements_by_css_selector('div.comment-content')  # 获取评论区
        # print(pinluns_qu)
        pinluns = pinluns_qu[0].find_elements_by_css_selector('div.m-text-box')  # 获取每个评论
        try:
            print("进入评论区了")
            for pinlun in pinluns:
                user = pinlun.find_element_by_css_selector('h4').text
                comment = pinlun.find_element_by_css_selector('h3').text
                # 获取到评论先根据帖子ID 写进第二张表，然后返回第二张表的ID
                # 获取到评论的回复之后再进行切割。获取第二张表的ID绑定 写入第三张表
                comment_reply = iselement(pinlun, 'div.cmt-sub-txt', True)
                print("评论回复的值是{}".format(str(comment_reply)))
                if comment_reply:
                    comment_reply = comment_reply.split(':')
                    # 写入第三张表
                    reply = ""
                    print(comment_reply)
                    for i in range(1, len(comment_reply)):
                        reply += comment_reply[i]
                else:
                    reply=''
                # 去重
                if FirstComment.objects.filter(username=user, context=comment):
                    if comment_reply:
                        # 更新评论的回复
                        queryset = SecondComment.objects.filter(username=comment_reply[0]).first()
                        queryset.context = reply
                        print("以更新评论{}的回复".format(comment))
                else:
                    first_id = insert_first(user, comment, art_id)
                    if comment_reply:
                        insert_sec(comment_reply[0], reply, first_id)
                    print("用户：{}，评论：{},评论的回复：{}".format(user, comment, comment_reply))
        except Exception as e:
            print(e)
            pass
        # 返回按钮
        btn = driver.find_element_by_css_selector("i.m-font.m-font-arrow-left")
        btn.click()
        time.sleep(3)


    except:
        pass


# 获取图片链接
def get_pic(elem):
    links = ""
    try:
        # 获取该条微博中的图片元素,之后遍历每个图片元素，获取图片链接并下载图片
        # 如果是多张图片
        if elem.find_elements_by_css_selector('div > div > article > div > div:nth-child(2) > div > ul > li') != []:
            pic_links = elem.find_elements_by_css_selector(
                'div > div > article > div > div:nth-child(2) > div > ul > li')
            for pic_link in pic_links:
                pic_link = pic_link.find_element_by_css_selector('div > img').get_attribute('src')
                links = pic_link + ";"
        # 如果图片只有一张
        else:
            pic_link = elem.find_element_by_css_selector(
                'div > div > article > div > div:nth-child(2) > div > div > img').get_attribute('src')
            links = pic_link + ";"
    except Exception as e:
        # print(e)
        pass
    return links


# 1.用于将cookie字符串转换为对象，因为后面add_cookie需要传字典进去
def ParseCookiestr(cookie_str):
    cookielist = []
    cookie_str = cookie_str.strip()
    for item in cookie_str.split(';'):
        temp = item.split('=')
        cookie = {}
        # 注意前导空格，不去除会unable to set cookie
        item_name = item.split('=')[0].strip()
        item_value = ""
        for i in range(1, len(temp)):
            item_value += temp[i]
        cookie['name'] = item_name
        # 将url上一堆转码的东西转回原始
        # cookie['value'] = urllib.parse.unquote(item_value)
        cookie['value'] = item_value
        cookielist.append(cookie)
    print(cookielist)
    return cookielist


def saveCookie(mode, cookies_file, webdriver):
    """

    :param mode: 使用的模式，selenium,pickle,json
    :param cookies_file: 存放cookies的文件路径
    :param webdriver: selenium的浏览器driver
    :return:
    """
    if mode == 'pickle':
        Cookies = webdriver.get_cookies()
        cookies = {}
        for itme in Cookies:
            cookies[itme['name']] = itme['value']
            outputPath = open(cookies_file, 'wb')  # 新建一个文件
            pickle.dump(cookies, outputPath)
            outputPath.close()
    elif mode == 'selenium':
        # 2,直接储存selenium
        with open(cookies_file, 'w') as f:
            json.dump(webdriver.get_cookies(), f)
    elif mode == 'json':
        # 1，json.loads错误,写入时应使用dump方法,数据本身一些没加“”，难搞，还是得转化，不能直接使用
        with open(cookies_file, 'w') as f:
            cookie = {}
            for i in webdriver.get_cookies():
                cookie[i['name']] = i['value']
            json.dump(cookie, f)


def useCookie(mode, cookies_file, webdriver):
    """
    mode : 使用的模式，brower,selenium,pickle,json
    cookies_file : 存放cookies的文件路径
    webdriver : selenium的浏览器driver
    :return:
    """
    # 删除原先所以cookies
    webdriver.delete_all_cookies()
    # 3，从浏览器复制的cookie转化使用
    if mode == 'brower':
        with open(cookies_file, 'r') as f:
            cookielist = ParseCookiestr(f.read())
            for i in cookielist:
                cookie = {}
                # 3.对于使用add_cookie来说，参考其函数源码注释，需要有name,value字段来表示一条cookie，有点生硬
                cookie['name'] = i['name']
                cookie['value'] = i['value']
                # 4.这里需要先删掉之前那次访问时的同名cookie，不然自己设置的cookie会失效
                webdriver.delete_cookie(i['name'])
                # 添加自己的cookie
                webdriver.add_cookie(cookie)
    elif mode == 'json':
        # 1，提取出name和value用json储存
        with open(cookies_file, 'r') as f:
            cookies = json.load(f)
            for key in cookies:
                cookie = {
                    'name': key,
                    'value': cookies[key]
                }
                webdriver.add_cookie(cookie)
    elif mode == 'pickle':
        # 2，使用pickle
        if os.path.exists(cookies_file):
            readPath = open(cookies_file, 'rb')
            cookies = pickle.load(readPath)
            for cookie in cookies:
                webdriver.add_cookie({
                    "name": cookie,
                    "value": cookies[cookie],
                })
    elif mode == 'selenium':
        # # 从selenium保存的cookie使用
        with open(cookies_file, 'r') as f:
            cookies = json.load(f)
            for cook in cookies:
                webdriver.add_cookie(cook)


def get_code():
    code = ''
    i = 0
    # 超过50秒获取不到就退出循环
    while code == '':
        # print(i)
        code = requests.get('http://106.53.108.157:8000/msg/get/').text
        # print(type(code))
        # print(code)
        i += 1
        if i > 5:
            break
        time.sleep(10)
    print(code)
    return code


def login(driver, username, password, cookies_file):
    # 如果存在cookies，默认用selenium自身保存的cookies
    if os.path.exists(cookies_file):
        sz = os.path.getsize(cookies_file)
        # 若为空文件不执行设置cookies
        if not sz:
            print(cookies_file, " is empty!")
            return "cookies文件为空"
        else:
            driver.get(url)
            time.sleep(3)
            useCookie('selenium', cookies_file, driver)
            driver.refresh()
            time.sleep(4)
    else:
        # 加载驱动，使用浏览器打开指定网址
        # driver.set_window_size(452, 790)
        # driver.get('https://m.weibo.cn')

        driver.get("https://passport.weibo.cn/signin/login")
        print("开始自动登陆，若出现验证码手动验证")
        time.sleep(3)

        elem = driver.find_element_by_xpath("//*[@id='loginName']")
        elem.send_keys(username)
        elem = driver.find_element_by_xpath("//*[@id='loginPassword']")
        elem.send_keys(password)
        elem = driver.find_element_by_xpath("//*[@id='loginAction']")
        elem.send_keys(Keys.ENTER)
        # print("暂停20秒，用于验证码验证")
        time.sleep(2)

        # 点击激活
        driver.find_element_by_xpath('//*[@id="protectGuide"]/div/div/div[3]/a').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="vdVerify"]/div[1]/div/div/div[3]/a').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="verifyCode"]/div[1]/div/div/div[2]/div/div/div/span[1]/input').send_keys(
            get_code())
        # 点击登录
        driver.find_element_by_xpath('//*[@id="verifyCode"]/div[1]/div/div/div[3]/a').click()
        # 保存cookies
        time.sleep(3)
        saveCookie('selenium', cookies_file, driver)
        print("cookie保存成功")
        return "登陆成功"


def spider(driver):
    driver.get(url)
    # 每页10个
    # for i in range(5):
    #     scrob()
    # # 先刷到100条再进行抓取，妈的直接失效
    # time.sleep(2)
    # elems = driver.find_elements_by_css_selector('div.card.m-panel.card9')
    # print(len(elems))
    # 先抓全文，用户等，再根据是否有评论再去抓评论
    for i in range(0, 10):
        # 在里面加srcb就会进不了评论区
        print("次数：" + str(i))
        if (i % 10) == 0:
            scrob(driver)
            time.sleep(3)
        elem = driver.find_elements_by_css_selector('div.card.m-panel.card9')[i]
        # 获取时间
        tim = elem.find_element_by_css_selector("span.time").text
        # print(tim)
        # print(driver.page_source)
        user_name = elem.find_elements_by_css_selector('h3.m-text-cut')[0].text
        # 微博内容
        # 点击“全文”，获取完整的微博文字内容
        weibo_content = get_all_text(driver, elem)
        # 获取图片链接
        links_text = get_pic(elem)
        # if links_text:
        #     print(links_text)
        # 获取分享数，评论数和点赞数
        shares = elem.find_elements_by_css_selector('i.m-font.m-font-forward + h4')[0].text
        if shares == '转发':
            shares = '0'
        likes = elem.find_elements_by_css_selector('i.m-icon.m-icon-like + h4')[0].text
        if likes == '赞':
            likes = '0'
        comments = elem.find_elements_by_css_selector('i.m-font.m-font-comment + h4')[0].text
        # print(comments)
        if comments == '评论':
            comments = '0'
        # 先写入第一张表，返回一个ID，传给评论获取
        # 去重：
        if weibo.objects.filter(username=user_name, article=weibo_content):
            queryset = weibo.objects.filter(username=user_name, article=weibo_content).first()
            if queryset.comment_num == int(comments):
                pass
            else:
                get_comments(driver, elem, int(comments), queryset.pk)
        else:
            art_id = insert_weibo(user_name, weibo_content, likes, comments, shares, tim, links_text)
            if comments != '0':
                get_comments(driver, elem, int(comments), art_id)
        print("用户名：{}，内容：{}，点赞：{}，评论：{}，转发：{}".format(user_name,weibo_content,likes,comments,shares))


def run():
    driver = webdriver.Chrome(options=opt)  # 你的chromedriver的地址
    # driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=opt)
    driver.implicitly_wait(2)  # 隐式等待2秒
    # 爬取
    username = '19965440781'
    password = 'buzhi123456'
    # username = '19304914193'
    # password = '123456buzhi'
    login(driver, username, password, 'cookie.txt')
    spider(driver)
    # driver.quit()


if __name__ == '__main__':
    run()
