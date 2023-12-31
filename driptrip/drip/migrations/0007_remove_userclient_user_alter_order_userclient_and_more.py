# Generated by Django 4.2.6 on 2023-11-10 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drip', '0006_alter_photoproduct_photolink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userclient',
            name='user',
        ),
        migrations.AlterField(
            model_name='order',
            name='userclient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.user'),
        ),
        migrations.AlterField(
            model_name='product',
            name='userclient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.user'),
        ),
        migrations.AlterField(
            model_name='review',
            name='userclient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drip.user'),
        ),
        migrations.DeleteModel(
            name='UserAdmin',
        ),
        migrations.DeleteModel(
            name='UserClient',
        ),
    ]
