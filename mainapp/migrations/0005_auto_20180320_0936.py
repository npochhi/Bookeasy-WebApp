# Generated by Django 2.0 on 2018-03-20 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20180319_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='institute_id',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default='', max_length=30),
        ),
    ]