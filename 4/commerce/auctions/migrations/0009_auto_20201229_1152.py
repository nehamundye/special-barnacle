# Generated by Django 3.1.2 on 2020-12-29 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20201227_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlistings',
            name='id',
        ),
        migrations.AddField(
            model_name='auctionlistings',
            name='listing_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
