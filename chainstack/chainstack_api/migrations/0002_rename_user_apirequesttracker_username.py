# Generated by Django 4.1.4 on 2022-12-25 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chainstack_api", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="apirequesttracker",
            old_name="user",
            new_name="username",
        ),
    ]
