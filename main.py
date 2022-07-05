# -*- coding: utf-8 -*-

import df
import logger
from base import Base
from datetime import datetime
from sys import argv


def get_date_indexes(arg: list):
    '''
    Определение даты и цифровых индексов валют из входящих данных
    '''
    date_indexes = ''.join(arg[1:])
    date_indexes = date_indexes.split(',')
    date = date_indexes[0]
    date = datetime.strptime(date, "%d.%m.%Y")
    date = date.date()
    indexes = date_indexes[1:]

    return date, indexes



def filter_data(indexes: list[str], data: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    '''
    Выборка необходимых индексов валют из полученных от ресурса данных
    '''
    f_data = [data[i] for i in indexes]
    return f_data
   


if __name__ == '__main__':
        
    url = 'https://www.cbr.ru/dailyinfowebserv/dailyinfo.asmx?wsdl'  # адрес ресурса с данными

    name_log = argv[0]  # полное имя модуля
    name_log = name_log.split('.')[0] # частичное имя модуля
    log = logger.set_logger(name_log) # объявление логера
    
    bd = Base(log)

    date, indexes = get_date_indexes(argv)
    currency_order, id, indexes = bd.chek_data(date, indexes)
    if id is not None:
        data = df.data(date, url)
        f_data = filter_data(indexes, data)
        bd.set_data(id, date, f_data, currency_order)

       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       