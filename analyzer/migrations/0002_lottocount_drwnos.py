# Generated by Django 3.0 on 2020-04-16 07:46

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lottocount',
            name='drwNos',
            field=django_mysql.models.ListCharField(models.IntegerField(default=1), default=1, max_length=8000, size=4),
            preserve_default=False,
        ),
    ]