from django.db import models

# Create your models here.
class OrganizeWaste(models.Model):

    TYPE_CHOICES = (
        ('Элеватор', 'Элеватор'),
        ('Мельница', 'Мельница'),
        ('Крупозавод', 'Крупозавод'),
        ('Фасовка', 'Фасовка')
    )

    emission_source = models.CharField(verbose_name="Источник выбросов", choices=TYPE_CHOICES, max_length=30)
    emission_source_number = models.CharField(verbose_name="№ источника выброса", max_length=10)
    au_ptu_number = models.CharField(verbose_name="№ АУ или ПТУ", max_length=10)
    harmful_substance_name = models.CharField(verbose_name="Вредное вещество", max_length=100, default="Пыль зерновая")

    year = models.IntegerField(verbose_name="Год", default="2022")
    quarter = models.IntegerField(verbose_name="Квартал", default=1)

    first_month = models.IntegerField(verbose_name="Первый месяц в квартале", default=0)
    second_month = models.IntegerField(verbose_name="Второй месяц в квартале", default=0)
    third_month = models.IntegerField(verbose_name="Третий месяц в квартале", default=0)
    all = models.IntegerField(verbose_name="Всего", default=0)

    M = models.DecimalField(verbose_name="М, г/с", max_digits=6, decimal_places=3, default=0)
    G = models.DecimalField(verbose_name="G, т/год", max_digits=8, decimal_places=5, default=0)

    def __str__(self) -> str:
        return f'{self.emission_source} {self.emission_source_number} {self.au_ptu_number} [{self.year} {self.quarter}]'


class WeldingWaste(models.Model):

    year = models.IntegerField(verbose_name="Год", default="2022")
    quarter = models.IntegerField(verbose_name="Квартал", default=1)

    mark = models.CharField(verbose_name='Марка электр.', max_length=100)
    emission = models.DecimalField(verbose_name='Удельн. выдел.', max_digits=6, decimal_places=3)
    
    iron_ox_kg = models.IntegerField(verbose_name='Оксид железа [кг]')
    iron_ox_ton = models.DecimalField(verbose_name='Оксид железа [т/год]', max_digits=6, decimal_places=5, default=0)

    mg_gg = models.DecimalField(verbose_name='Марганец [г/г]', max_digits=4, decimal_places=3)
    mg_ton = models.DecimalField(verbose_name='Марганец [т/год]', max_digits=7, decimal_places=6, default=0)

    hyd_flu_gkg = models.DecimalField(verbose_name='Фтористый водород [г/кг]', max_digits=4, decimal_places=3)
    hyd_flu_ton = models.DecimalField(verbose_name='Фтористый водород [т/год]', max_digits=8, decimal_places=7, default=0)

    def __str__(self) -> str:
        return f'{self.mark} {self.emission} [{self.year} {self.quarter}]'
