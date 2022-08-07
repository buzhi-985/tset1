from django.db import models


# Create your models here.
class weibo(models.Model):
    username = models.CharField(max_length=30, verbose_name='用户名')
    article = models.CharField(max_length=500, verbose_name='文章')
    # 点赞，评论，转发,帖子
    likes_num = models.IntegerField(verbose_name='点赞数')
    comment_num = models.IntegerField(verbose_name='评论数')
    transmit_num = models.IntegerField(verbose_name='转发数')
    c_time = models.CharField(max_length=50, verbose_name='最后回复时间')
    pic_links = models.CharField(max_length=500, verbose_name='图片链接', null=True, blank=True)
    art_links = models.CharField(max_length=200, verbose_name='文章链接', null=True, blank=True)



    class Meta:
        verbose_name = '微博帖子'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.article)



class FirstComment(models.Model):
    username = models.CharField(max_length=30, verbose_name='用户名')
    context = models.CharField(max_length=500, verbose_name='评论内容')
    art = models.ForeignKey('weibo', on_delete=models.CASCADE, related_name='firstcomment',verbose_name="文章")

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
    def __str__(self):
        return "{}".format("".join(self.context))


class SecondComment(models.Model):
    username = models.CharField(max_length=30, verbose_name='用户名')
    context = models.CharField(max_length=500, verbose_name='评论回复内容')
    com = models.ForeignKey('FirstComment', on_delete=models.CASCADE, related_name='secondcomment',verbose_name="评论")
    art = models.ForeignKey('weibo', on_delete=models.CASCADE, related_name='secondcomment',verbose_name="评论")

    class Meta:
        verbose_name='评论的回复'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format("".join(self.context))


"""获取方法
def index(res):
    user = User.objects.get(pk=1)
    all_articles = user.articles.all() # 使用关联名称 articles来取数据
    print(all_articles)
    # <QuerySet [<Article: Article object (1)>, <Article: Article object (3)>]>
    return render(res, 'test_html.html')
    """
