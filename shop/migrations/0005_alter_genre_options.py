# Generated by Django 4.1.1 on 2022-10-02 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_book_book_profile_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['genre']},
        ),
    ]
