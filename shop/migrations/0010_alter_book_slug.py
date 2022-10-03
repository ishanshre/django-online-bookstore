# Generated by Django 4.1.1 on 2022-10-02 10:38

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_author_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=('title',), unique=True, verbose_name='slug'),
        ),
    ]
