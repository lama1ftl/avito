# Generated by Django 4.0 on 2022-01-05 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_alter_user_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=20, null=True, verbose_name='city'),
        ),
    ]
