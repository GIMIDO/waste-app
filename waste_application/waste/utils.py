import json
from .models import *
import decimal
import math


def get_months(quarter):
    
    if (quarter == '1'):
        return {'1': 'Январь','2': 'Февраль','3': 'Март'}
    elif (quarter == '2'):
        return {'1': 'Апрель','2': 'Май','3': 'Июнь'}
    elif (quarter == '3'):
        return {'1': 'Июль','2': 'Август','3': 'Сентябрь'}
    elif (quarter == '4'):
        return {'1': 'Октябрь','2': 'Ноябрь','3': 'Декабрь'}
    else:
        return {'1': 'Месяц 1','2': 'Месяц 2','3': 'Месяц 3'}

def get_boiler_months(quarter):
    
    if (quarter == '1'):
        return ['Январь', 'Февраль', 'Март']
    elif (quarter == '2'):
        return ['Апрель', 'Май', 'Июнь']
    elif (quarter == '3'):
        return ['Июль', 'Август', 'Сентябрь']
    elif (quarter == '4'):
        return ['Октябрь', 'Ноябрь', 'Декабрь']
    else:
        return ['М1','М2','М3']


# --- #

def organize_waste_calc_all(data):

    for elem in data:
        elem.all = elem.first_month + elem.second_month + elem.third_month
        elem.G = round(elem.all * elem.M * decimal.Decimal(3600) * decimal.Decimal(0.000001), 9)

        elem.save()
    
def organize_waste_calc_all_G(data):

    all_G = 0

    for elem in data:
        all_G += elem.G

        elem.G = round(elem.G, 4)
    
    return all_G

# --- #

def welding_waste_calc(data):

    for elem in data:
        elem.iron_ox_ton = round(elem.emission * elem.iron_ox_kg * decimal.Decimal(0.000001), 9)
        elem.mg_ton = round(elem.iron_ox_kg * elem.mg_gg * decimal.Decimal(0.000001), 9)
        elem.hyd_flu_ton = round(elem.iron_ox_kg * elem.hyd_flu_gkg * decimal.Decimal(0.000001), 9)

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

            elem.iron_ox_ton = round(elem.iron_ox_ton, 4)
            elem.mg_ton = round(elem.mg_ton, 4)
            elem.hyd_flu_ton = round(elem.hyd_flu_ton, 4)

        json_i = {
                    "s_i_kg": str(round(sum_iron_ox_kg, 4)),
                    "s_i_t": str(round(sum_iron_ox_ton, 4)),
                    "s_m_g": str(round(sum_mg_gg, 4)),
                    "s_m_t": str(round(sum_mg_ton, 4)),
                    "s_hf_g": str(round(sum_hyd_flu_gkg, 4)),
                    "s_hf_t": str(round(sum_hyd_flu_ton, 4))
                }

        sum_calc[str(q)] = json_i
        q += 1
        sum_iron_ox_kg, sum_iron_ox_ton, sum_mg_gg, sum_mg_ton, sum_hyd_flu_gkg, sum_hyd_flu_ton = 0,0,0,0,0,0

    json_y = {
            "y_i_kg": str(round(year_i_kg, 4)),
            "y_i_t": str(round(year_i_t, 4)),
            "y_m_g": str(round(year_m_g, 4)),
            "y_m_t": str(round(year_m_t, 4)),
            "y_hf_g": str(round(year_hf_g, 4)),
            "y_hf_t": str(round(year_hf_t, 4))
        }
    sum_calc["year"] = json_y

    return sum_calc

# --- #

def unorganize_waste_calculate(data):

    for elem in data:
        elem.all = elem.first_month + elem.second_month + elem.third_month
        elem.Tw = round(elem.T * elem.all / decimal.Decimal(3600), 9)
        elem.G = round(elem.Tw * elem.M * decimal.Decimal(3600) * decimal.Decimal(0.000001), 9)

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

                elem.Tw = round(elem.Tw, 4)
                elem.G = round(elem.G, 4)
            
            return [p_1, p_2]

        case "Крупозавод":
            h_s = ['Пыль зерновая к/з']
            p_1 = 0

            for elem in data:
                p_1 += elem.G
            
                elem.Tw = round(elem.Tw, 4)
                elem.G = round(elem.G, 4)

            return [p_1]

        case "РБ":
            h_s = ['Пыль зерновая р/б']
            p_1 = 0

            for elem in data:
                p_1 += elem.G
            
                elem.Tw = round(elem.Tw, 4)
                elem.G = round(elem.G, 4)

            return [p_1]
    
def get_hs(obj_type):

    match obj_type:
        case "Мельзавод":
            return ['Пыль зерновая м/з', 'Пыль мучная']

        case "Крупозавод":
            return ['Пыль зерновая к/з']

        case "РБ":
            return ['Пыль зерновая р/б']


# --- #


def boiler_carbon_waste_calc(data):

    for elem in data:
        elem.Qh_calc = round(elem.Qh * elem.name.K * decimal.Decimal(0.001), 9)
        elem.Cco = round(elem.Qh_calc * elem.name.q3 * elem.name.R, 9)
        elem.Mco = round(elem.B * elem.Cco * decimal.Decimal(0.001), 9)

        elem.save()

def boiler_nitrogen_waste_calc(data):

    for elem in data:
        elem.Q = round(elem.Qh * elem.name.K * decimal.Decimal(0.001), 9)
        elem.Bs = round(elem.B / (decimal.Decimal(3.6) * elem.T), 9)
        elem.Knox = round((decimal.Decimal(0.01) * decimal.Decimal(math.sqrt(decimal.Decimal(1.59) * elem.Q * elem.Bs))) + decimal.Decimal(0.03), 9)
        elem.Mnox = round(decimal.Decimal(0.001) * elem.B * elem.Q * elem.Knox * elem.name.Bk * elem.name.Bt, 9)
        elem.Mno2 = round(decimal.Decimal(0.8) * elem.Mnox, 9)
        elem.Mno = round(decimal.Decimal(0.13) * elem.Mnox, 9)

        elem.save()

def boiler_carbon_waste_month(data, months):

    B1, B2, B3 = 0, 0, 0
    Mco1, Mco2, Mco3 = 0, 0, 0

    for elem in data:
        if elem.month == months[0]:
            B1 += elem.B
            Mco1 += elem.Mco

        elif elem.month == months[1]:
            B2 += elem.B
            Mco2 += elem.Mco

        elif elem.month == months[2]:
            B3 += elem.B
            Mco3 += elem.Mco

        
        elem.Qh_calc = round(elem.Qh_calc, 4)
        elem.Cco = round(elem.Cco, 4)
        elem.Mco = round(elem.Mco, 4)

    return [[months[0], B1, round(Mco1, 4)], [months[1], B2, round(Mco2, 4)], [months[2], B3, round(Mco3, 4)]]

def boiler_nitrogen_waste_month(data, months):

    B1, B2, B3 = 0, 0, 0
    Mno1, Mno2, Mno3 = 0, 0, 0
    Mno2_1, Mno2_2, Mno2_3 = 0, 0, 0

    for elem in data:
        if elem.month == months[0]:
            B1 += elem.B
            Mno1 += elem.Mno
            Mno2_1 += elem.Mno2

        elif elem.month == months[1]:
            B2 += elem.B
            Mno2 += elem.Mno
            Mno2_2 += elem.Mno2

        elif elem.month == months[2]:
            B3 += elem.B
            Mno3 += elem.Mno
            Mno2_3 += elem.Mno2

        
        elem.Q = round(elem.Q, 4)
        elem.Bs = round(elem.Bs, 4)
        elem.Knox = round(elem.Knox, 4)
        elem.Mnox = round(elem.Mnox, 4)
        elem.Mno2 = round(elem.Mno2, 4)
        elem.Mno = round(elem.Mno, 4)

    return [[months[0], B1, round(Mno1), round(Mno2_1)], [months[1], B2, round(Mno2), round(Mno2_2)], [months[2], B3, round(Mno3), round(Mno2_3)]]