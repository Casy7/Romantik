# Generated by Django 4.2 on 2024-10-19 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KaptyorkaApp', '0002_alter_equipment_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oldpriceofequipment',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=63, null=True),
        ),
    ]
