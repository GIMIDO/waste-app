# Generated by Django 4.1.3 on 2023-01-02 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0004_organizewaste_code_zv_organizewaste_operating_mode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='boilerwaste',
            name='fuel',
            field=models.CharField(choices=[('Газ природ.', 'Газ природ.'), ('Дизтопливо', 'Дизтопливо')], default='Газ природ.', max_length=20, verbose_name='Наименование топлива, сырья, материалов'),
        ),
        migrations.AddField(
            model_name='boilerwaste',
            name='number',
            field=models.CharField(default=4, max_length=6, verbose_name='Номер источника'),
        ),
        migrations.AlterField(
            model_name='organizewaste',
            name='operating_mode',
            field=models.CharField(choices=[('Постоянно', 'Постоянно'), ('Периодически', 'Периодически')], default='Периодически', max_length=12, verbose_name='Режим работы технологического оборудования'),
        ),
    ]
