# Generated by Django 4.0.3 on 2022-03-14 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("salesmanbasket", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basket",
            name="extra",
            field=models.JSONField(blank=True, default=dict, verbose_name="Extra"),
        ),
        migrations.AlterField(
            model_name="basketitem",
            name="extra",
            field=models.JSONField(blank=True, default=dict, verbose_name="Extra"),
        ),
    ]
