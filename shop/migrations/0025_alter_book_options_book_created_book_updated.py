# Generated by Django 4.1.1 on 2022-10-16 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_alter_review_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['created']},
        ),
        migrations.AddField(
            model_name='book',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
