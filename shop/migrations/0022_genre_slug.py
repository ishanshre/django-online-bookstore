# Generated by Django 4.1.1 on 2022-10-14 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_alter_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
