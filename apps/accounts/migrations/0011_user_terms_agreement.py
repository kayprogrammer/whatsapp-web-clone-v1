# Generated by Django 4.1.2 on 2022-11-01 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_blockedcontact_unique_blocker_blockee'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='terms_agreement',
            field=models.BooleanField(default=False),
        ),
    ]
