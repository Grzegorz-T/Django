# Generated by Django 3.0.8 on 2020-11-21 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_auto_20200908_1915'),
        ('members', '0006_auto_20201120_1905'),
        ('orders', '0010_auto_20201103_1849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='member_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='stock_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='stock_name',
        ),
        migrations.AddField(
            model_name='order',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.Member'),
        ),
        migrations.AddField(
            model_name='order',
            name='stock',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stocks.Stocks'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
