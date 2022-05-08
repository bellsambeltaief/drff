# Generated by Django 3.2.6 on 2022-05-08 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produit', '0002_alter_produit_prod_name_alter_produit_prod_regno'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produit',
            name='prod_regNo',
        ),
        migrations.AddField(
            model_name='produit',
            name='category',
            field=models.CharField(blank=True, choices=[('Shirt', 'Shirt'), ('Sport wear', 'Sport wear'), ('Outwear', 'Outwear'), ('Tech', 'Tecknology'), ('Camping', 'Camping')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='produit',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='produit',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='produit',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='produit',
            name='prod_name',
            field=models.CharField(max_length=255),
        ),
    ]