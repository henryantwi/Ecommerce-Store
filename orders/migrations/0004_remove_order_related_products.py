# Generated by Django 4.2.6 on 2024-01-14 22:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0003_alter_order_status_alter_ordertracking_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="related_products",
        ),
    ]