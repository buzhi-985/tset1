# Generated by Django 3.2.13 on 2022-07-11 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ClerkProfile', '0003_alter_clerkpayroll_clerk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clerkpayroll',
            name='clerk',
        ),
    ]
