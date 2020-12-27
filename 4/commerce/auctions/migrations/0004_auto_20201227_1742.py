# Generated by Django 3.1.2 on 2020-12-27 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auctionlistings_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='image_url',
            field=models.ImageField(blank=True, upload_to='static/auctions/media/'),
        ),
        migrations.AlterField(
            model_name='auctionlistings',
            name='isActive',
            field=models.BooleanField(blank=True),
        ),
    ]