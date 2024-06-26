# Generated by Django 4.2.11 on 2024-05-18 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('id_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_page.product')),
                ('id_size', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_page.size')),
            ],
            options={
                'unique_together': {('id_product', 'id_size')},
            },
        ),
    ]
