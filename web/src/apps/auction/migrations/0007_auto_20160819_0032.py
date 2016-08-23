# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-19 00:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0006_auto_20160819_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_bids', to='auction.Product'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_bids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='bidders',
            field=models.ManyToManyField(related_name='bid_products', through='auction.Bid', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(related_name='category_products', through='auction.ProductCategory', to='auction.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='reviewers',
            field=models.ManyToManyField(related_name='reviewed_products', through='auction.Review', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_product_pairs', to='auction.Category'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_category_pairs', to='auction.Product'),
        ),
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to='auction.Product'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]