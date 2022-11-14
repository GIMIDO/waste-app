from .models import *
import decimal


def get_columns(quarter, toc):

    months = get_months(str(quarter))

    match toc:
        case 'ow':
            return ['№ ист.', '№ АУ или ПТУ', 'Вредное вещество', months['1'], months['2'], months['3'], 'Всего', 'М, г/с', 'G, т/год']


def organize_waste_calc_all(data):

    for elem in data:
        elem.all = elem.first_month + elem.second_month + elem.third_month
        elem.G = round(elem.all * elem.M * decimal.Decimal(3600) * decimal.Decimal(0.000001), 5)
        elem.save()
    
    
def organize_waste_calc_all_G(data):

    all_G = 0

    for elem in data:
        all_G += elem.G
    
    return all_G


def get_months(quarter):
    
    if (quarter == '1'):
        return {
            '1': 'Январь',
            '2': 'Февраль',
            '3': 'Март'
        }
    elif (quarter == '2'):
        return {
            '1': 'Апрель',
            '2': 'Май',
            '3': 'Июнь'
        }
    elif (quarter == '3'):
        return {
            '1': 'Июль',
            '2': 'Август',
            '3': 'Сентябрь'
        }
    elif (quarter == '4'):
        return {
            '1': 'Октябрь',
            '2': 'Ноябрь',
            '3': 'Декабрь'
        }
    else:
        return {
            '1': 'Месяц 1',
            '2': 'Месяц 2',
            '3': 'Месяц 3'
        }


def get_next_link(request):

    if request.GET.get('next'):
        return request.GET.get('next')
    else:
        return '/'