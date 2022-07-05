from django.db import models
# 导入django自带的用户表作为外键
from django.contrib.auth.models import User

# Create your models here.

GENDER_TYPE = (
    ('男', '男'),
    ('女', '女'),
)


class PetProfile(models.Model):
    # 字段加上null=True, blank=True时就可以创建一个链接user的空对象
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_telephone = models.CharField(max_length=50, blank=True, verbose_name='联系方式', null=True)

    pet_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='宠物姓名')
    pet_age = models.SmallIntegerField(verbose_name='宠物年龄', null=True, blank=True)
    pet_id = models.IntegerField(unique=True, verbose_name='宠物编号', null=True, blank=True)
    pet_breed = models.CharField(max_length=50, blank=True, verbose_name='宠物种类', null=True)
    pet_gender = models.CharField(choices=GENDER_TYPE, max_length=50, blank=True, verbose_name='宠物性别', null=True)
    pet_physical_date = models.DateTimeField(auto_now=True, verbose_name='最后体检时间', null=True, blank=True)

    class Meta:
        verbose_name = 'Pet Profile'

    def __str__(self):
        return "{}".format(self.user.__str__())
