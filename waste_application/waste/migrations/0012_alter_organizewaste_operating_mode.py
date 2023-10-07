# Generated by Django 4.1.6 on 2023-02-08 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0011_alter_organizewaste_operating_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizewaste',
            name='operating_mode',
            field=models.CharField(choices=[('Периодически', 'Периодически'), ('Постоянно', 'Постоянно')], default='Периодически', max_length=12, verbose_name='Режим работы технологического оборудования'),
        ),
    ]