# Generated by Django 3.0.8 on 2022-01-30 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis_v1', '0002_auto_20220130_0613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='output',
            field=models.ImageField(null=True, upload_to='results/'),
        ),
    ]