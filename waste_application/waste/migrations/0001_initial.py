# Generated by Django 4.1.3 on 2022-12-06 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoilerWaste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('K', models.DecimalField(decimal_places=4, default=4.1868, max_digits=5, verbose_name='К')),
                ('q3', models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='q3, %')),
                ('R', models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='R')),
                ('Bk', models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='Bk')),
                ('Bt', models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='Bt')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizeWaste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emission_source', models.CharField(choices=[('Элеватор', 'Элеватор'), ('Мельница', 'Мельница'), ('Крупозавод', 'Крупозавод'), ('Фасовка', 'Фасовка')], max_length=30, verbose_name='Источник выбросов')),
                ('emission_source_number', models.CharField(max_length=10, verbose_name='№ источника выброса')),
                ('au_ptu_number', models.CharField(max_length=10, verbose_name='№ АУ или ПТУ')),
                ('harmful_substance_name', models.CharField(choices=[('Пыль зерновая', 'Пыль зерновая'), ('Твердые суммарно', 'Твердые суммарно')], default='Пыль зерновая', max_length=100, verbose_name='Вредное вещество')),
                ('year', models.IntegerField(default='2022', verbose_name='Год')),
                ('quarter', models.IntegerField(default=1, verbose_name='Квартал')),
                ('first_month', models.IntegerField(default=0, verbose_name='Первый месяц в квартале')),
                ('second_month', models.IntegerField(default=0, verbose_name='Второй месяц в квартале')),
                ('third_month', models.IntegerField(default=0, verbose_name='Третий месяц в квартале')),
                ('all', models.IntegerField(default=0, verbose_name='Всего')),
                ('M', models.DecimalField(decimal_places=3, default=0, max_digits=6, verbose_name='М, г/с')),
                ('G', models.DecimalField(decimal_places=5, default=0, max_digits=8, verbose_name='G, т/год')),
            ],
        ),
        migrations.CreateModel(
            name='UnOrganizeWaste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obj_type', models.CharField(choices=[('Мельзавод', 'Мельзавод'), ('Крупозавод', 'Крупозавод'), ('РБ', 'РБ')], max_length=30, verbose_name='Объект')),
                ('e_s_number', models.CharField(max_length=10, verbose_name='№ источника выброса')),
                ('e_s_name', models.CharField(max_length=255, verbose_name='Наименование источника выброса')),
                ('harmful_substance_name', models.CharField(choices=[('Пыль зерновая м/з', 'Пыль зерновая м/з'), ('Пыль мучная', 'Пыль мучная'), ('Пыль зерновая к/з', 'Пыль зерновая к/з'), ('Пыль зерновая р/б', 'Пыль зерновая р/б')], max_length=100, verbose_name='Вредное вещество')),
                ('M', models.DecimalField(decimal_places=3, default=0, max_digits=6, verbose_name='Максимальное выделение веществ [М, г/с]')),
                ('T', models.IntegerField(default=0, verbose_name='Время операции [T, с]')),
                ('year', models.IntegerField(default='2022', verbose_name='Год')),
                ('quarter', models.IntegerField(default=1, verbose_name='Квартал')),
                ('first_month', models.DecimalField(decimal_places=3, default=0, max_digits=6, verbose_name='Первый месяц в квартале')),
                ('second_month', models.DecimalField(decimal_places=3, default=0, max_digits=6, verbose_name='Второй месяц в квартале')),
                ('third_month', models.DecimalField(decimal_places=3, default=0, max_digits=6, verbose_name='Третий месяц в квартале')),
                ('all', models.DecimalField(decimal_places=3, default=0, max_digits=6, verbose_name='Всего')),
                ('Tw', models.DecimalField(decimal_places=3, default=0, max_digits=6, verbose_name='Кол-во часов работы [T, час/год]')),
                ('G', models.DecimalField(decimal_places=4, default=0, max_digits=6, verbose_name='Валовый выброс [T, т/год]')),
                ('loaded', models.IntegerField(default=0, verbose_name='Загружено')),
                ('weight', models.IntegerField(default=0, verbose_name='Вес одной ед. [кг]')),
            ],
        ),
        migrations.CreateModel(
            name='WeldingWaste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default='2022', verbose_name='Год')),
                ('quarter', models.IntegerField(default=1, verbose_name='Квартал')),
                ('mark', models.CharField(max_length=100, verbose_name='Марка электр.')),
                ('emission', models.DecimalField(decimal_places=3, max_digits=6, verbose_name='Удельн. выдел.')),
                ('iron_ox_kg', models.IntegerField(verbose_name='Оксид железа [кг]')),
                ('iron_ox_ton', models.DecimalField(decimal_places=5, default=0, max_digits=6, verbose_name='Оксид железа [т/год]')),
                ('mg_gg', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Марганец [г/г]')),
                ('mg_ton', models.DecimalField(decimal_places=6, default=0, max_digits=7, verbose_name='Марганец [т/год]')),
                ('hyd_flu_gkg', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Фтористый водород [г/кг]')),
                ('hyd_flu_ton', models.DecimalField(decimal_places=7, default=0, max_digits=8, verbose_name='Фтористый водород [т/год]')),
            ],
        ),
        migrations.CreateModel(
            name='BoilerNitrogenWaste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarter', models.IntegerField(default=1, verbose_name='Квартал')),
                ('month', models.CharField(choices=[('Январь', 'Январь'), ('Февраль', 'Февраль'), ('Март', 'Март'), ('Апрель', 'Апрель'), ('Май', 'Май'), ('Июнь', 'Июнь'), ('Июль', 'Июль'), ('Август', 'Август'), ('Сентябрь', 'Сентябрь'), ('Октябрь', 'Октябрь'), ('Ноябрь', 'Ноябрь'), ('Декабрь', 'Декабрь')], max_length=10, verbose_name='Месяц')),
                ('year', models.IntegerField(default='2022', verbose_name='Год')),
                ('B', models.DecimalField(decimal_places=4, default=0, max_digits=7, verbose_name='В, тыс. м3')),
                ('Qh', models.IntegerField(default=0, verbose_name='Qн, ккал/м3')),
                ('T', models.IntegerField(default=0, verbose_name='T, час')),
                ('Q', models.DecimalField(decimal_places=9, default=0, max_digits=12, verbose_name='Q')),
                ('Bs', models.DecimalField(decimal_places=9, default=0, max_digits=11, verbose_name='Вs, м3/с')),
                ('Knox', models.DecimalField(decimal_places=9, default=0, max_digits=11, verbose_name='Кnoх, г/МДж')),
                ('Mnox', models.DecimalField(decimal_places=9, default=0, max_digits=11, verbose_name='Мnox, т/год')),
                ('Mno2', models.DecimalField(decimal_places=9, default=0, max_digits=11, verbose_name='М(NO2)')),
                ('Mno', models.DecimalField(decimal_places=4, default=0, max_digits=11, verbose_name='М(NO)')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waste.boilerwaste', verbose_name='Объект')),
            ],
        ),
        migrations.CreateModel(
            name='BoilerCarbonOxWaste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarter', models.IntegerField(default=1, verbose_name='Квартал')),
                ('month', models.CharField(choices=[('Январь', 'Январь'), ('Февраль', 'Февраль'), ('Март', 'Март'), ('Апрель', 'Апрель'), ('Май', 'Май'), ('Июнь', 'Июнь'), ('Июль', 'Июль'), ('Август', 'Август'), ('Сентябрь', 'Сентябрь'), ('Октябрь', 'Октябрь'), ('Ноябрь', 'Ноябрь'), ('Декабрь', 'Декабрь')], max_length=10, verbose_name='Месяц')),
                ('year', models.IntegerField(default='2022', verbose_name='Год')),
                ('B', models.DecimalField(decimal_places=4, default=0, max_digits=6, verbose_name='В, тыс. м3')),
                ('Qh', models.IntegerField(default=0, verbose_name='Qн, ккал/м3')),
                ('Qh_calc', models.DecimalField(decimal_places=4, default=0, max_digits=6, verbose_name='Qн, МДж/м3')),
                ('Cco', models.DecimalField(decimal_places=4, default=0, max_digits=5, verbose_name='Ссо, г/м3')),
                ('Mco', models.DecimalField(decimal_places=4, default=0, max_digits=5, verbose_name='М(CO), т/мес')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waste.boilerwaste', verbose_name='Объект')),
            ],
        ),
    ]
