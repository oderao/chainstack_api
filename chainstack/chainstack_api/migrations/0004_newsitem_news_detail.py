# Generated by Django 4.1.4 on 2022-12-26 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chainstack_api", "0003_rename_username_apirequesttracker_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="newsitem",
            name="news_detail",
            field=models.TextField(null=True),
        ),
    ]
