# Generated by Django 3.0.8 on 2020-11-30 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_member_capital'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='profit',
            field=models.FloatField(default=0),
        ),
    ]
