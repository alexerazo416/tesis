# Generated by Django 5.0.6 on 2024-08-20 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0002_remove_bicicleta_estado_bic_bicicleta_accesorios_bic_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
