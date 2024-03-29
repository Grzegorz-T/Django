# Generated by Django 3.0.8 on 2020-09-08 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField()),
                ('member_id', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('owned', models.IntegerField()),
                ('stock_id', models.IntegerField()),
                ('purchase_price', models.FloatField()),
                ('buy_sell', models.BooleanField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.DeleteModel(
            name='Orders',
        ),
    ]
