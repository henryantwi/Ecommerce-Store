# Generated by Django 4.2.6 on 2024-01-14 15:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="related_products",
            field=models.TextField(null=True),
        ),
    ]
