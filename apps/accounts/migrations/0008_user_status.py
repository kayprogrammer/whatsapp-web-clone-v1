# Generated by Django 4.1.2 on 2022-11-01 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_about_status_user_avatar_user_avatar_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(default="Hey There! I'm using Whatsapp Web Clone V1!", max_length=300),
        ),
    ]
