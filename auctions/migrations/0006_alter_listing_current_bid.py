# Generated by Django 5.0.3 on 2024-04-07 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_current_bid_bid_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='current_bid',
            field=models.IntegerField(default=None),
        ),
    ]