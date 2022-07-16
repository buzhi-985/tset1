from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from PetProfile.models import GENDER_TYPE

HANDLE_TYPES = (
    ('未处理', '未处理'),
    ("未发放", '未发放'),
    ('已发放', '已发放'),
)


class ClerkProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='clerkprofile')
    user_phone = models.CharField(max_length=50, blank=True, verbose_name='员工联系方式', null=True)
    user_position = models.CharField(max_length=50,  blank=True, verbose_name='员工职位', null=True)
    user_age = models.IntegerField(verbose_name='员工年龄', null=True, blank=True)
    user_gender = models.CharField(choices=GENDER_TYPE, max_length=10, blank=True, verbose_name='员工性别', null=True)

    def __str__(self):
        return "{}".format(self.user.__str__(),self.user_position,self.user_phone,self.user_age,self.user_gender)



class ClerkPayroll(models.Model):
    # clerk = models.OneToOneField(ClerkProfile,on_delete=models.CASCADE,related_name="clerkprofile1",blank=True,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='payrollprofile',verbose_name="用户")
    user_position = models.CharField(max_length=50, blank=True, verbose_name='员工职位', null=True)
    user_salary = models.IntegerField(blank=True, verbose_name='员工工资', null=True)
    month = models.CharField(blank=True, null=True, verbose_name="月份",max_length=50)
    modified_date = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')
    last_editor = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name='最后处理者')
    is_handle = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        choices=HANDLE_TYPES,
        default='未处理',
        verbose_name='处理状态')
