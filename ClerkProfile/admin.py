import datetime

import xlrd, xlwt
from django.contrib import admin
from django.http import HttpResponse
from xlutils.copy import copy

from .models import ClerkPayroll, ClerkProfile


def setStyle(name, height, color, bold=False, align=True, border=False):
    """
    xlwt字体写入设置
    """
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    # 字体类型：比如宋体、仿宋也可以是汉仪瘦金书繁
    font.name = name
    # 设置字体颜色
    font.colour_index = color
    # 字体大小
    font.height = height
    # 字体加粗
    font.bold = bold
    # 定义格式
    style.font = font

    if border:
        # 框线
        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        style.borders = borders

    if align:
        # 设置单元格对齐方式
        al = xlwt.Alignment()
        # 0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
        al.horz = 0x02
        # 0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)
        al.vert = 0x01
        style.alignment = al

    return style


# 工资明细导出字段
field_list = ['user', 'user_position', 'user_salary', 'month', 'modified_date', 'is_handle', 'last_editor']


def export_xls(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=DEMO.xls'
    rd = xlrd.open_workbook("export/clerkprofile/template.xls", formatting_info=True)  # 打开文件
    workbook = copy(rd)  # 复制
    worksheet = workbook.get_sheet(0)  # 获取第一个sheet
    # 这里的height代表字号大小，换算公式为字号height = 字号 * 20
    # name代表字体，bold、align、border分别控制是否加粗、居中对齐，所有边框
    style = setStyle(name='宋体', height=240, color=256, bold=True, align=True, border=True)
    title_style = setStyle(name='方正小标宋简体', height=360, color=256, bold=False, align=False, border=False)

    # 写入标题
    worksheet.write_merge(0, 1, 1, 7, '不知宠物医院{}工资明细表'.format(datetime.datetime.now().strftime('%Y-%m')), title_style)

    # 第一个参数为单元格行，第二个为单元格列
    verbose_list = [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    verbose_list.insert(0, "序号")

    # 获取字符串长度
    def string_len(string):
        length = 0
        for s in string:
            if s.isupper() or s.islower():
                length += 2
            elif s.isspace():
                length += 1
            else:
                length += 3
        # print(length)
        return length

    # 写入字段名
    for i in range(0, len(verbose_list)):
        worksheet.write(2, i, verbose_list[i], style)
        # 自适应列宽
        '''
        sheet也有设置列宽度方法 worksheet5.col(3).width = 256 * 16
        xlwt中列宽的值表示方法：默认字体0的1/256为衡量单位
        xlwt创建时使用的默认宽度为2960，既11个字符0的宽度
        '''
        worksheet.col(i).width = string_len(verbose_list[i]) * 256

    # 写入序号并写入每行
    salary_count = 0
    style = setStyle(name='宋体', height=240, color=256, bold=False, align=True, border=True)
    index = 3  # 第一个索引所在的行
    for i in range(0, len(queryset)):
        worksheet.write(index, 0, i, style)
        obj = queryset[i]
        worksheet.write(index, 1, obj.user.__str__(), style)
        worksheet.write(index, 2, obj.user_position, style)
        worksheet.write(index, 3, obj.user_salary, style)
        salary_count += int(obj.user_salary)
        worksheet.write(index, 4, obj.month, style)
        worksheet.write(index, 5, obj.modified_date.strftime('%dday %H-%M-%S'), style)
        worksheet.write(index, 6, obj.is_handle, style)
        worksheet.write(index, 7, obj.last_editor, style)
        index += 1
    text = '总人数：{} 工资合计：{}'.format(len(queryset), salary_count)
    # 写入合并的单元格
    worksheet.write_merge(index + 3, index + 3, 2, 3, text, style)
    worksheet.col(2).width = string_len(text) * 256
    workbook.save(response)
    return response


export_xls.short_description = '导出工资数据'


class ClerkProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_phone', 'user_position', 'user_age', 'user_gender']


# Register your models here.
class ClerkPayrollAdmin(admin.ModelAdmin):
    list_display = field_list
    list_editable = ['is_handle', ]
    actions = [export_xls, ]


admin.site.register(ClerkPayroll, ClerkPayrollAdmin)
admin.site.register(ClerkProfile, ClerkProfileAdmin)
