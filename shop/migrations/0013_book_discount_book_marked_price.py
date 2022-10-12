# Generated by Django 4.1.1 on 2022-10-12 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_alter_author_description_alter_book_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='discount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='marked_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
