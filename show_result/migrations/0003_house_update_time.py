# Generated by Django 2.2.12 on 2021-12-07 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show_result', '0002_auto_20211207_0220'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新時間'),
        ),
    ]
