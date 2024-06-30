# Generated by Django 4.2.13 on 2024-06-29 15:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(error_messages={'unique': 'نام کاربری انتخاب شده قبلا استفاده شده است.'}, max_length=150, unique=True)),
                ('email', models.EmailField(error_messages={'unique': 'این ایمیل قبلا ثبت شده است.'}, max_length=254, unique=True, validators=[django.core.validators.EmailValidator(message='ایمیل معتبر نیست.')])),
                ('password', models.CharField(max_length=128)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]