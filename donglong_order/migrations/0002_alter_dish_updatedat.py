# Generated by Django 4.2.11 on 2024-03-13 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donglong_order", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dish",
            name="updatedAt",
            field=models.DateTimeField(auto_now=True, null=True, verbose_name="修改时间"),
        ),
    ]
