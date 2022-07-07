import csv
import os
from datetime import datetime
from django.contrib import admin, messages
from django.http import HttpResponse
import pandas as pd
from .models import PetProfile, ImportPetProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

exportable_fields = (
    'user',
    'pet_name',
    'pet_id',
    'pet_age',
    'pet_breed',
    'pet_gender',
    'modified_date',
    'pet_illness',
    'is_handle',
)


def export_csv(modeladmin, request, queryset):
    """
    :param model_admin: 要求model_admin中必须定义list_display字段
    :param request:
    :param queryset: 为界面中选中的queryset obj集合
    :return: response下载
    """
    field_list = exportable_fields

    output_file_path = 'export/petprofile/petprofile.csv'

    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    with open(output_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', delimiter=',')
        # 写入表头
        writer.writerow([queryset.model._meta.get_field(f).verbose_name.title() for f in field_list], )
        for obj in queryset:
            # 每行记录的值
            csv_line_values = []
            for field in field_list:
                field_object = queryset.model._meta.get_field(field)
                field_value = field_object.value_from_object(obj)
                csv_line_values.append(field_value)
            writer.writerow(csv_line_values)
            # print(csv_line_values)

    f = open(output_file_path, 'rb')
    # Build your response
    response = HttpResponse(f.read(), content_type='text/csv')
    # response实现文件下载
    response['Content-Disposition'] = 'attachment; filename="petprofile.csv"'
    f.close()

    return response


# 设置函数的short_description属性，指定这个操作在模板中显示的名字
export_csv.short_description = '导出数据'


# Register your models here.


class PetProfileInline(admin.StackedInline):
    model = PetProfile
    # fields = ['pet_name', 'pet_id', ]# 展示某些字段


class PetProfileAdmin(admin.ModelAdmin):
    list_display = [
        # 'user__username',
        'user',
        # 'user__username',
        'pet_name',
        'pet_id',
        'pet_age',
        'pet_breed',
        'pet_gender',
        'modified_date',
        'last_editor',
        # 'pet_illness',
        'is_handle',
    ]

    list_editable = [
        'is_handle'
    ]
    list_filter = ['pet_breed', 'pet_age', 'pet_gender', 'user__email', ]

    search_fields = ['pet_name', 'user_telephone', 'pet_breed', 'pet_id']

    actions = [export_csv, ]

    # 记录最后编辑时间和编辑者
    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user.username
        obj.modified_date = datetime.now()
        obj.save()


# 定义一个行内 admin
# class UserInline(admin.StackedInline):
#     model = User


# 将 PetProfile 关联到 User 中
class UserAdmin(BaseUserAdmin):
    inlines = [PetProfileInline, ]

# 导入信息操作
class ImportPetProfileAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):

        # 先保存，再进入后续操作
        obj.save()
        print(obj.import_file)
        # 读取导入的文件
        file_path = 'appendix/{}'.format(obj.import_file)
        print(file_path)
        df = pd.read_excel(file_path)
        print(df['宠物身份证号'])

        # 检查宠物身份证号是否已经注册过
        existed_people = []
        df['宠物身份证号'] = df['宠物身份证号'].astype(str)
        for i in range(len(df['宠物身份证号'])):
            pet_id = df['宠物身份证号'][i]
            try:
                PetProfile.objects.get(pet_id=pet_id)
                existed_people.append(df['宠物身份证号'][i])
            except:
                pass
        if existed_people:
            # 得到未提交列表
            error_type = '用户信息已存在'
            for people in existed_people:
                error_message = '导入失败，{}已注册过账号，请检查后重新上传'.format(people)
                messages.error(request, error_message)
            # 出现错误就删除文件，免得占内存
            os.remove(file_path)
            return False
        # 检查是否有空值，
        check_list = df.isnull().any().tolist()
        if True in check_list:
            error_message = '数据中存在空值，请仔细检查后导入'
            messages.error(request, error_message)
            # 出现错误就删除文件，免得占内存，
            os.remove(file_path)
            return False
        # 检查完毕，开始导入
        for i in range(len(df)):
            username = df["姓名"][i]
            user_phone = df["手机号码"][i]
            user_email = df["邮箱"][i]
            # user_id = int(df["User"][i].strip())
            pet_id = int(df['宠物身份证号'][i].strip())
            pet_name = df["宠物姓名"][i].strip()
            pet_age = int(df["宠物年龄"][i])
            pet_breed = df["宠物种类"][i]
            pet_gender = df["宠物性别"][i]
            pet_illness = df["宠物病情"][i]
            is_handle = df["处理状态"][i]

            User.objects.create_user(
                username=username,
                # 默认密码为手机号
                password=str(user_phone),
                email=user_email,
            )

            # 获取创建的用户在django自带用户系统中的id，后续外键绑定需要用到
            pk = User.objects.get(username=username).pk
            print(pk)

            PetProfile.objects.create(
                user_telephone=user_phone,
                user_id=pk,
                pet_id=pet_id,
                pet_name=pet_name,
                pet_age=pet_age,
                pet_breed=pet_breed,
                pet_gender=pet_gender,
                pet_illness=pet_illness,
                is_handle=is_handle,
            )

            text = '{}({})成功导入({}/{})'.format(pet_name, df['宠物姓名'][i], i + 1, len(df))
            messages.success(request, text)


admin.site.register(PetProfile, PetProfileAdmin)
# 导入信息的
admin.site.register(ImportPetProfile, ImportPetProfileAdmin)
# 重新注册 User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
