# Generated by Django 4.2.7 on 2023-11-16 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drip', '0011_alter_order_usercourier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(),
        ),
    ]
