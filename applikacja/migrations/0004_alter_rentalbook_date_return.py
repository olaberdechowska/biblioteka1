# Generated by Django 4.2.1 on 2023-06-22 16:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("applikacja", "0003_alter_catalog_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rentalbook",
            name="date_return",
            field=models.DateField(blank=True, null=True),
        ),
    ]
