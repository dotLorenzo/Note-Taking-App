# Generated by Django 3.0.5 on 2020-04-24 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0006_auto_20200424_1559'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='content',
            new_name='notes',
        ),
    ]