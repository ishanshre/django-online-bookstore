# Generated by Django 4.1.1 on 2022-10-12 03:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_order_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cartitems', to='orders.cart'),
        ),
    ]
