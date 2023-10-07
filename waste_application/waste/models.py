from django.db import models
from django.contrib.auth import get_user_model

# модель пользвоателя (встроенная)
User = get_user_model()


# Организованные
class OrganizeWaste(models.Model):

    TYPE_CHOICES = (
        ('Элеватор', 'Элеватор'),
        ('Мельница', 'Мельница'),
        ('Крупозавод', 'Крупозавод'),
        ('Фасовка', 'Фасовка')
    )

    SUBSTANCE_CHOICES = (
        ('Пыль зерновая', 'Пыль зерновая'),
        ('Твердые суммарно', 'Твердые суммарно')
    )

    OPERATING_CHOICES = {
        ('Постоянно','Постоянно'),
        ('Периодически','Периодически')
    }

    emission_source = models.CharField(verbose_name="Источник выбросов", choices=TYPE_CHOICES, max_length=30)
    emission_source_number = models.CharField(verbose_name="№ источника выброса", max_length=10)
    au_ptu_number = models.CharField(verbose_name="№ АУ или ПТУ", max_length=10)
    harmful_substance_name = models.CharField(verbose_name="Вредное вещество", choices=SUBSTANCE_CHOICES, max_length=100, default="Пыль зерновая")

    operating_mode = models.CharField(verbose_name="Режим работы технологического оборудования", choices=OPERATING_CHOICES, max_length=12, default="Периодически")
    code_ZV = models.CharField(verbose_name="Код ЗВ", max_length=5, default='2937')

    year = models.IntegerField(verbose_name="Год", default="2022")
    quarter = models.IntegerField(verbose_name="Квартал", default=1)

    first_month = models.IntegerField(verbose_name="Первый месяц в квартале", default=0)
    second_month = models.IntegerField(verbose_name="Второй месяц в квартале", default=0)
    third_month = models.IntegerField(verbose_name="Третий месяц в квартале", default=0)
    all = models.IntegerField(verbose_name="Всего", default=0)

    M = models.DecimalField(verbose_name="М, г/с", max_digits=6, decimal_places=3, default=0)
    G = models.DecimalField(verbose_name="G, т/год", max_digits=8, decimal_places=5, default=0)

    def __str__(self) -> str:
        return f'{self.emission_source} {self.emission_source_number} {self.au_ptu_number} {self.harmful_substance_name} [{self.year} {self.quarter}]'

    class Meta:
        verbose_name = 'Организованные'
        verbose_name_plural = 'Организованные'

# Сварка
class WeldingWaste(models.Model):

    year = models.IntegerField(verbose_name="Год", default="2022")
    quarter = models.IntegerField(verbose_name="Квартал", default=1)

    mark = models.CharField(verbose_name='Марка электр.', max_length=100)
    emission = models.DecimalField(verbose_name='Удельн. выдел.', max_digits=6, decimal_places=3)
    
    iron_ox_kg = models.DecimalField(verbose_name='Оксид железа [кг]', max_digits=8, decimal_places=5, default=0)
    iron_ox_ton = models.DecimalField(verbose_name='Оксид железа [т/год]', max_digits=8, decimal_places=5, default=0)

    mg_gg = models.DecimalField(verbose_name='Марганец [г/г]', max_digits=5, decimal_places=4)
    mg_ton = models.DecimalField(verbose_name='Марганец [т/год]', max_digits=7, decimal_places=6, default=0)

    hyd_flu_gkg = models.DecimalField(verbose_name='Фтористый водород [г/кг]', max_digits=5, decimal_places=4)
    hyd_flu_ton = models.DecimalField(verbose_name='Фтористый водород [т/год]', max_digits=8, decimal_places=7, default=0)

    def __str__(self) -> str:
        return f'{self.mark} {self.emission} [{self.year} {self.quarter}]'

    class Meta:
        verbose_name = 'Сварка'
        verbose_name_plural = 'Сварка'

# Неорганизованные
class UnOrganizeWaste(models.Model):

    OBJ_TYPE = (
        ('Мельзавод', 'Мельзавод'),
        ('Крупозавод', 'Крупозавод'),
        ('РБ', 'РБ'),
        ('Фосфин','Фосфин'),
    )

    H_S_NAME = (
        ('Пыль зерновая м/з', 'Пыль зерновая м/з'),
        ('Пыль мучная', 'Пыль мучная'),
        ('Пыль зерновая к/з', 'Пыль зерновая к/з'),
        ('Пыль зерновая р/б', 'Пыль зерновая р/б'),
        ('фосфин (водород фосфористый)', 'фосфин (водород фосфористый)'),
    )

    obj_type = models.CharField(verbose_name="Объект", choices=OBJ_TYPE, max_length=30)
    e_s_number = models.CharField(verbose_name="№ источника выброса", max_length=10)
    e_s_name = models.CharField(verbose_name="Наименование источника выброса", max_length=255)
    code_ZV = models.CharField(verbose_name="Код ЗВ", max_length=5, default='2937')

    harmful_substance_name = models.CharField(verbose_name="Вредное вещество", choices=H_S_NAME, max_length=100)

    M = models.DecimalField(verbose_name="Максимальное выделение веществ [М, г/с]", max_digits=6, decimal_places=3, default=0)
    T = models.IntegerField(verbose_name="Время операции [T, с]", default=0)

    year = models.IntegerField(verbose_name="Год", default="2022")
    quarter = models.IntegerField(verbose_name="Квартал", default=1)

    first_month = models.DecimalField(verbose_name="Первый месяц в квартале", max_digits=6, decimal_places=3, default=0)
    second_month = models.DecimalField(verbose_name="Второй месяц в квартале", max_digits=6, decimal_places=3, default=0)
    third_month = models.DecimalField(verbose_name="Третий месяц в квартале", max_digits=6, decimal_places=3, default=0)
    all = models.DecimalField(verbose_name="Всего", max_digits=6, decimal_places=3, default=0)

    Tw = models.DecimalField(verbose_name="Кол-во часов работы [T, час/год]", max_digits=6, decimal_places=3, default=0)
    G = models.DecimalField(verbose_name="Валовый выброс [T, т/год]", max_digits=6, decimal_places=4, default=0)

    loaded = models.IntegerField(verbose_name="Загружено", default=0)
    weight = models.IntegerField(verbose_name="Вес одной ед. [кг]", default=0)

    def __str__(self) -> str:
        return f'[{self.obj_type} {self.e_s_number}] {self.year} {self.quarter} {self.harmful_substance_name}'

    class Meta:
        verbose_name = 'Неорганизованные'
        verbose_name_plural = 'Неорганизованные'

# Котельные (типы)
class BoilerWaste(models.Model):

    FUEL = (
        ("Газ природ.","Газ природ."),
        ("Дизтопливо","Дизтопливо")
    )
    name = models.CharField(verbose_name="Название", max_length=100)
    short_name = models.CharField(verbose_name="Короткое название (для автозаполнения) [5 символов]", max_length=5, null=True)
    number = models.CharField(verbose_name="Номер источника", max_length=6, default=4)
    fuel = models.CharField(verbose_name="Наименование топлива, сырья, материалов", choices=FUEL, max_length=20, default="Газ природ.")

    K = models.DecimalField(verbose_name="К", max_digits=6, decimal_places=4, default=4.1868)

    q3 = models.DecimalField(verbose_name="q3, %", max_digits=3, decimal_places=2, default=0)
    R = models.DecimalField(verbose_name="R", max_digits=3, decimal_places=2, default=0)

    Bk = models.DecimalField(verbose_name="Bk", max_digits=3, decimal_places=2, default=0)
    Bt = models.DecimalField(verbose_name="Bt", max_digits=4, decimal_places=3, default=0)

    def __str__(self) -> str:
        return f'{self.name} K={self.K}'

    class Meta:
        verbose_name = 'Котельные (типы)'
        verbose_name_plural = 'Котельные (типы)'

# Котельные (углерод оксид)
class BoilerCarbonOxWaste(models.Model):

    MONTHS = (
        ("Январь", "Январь"),
        ("Февраль", "Февраль"),
        ("Март", "Март"),
        ("Апрель", "Апрель"),
        ("Май", "Май"),
        ("Июнь", "Июнь"),
        ("Июль", "Июль"),
        ("Август", "Август"),
        ("Сентябрь", "Сентябрь"),
        ("Октябрь", "Октябрь"),
        ("Ноябрь", "Ноябрь"),
        ("Декабрь", "Декабрь"),
    )

    name = models.ForeignKey(BoilerWaste, on_delete=models.CASCADE, verbose_name='Объект')
    quarter = models.IntegerField(verbose_name="Квартал", default=1)

    month = models.CharField(verbose_name="Месяц", choices=MONTHS, max_length=10)
    year = models.IntegerField(verbose_name="Год", default="2022")

    B = models.DecimalField(verbose_name="В, тыс. м3", max_digits=10, decimal_places=4, default=0)
    Qh = models.IntegerField(verbose_name="Qн, ккал/м3", default=0)

    # рассчитывается
    Qh_calc = models.DecimalField(verbose_name="Qн, МДж/м3", max_digits=10, decimal_places=4, default=0)
    Cco = models.DecimalField(verbose_name="Ссо, г/м3", max_digits=10, decimal_places=4, default=0)
    Mco = models.DecimalField(verbose_name="М(CO), т/мес", max_digits=10, decimal_places=4, default=0)


    def __str__(self) -> str:
        return f'{self.name.name} [{self.year}/{self.month}/{self.quarter}]'

    class Meta:
        verbose_name = 'Котельные (углерод оксид)'
        verbose_name_plural = 'Котельные (углерод оксид)'

# Котельные (азот диоксид и азот оксид)
class BoilerNitrogenWaste(models.Model):

    MONTHS = (
        ("Январь", "Январь"),
        ("Февраль", "Февраль"),
        ("Март", "Март"),
        ("Апрель", "Апрель"),
        ("Май", "Май"),
        ("Июнь", "Июнь"),
        ("Июль", "Июль"),
        ("Август", "Август"),
        ("Сентябрь", "Сентябрь"),
        ("Октябрь", "Октябрь"),
        ("Ноябрь", "Ноябрь"),
        ("Декабрь", "Декабрь"),
    )

    name = models.ForeignKey(BoilerWaste, on_delete=models.CASCADE, verbose_name='Объект')
    quarter = models.IntegerField(verbose_name="Квартал", default=1)

    month = models.CharField(verbose_name="Месяц", choices=MONTHS, max_length=10)
    year = models.IntegerField(verbose_name="Год", default="2022")

    B = models.DecimalField(verbose_name="В, тыс. м3", max_digits=8, decimal_places=4, default=0)
    Qh = models.IntegerField(verbose_name="Qн, ккал/м3", default=0)
    T = models.IntegerField(verbose_name="T, час", default=0)

    # рассчитывается
    Q = models.DecimalField(verbose_name="Q", max_digits=12, decimal_places=9, default=0)
    Bs = models.DecimalField(verbose_name="Вs, м3/с", max_digits=12, decimal_places=9, default=0)
    Knox = models.DecimalField(verbose_name="Кnoх, г/МДж", max_digits=12, decimal_places=9, default=0)
    Mnox = models.DecimalField(verbose_name="Мnox, т/год", max_digits=12, decimal_places=9, default=0)

    Mno2 = models.DecimalField(verbose_name="М(NO2)", max_digits=12, decimal_places=9, default=0)
    Mno = models.DecimalField(verbose_name="М(NO)", max_digits=12, decimal_places=4, default=0)
    
    def __str__(self) -> str:
        return f'{self.name.name} [{self.year}/{self.month}]'

    class Meta:
        verbose_name = 'Котельные (азот диоксид и азот оксид)'
        verbose_name_plural = 'Котельные (азот диоксид и азот оксид)'

# Котельные (дизельное топливо и сажа)
class BoilerSulfCarbWaste(models.Model):

    MONTHS = (
        ("Январь", "Январь"),
        ("Февраль", "Февраль"),
        ("Март", "Март"),
        ("Апрель", "Апрель"),
        ("Май", "Май"),
        ("Июнь", "Июнь"),
        ("Июль", "Июль"),
        ("Август", "Август"),
        ("Сентябрь", "Сентябрь"),
        ("Октябрь", "Октябрь"),
        ("Ноябрь", "Ноябрь"),
        ("Декабрь", "Декабрь"),
    )

    name = models.ForeignKey(BoilerWaste, on_delete=models.CASCADE, verbose_name='Объект')
    
    quarter = models.IntegerField(verbose_name="Квартал", default=1)
    month = models.CharField(verbose_name="Месяц", choices=MONTHS, max_length=10)
    year = models.IntegerField(verbose_name="Год", default="2022")
    B = models.DecimalField(verbose_name="В, тыс. м3", max_digits=9, decimal_places=5, default=0)

    Mso2 = models.DecimalField(verbose_name='Mso2, т/год', max_digits=7, decimal_places=4, default=0)
    Mc = models.DecimalField(verbose_name='M c, т/год', max_digits=7, decimal_places=4, default=0) 

    def __str__(self) -> str:
        return f'дизельное топливо / сажа | {self.Mso2} {self.year}'

    class Meta:
        verbose_name = 'Котельные (дизельное топливо и сажа)'
        verbose_name_plural = 'Котельные (дизельное топливо и сажа)'

# Данные для Деклараций
class DeclarationWaste(models.Model):

    quarter = models.IntegerField(verbose_name="Квартал")
    year = models.IntegerField(verbose_name="Год")

    two = models.DecimalField(verbose_name='2 класс опасности', max_digits=10, decimal_places=4, default=0)
    three_1 = models.DecimalField(verbose_name='3 класс опасности', max_digits=10, decimal_places=4, default=0)
    three_2 = models.DecimalField(verbose_name='3 класс опасности (организованные)', max_digits=10, decimal_places=4, default=0)
    four = models.DecimalField(verbose_name='4 класс опасности', max_digits=10, decimal_places=4, default=0)

    def __str__(self) -> str:
        return f'{self.year} [{self.quarter}]'

    class Meta:
        verbose_name = 'Данные для Деклараций'
        verbose_name_plural = 'Данные для Деклараций'

class DeclarationCalc(models.Model):

    sum = models.DecimalField(verbose_name='Сумма', max_digits=7, decimal_places=2, default=0)

    quarter = models.IntegerField(verbose_name="Квартал")
    year = models.IntegerField(verbose_name="Год")

    def __str__(self) -> str:
        return f'{self.year} [{self.quarter} {self.sum}]'