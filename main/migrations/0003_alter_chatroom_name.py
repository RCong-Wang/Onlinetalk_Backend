# Generated by Django 3.2.15 on 2024-01-17 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20240117_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]