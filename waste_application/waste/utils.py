import json
from .models import *
import decimal


# class DictObj(object):
#     def __init__(self, in_dict:dict):
#         assert isinstance(in_dict, dict)
#         for key, val in in_dict.items():
#             if isinstance(val, (list, tuple)):
#                setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
#             else:
#                setattr(self, key, DictObj(val) if isinstance(val, dict) else val)


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

# --- #

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

# --- #

def welding_waste_calc(data):

    for elem in data:
        elem.iron_ox_ton = round(elem.emission * elem.iron_ox_kg * decimal.Decimal(0.000001), 5)
        elem.mg_ton = round(elem.iron_ox_kg * elem.mg_gg * decimal.Decimal(0.000001), 6)
        elem.hyd_flu_ton = round(elem.iron_ox_kg * elem.hyd_flu_gkg * decimal.Decimal(0.000001), 7)
        elem.save()

def get_quarters(data):

    q = 0
    quarters = []
    for elem in data:
        if (elem.quarter > q):
            quarters.append(elem.quarter)
            q = elem.quarter

    return quarters

def welding_waste_sum_calc(data):

    if (data.exists()):
        pass
    else:
        return None

    q = 1

    sum_calc = {}

    sum_iron_ox_kg, sum_iron_ox_ton, sum_mg_gg, sum_mg_ton, sum_hyd_flu_gkg, sum_hyd_flu_ton = 0,0,0,0,0,0

    year_i_kg, year_i_t, year_m_g, year_m_t, year_hf_g, year_hf_t = 0,0,0,0,0,0

    while (q <= 4):

        for elem in data:

            if (q == elem.quarter):
                sum_iron_ox_kg += elem.iron_ox_kg
                sum_iron_ox_ton += elem.iron_ox_ton
                sum_mg_gg += elem.mg_gg
                sum_mg_ton += elem.mg_ton
                sum_hyd_flu_gkg += elem.hyd_flu_gkg
                sum_hyd_flu_ton += elem.hyd_flu_ton

                year_i_kg += elem.iron_ox_kg
                year_i_t += elem.iron_ox_ton
                year_m_g += elem.mg_gg
                year_m_t += elem.mg_ton
                year_hf_g += elem.hyd_flu_gkg
                year_hf_t += elem.hyd_flu_ton

        json_i = {
                    "s_i_kg": str(sum_iron_ox_kg),
                    "s_i_t": str(sum_iron_ox_ton),
                    "s_m_g": str(sum_mg_gg),
                    "s_m_t": str(sum_mg_ton),
                    "s_hf_g": str(sum_hyd_flu_gkg),
                    "s_hf_t": str(sum_hyd_flu_ton)
                }

        sum_calc[str(q)] = json_i
        q += 1
        sum_iron_ox_kg, sum_iron_ox_ton, sum_mg_gg, sum_mg_ton, sum_hyd_flu_gkg, sum_hyd_flu_ton = 0,0,0,0,0,0

    json_y = {
            "y_i_kg": str(year_i_kg),
            "y_i_t": str(year_i_t),
            "y_m_g": str(year_m_g),
            "y_m_t": str(year_m_t),
            "y_hf_g": str(year_hf_g),
            "y_hf_t": str(year_hf_t)
        }
    sum_calc["year"] = json_y

    return sum_calc

# --- #

def unorganize_waste_calculate(data):

    for elem in data:
        elem.all = elem.first_month + elem.second_month + elem.third_month
        elem.Tw = round(elem.T * elem.all / decimal.Decimal(3600), 3)
        elem.G = round(elem.Tw * elem.M * decimal.Decimal(3600) * decimal.Decimal(0.000001), 4)

        elem.save()

def unorganize_calc_data(data, obj_type):
    match obj_type:
        case "Мельзавод":
            h_s = ['Пыль зерновая м/з', 'Пыль мучная']
            p_1, p_2 = 0, 0

            for elem in data:
                if elem.harmful_substance_name == h_s[0]:
                    p_1 += elem.G
                else:
                    p_2 += elem.G
            
            return [p_1, p_2]

        case "Крупозавод":
            pass
        case "Р/Б":
            pass
    
def get_hs(obj_type):

    match obj_type:
        case "Мельзавод":
            return ['Пыль зерновая м/з', 'Пыль мучная']

        case "Крупозавод":
            pass
        case "Р/Б":
            pass