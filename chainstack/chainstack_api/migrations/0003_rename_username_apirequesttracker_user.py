# Generated by Django 4.1.4 on 2022-12-25 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chainstack_api", "0002_rename_user_apirequesttracker_username"),
    ]

    operations = [
        migrations.RenameField(
            model_name="apirequesttracker",
            old_name="username",
            new_name="user",
        ),
    ]
