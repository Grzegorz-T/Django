# Generated by Django 3.0.8 on 2020-08-22 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks',
            name='change',
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stocks',
            name='max',
            field=models.FloatField(default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stocks',
            name='min',
            field=models.FloatField(default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stocks',
            name='opening',
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stocks',
            name='perc',
            field=models.FloatField(default=4),
            preserve_default=False,
        ),
    ]
