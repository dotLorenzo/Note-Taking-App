# Generated by Django 3.0.6 on 2020-06-16 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'ordering': ['category'], 'verbose_name_plural': 'Categories'},
        ),
    ]
