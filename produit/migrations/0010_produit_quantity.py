# Generated by Django 3.2.6 on 2022-05-29 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produit', '0009_produit_vender'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='quantity',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
