# Generated by Django 4.2.6 on 2024-02-22 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_category_product_category_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='stars',
            field=models.ImageField(default=5, null=True, upload_to=''),
        ),
    ]
