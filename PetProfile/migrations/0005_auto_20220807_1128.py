# Generated by Django 3.1.5 on 2022-08-07 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PetProfile', '0004_auto_20220710_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importpetprofile',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='petprofile',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]