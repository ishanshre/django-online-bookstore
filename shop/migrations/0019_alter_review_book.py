# Generated by Django 4.1.1 on 2022-10-12 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_alter_review_book_alter_review_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='book',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='book_reviews', to='shop.book'),
        ),
    ]
