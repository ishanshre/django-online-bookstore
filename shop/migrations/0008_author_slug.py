# Generated by Django 4.1.1 on 2022-10-02 10:29

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_remove_author_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=('firs_name', 'last_name'), unique=True, verbose_name='slug'),
        ),
    ]
