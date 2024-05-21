# Generated by Django 4.2.13 on 2024-05-21 16:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_page", "0005_bill"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bill",
            options={
                "ordering": ["-date"],
                "verbose_name": "Bill",
                "verbose_name_plural": "Bills",
            },
        ),
        migrations.RemoveField(
            model_name="bill",
            name="cart_item_ids",
        ),
        migrations.AddField(
            model_name="bill",
            name="cart_items",
            field=models.ManyToManyField(related_name="bills", to="admin_page.cart"),
        ),
    ]
