# Generated by Django 3.0.8 on 2022-01-30 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('img', models.ImageField(upload_to='results/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
