# Generated by Django 3.2.13 on 2022-07-11 04:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ClerkProfile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clerkpayroll',
            name='clerk',
            field=models.OneToOneField(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, related_name='clerkprofile1', to='ClerkProfile.clerkprofile'),
            preserve_default=False,
        ),
    ]