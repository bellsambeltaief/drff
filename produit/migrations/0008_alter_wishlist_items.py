# Generated by Django 3.2.6 on 2022-05-22 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produit', '0007_remove_wishlist_ref_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='items',
            field=models.ManyToManyField(to='produit.WishlistItem'),
        ),
    ]