# Generated by Django 3.0 on 2024-07-08 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(default='', max_length=11, unique=True, verbose_name='手机号')),
                ('captcha', models.CharField(max_length=4, null=True, verbose_name='验证码')),
            ],
        ),
        migrations.CreateModel(
            name='Ocr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='日期')),
                ('img', models.FileField(max_length=128, upload_to='ocr/', verbose_name='图片')),
                ('mobile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ocr.User', verbose_name='手机号')),
            ],
        ),
    ]