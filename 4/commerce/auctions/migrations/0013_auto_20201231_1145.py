# Generated by Django 3.1.2 on 2020-12-31 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auctionlistings_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
