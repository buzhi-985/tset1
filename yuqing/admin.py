from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class FirstCommentInline(admin.StackedInline):
    model = FirstComment
    fields = ['art', ]
    readonly_fields = ['username']



class SecondCommentInline(admin.StackedInline):
    model = SecondComment
    fields = ('com',)
    readonly_fields = ['com']



# Register your models here.
class weiboAdmin(admin.ModelAdmin):
    list_display = ['username', 'article', 'likes_num', 'comment_num', 'c_time', 'url_tag', 'img_tag']
    readonly_fields = ['username', 'article', 'likes_num', 'comment_num', 'c_time', 'url_tag', 'img_tag','transmit_num']
    exclude = ('pic_links','art_links')
    inlines = [FirstCommentInline, SecondCommentInline]

    def url_tag(self, obj):
        if obj.art_links:
            return mark_safe(
                f'<a href="{obj.art_links}" target="_blank" >微博帖子地址</a>')
        return '-'

    url_tag.short_description = '微博帖子地址'

    def img_tag(self, obj):
        img_html = ''
        if obj.pic_links != '':
            img_list = obj.pic_links.split(';')
            img_list.remove(img_list[len(img_list)-1]) # 删除最后一个空元素
            for img in img_list:
                img_html += f'<image src="{img}" style="width:160px; height:160px;" alt="图片" />'
            return mark_safe(img_html)
        return '-'

    img_tag.short_description = '微博帖子图片'


    '''此错误只需把inlines里面的引号去掉即可，注意内联类要在此前定义
    'yuqing.FirstCommentAdmin' must inherit from 'InlineModelAdmin'.
    '''



class FirstCommentAdmin(admin.ModelAdmin):
    list_display = ['username', 'context', 'art']
    inlines = [SecondCommentInline]
    readonly_fields = ['username', 'context', 'art']


class SecondCommentAdmin(admin.ModelAdmin):
    list_display = ['username', 'context', 'com']
    readonly_fields = ['username', 'context', 'com']


admin.site.register(weibo, weiboAdmin)
admin.site.register(SecondComment, SecondCommentAdmin)
admin.site.register(FirstComment, FirstCommentAdmin)
