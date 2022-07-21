# Generated by Django 3.2.13 on 2022-07-10 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PetProfile', '0003_auto_20220706_1756'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='importpetprofile',
            options={'verbose_name': '批量导入PetProfile信息', 'verbose_name_plural': '批量导入PetProfile信息'},
        ),
        migrations.AlterField(
            model_name='petprofile',
            name='user_telephone',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='用户联系方式'),
        ),
    ]