# Generated by Django 3.1.2 on 2020-12-31 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_bids'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlistings',
            name='user',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]