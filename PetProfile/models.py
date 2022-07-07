from django.db import models
# 导入django自带的用户表作为外键
from django.contrib.auth.models import User

# Create your models here.

GENDER_TYPE = (
    ('男', '男'),
    ('女', '女'),
)
HANDLE_TYPES = (
    ('未处理', '未处理'),
    ("已处理", '已处理'),
    ('已拒绝', '已拒绝'),
)


class PetProfile(models.Model):
    # 字段加上null=True, blank=True时就可以创建一个链接user的空对象
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_telephone = models.CharField(max_length=50, blank=True, verbose_name='联系方式', null=True)
    # user_id = models.CharField(max_length=18,blank=True,null=True,verbose_name="用户身份证")

    pet_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='宠物姓名')
    pet_age = models.SmallIntegerField(verbose_name='宠物年龄', null=True, blank=True)
    pet_id = models.IntegerField(unique=True, verbose_name='宠物身份证号', null=True, blank=True)
    pet_breed = models.CharField(max_length=50, blank=True, verbose_name='宠物种类', null=True)
    pet_gender = models.CharField(choices=GENDER_TYPE, max_length=50, blank=True, verbose_name='宠物性别', null=True)
    # pet_physical_date = models.DateTimeField(auto_now=True, verbose_name='最后体检时间', null=True, blank=True)
    #
    pet_illness = models.CharField(max_length=500, verbose_name="宠物病情", null=True, blank=True)
    reply = models.CharField(max_length=500, verbose_name='医生意见', null=True, blank=True)
    is_handle = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        choices=HANDLE_TYPES,
        default='未处理',
        verbose_name='处理状态')

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='问诊时间', null=True, blank=True)
    modified_date = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name='更新时间')
    last_editor = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name='最后处理者')

    class Meta:
        verbose_name = 'Pet Profile'

    def __str__(self):
        return "{}".format(self.user.__str__())


class ImportPetProfile(models.Model):
    import_file = models.FileField(verbose_name='上传文件', upload_to='upload/')
    handle_text = models.TextField(verbose_name='处理信息', null=True, blank=True)

    class Meta:
        verbose_name = '批量导入Pet信息'
        verbose_name_plural = verbose_name
