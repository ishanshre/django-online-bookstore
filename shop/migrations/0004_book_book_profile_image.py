# Generated by Django 4.1.1 on 2022-10-02 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_bookimages_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_profile_image',
            field=models.ImageField(blank=True, default='default_book.png', null=True, upload_to='book_profile/'),
        ),
    ]
