# Generated by Django 5.1.2 on 2024-10-18 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca_app', '0002_alter_reserva_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='fecha_expiracion',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
