# Generated by Django 5.0.7 on 2024-08-27 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_profile_old_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='old_cart',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
