# Generated by Django 4.0.1 on 2022-01-26 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='bookmark',
        ),
    ]