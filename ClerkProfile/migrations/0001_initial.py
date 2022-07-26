# Generated by Django 3.2.13 on 2022-07-21 09:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClerkProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='员工联系方式')),
                ('user_position', models.CharField(blank=True, max_length=50, null=True, verbose_name='员工职位')),
                ('user_age', models.IntegerField(blank=True, null=True, verbose_name='员工年龄')),
                ('user_gender', models.CharField(blank=True, choices=[('男', '男'), ('女', '女')], max_length=10, null=True, verbose_name='员工性别')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='clerkprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClerkPayroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_position', models.CharField(blank=True, max_length=50, null=True, verbose_name='员工职位')),
                ('user_salary', models.IntegerField(blank=True, null=True, verbose_name='员工工资')),
                ('month', models.CharField(blank=True, max_length=50, null=True, verbose_name='月份')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('last_editor', models.CharField(blank=True, max_length=128, null=True, verbose_name='最后处理者')),
                ('is_handle', models.CharField(blank=True, choices=[('未处理', '未处理'), ('未发放', '未发放'), ('已发放', '已发放')], default='未处理', max_length=20, null=True, verbose_name='处理状态')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payrollprofile', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
    ]
