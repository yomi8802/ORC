# Generated by Django 3.1 on 2023-07-12 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orc', '0002_auto_20230712_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apcount',
            name='ap_count',
            field=models.IntegerField(default=0, verbose_name='AP数'),
        ),
    ]
