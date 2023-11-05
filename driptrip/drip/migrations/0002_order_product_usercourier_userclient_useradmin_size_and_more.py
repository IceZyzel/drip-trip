# Generated by Django 4.2.6 on 2023-11-05 14:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drip', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adress', models.CharField(max_length=64)),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.CharField(max_length=64)),
                ('brand', models.CharField(max_length=64)),
                ('description', models.TextField(max_length=250)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unisex')], max_length=1)),
                ('category', models.TextField(max_length=250)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='UserCourier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.user')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=10)),
                ('count', models.PositiveBigIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.product')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=250)),
                ('rate', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('date', models.DateField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.product')),
                ('userclient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.userclient')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='userclient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.userclient'),
        ),
        migrations.CreateModel(
            name='PhotoProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photolink', models.CharField(max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='userclient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.userclient'),
        ),
        migrations.AddField(
            model_name='order',
            name='usercourier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.usercourier'),
        ),
    ]