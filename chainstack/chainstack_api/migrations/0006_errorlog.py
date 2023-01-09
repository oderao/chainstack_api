# Generated by Django 4.1.4 on 2022-12-27 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chainstack_api", "0005_alter_newsitem_news_detail"),
    ]

    operations = [
        migrations.CreateModel(
            name="ErrorLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("log", models.TextField(null=True)),
                ("log_view", models.CharField(max_length=100, null=True)),
                ("log_id", models.CharField(max_length=100)),
            ],
        ),
    ]
