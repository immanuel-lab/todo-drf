# Generated by Django 4.2 on 2023-06-02 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]