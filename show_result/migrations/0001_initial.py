# Generated by Django 2.2.12 on 2021-12-06 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='house',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=256, verbose_name='地址')),
                ('lat', models.FloatField(blank=True, verbose_name='緯度')),
                ('lon', models.FloatField(blank=True, verbose_name='經度')),
                ('unitPrice', models.FloatField(blank=True, verbose_name='每平方公尺單價')),
            ],
        ),
    ]