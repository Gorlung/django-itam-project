# Generated by Django 2.2.5 on 2019-09-29 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_app', '0010_asset_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='aquisition_date',
            field=models.DateField(null=True),
        ),
    ]
