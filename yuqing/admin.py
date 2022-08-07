from django.contrib import admin

from .models import *


class FirstCommentInline(admin.StackedInline):
    model = FirstComment


class SecondCommentInline(admin.StackedInline):
    model = SecondComment




# Register your models here.
class weiboAdmin(admin.ModelAdmin):
    list_display = ['username', 'article', 'likes_num', 'comment_num', 'c_time', 'pic_links']

    '''此错误只需把inlines里面的引号去掉即可，注意内联类要在此前定义
    'yuqing.FirstCommentAdmin' must inherit from 'InlineModelAdmin'.
    '''

    inlines = [FirstCommentInline]


class FirstCommentAdmin(admin.ModelAdmin):
    list_display = ['username', 'context','art']
    inlines = [SecondCommentInline]

class SecondCommentAdmin(admin.ModelAdmin):
    list_display = ['username','context','com']
admin.site.register(weibo, weiboAdmin)
admin.site.register(SecondComment, SecondCommentAdmin)
admin.site.register(FirstComment, FirstCommentAdmin)

