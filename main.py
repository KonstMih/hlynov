# -*- coding: utf-8 -*-

import df
import logger
import base
from datetime import datetime
from sys import argv

url = 'http://www.cbr.ru/dailyinfowebserv/dailyinfo.asmx?wsdl'  # адрес ресурса с данными

conn, cur = base.make_base()
name_log = argv[0]  # полное имя модуля
name_log = name_log.split('.')[0] # частичное имя модуля
log = logger.set_logger(name_log) # объявление логера


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


def chek_data(date, indexes, cur=cur, conn=conn):
    '''
    Проверка даты и цифровых индексов на их наличие в базе данных
    '''
    date_str = date.strftime("%d.%m.%Y")

    cur.execute("SELECT * FROM CURRENCY_ORDER;")
    date_result = cur.fetchall()

    if date_result == []:
        return True, 1, indexes

    date_result = {i[1]: i[0] for i in date_result}

    if date_str in date_result.keys():
        index = date_result[date_str]

        cur.execute("SELECT order_id, numeric_code FROM URRENCY_RATES WHERE order_id=?;", [(index)])
        index_result = cur.fetchall()
        index_result = [i[1] for i in index_result]

        for i in set(indexes) & set(index_result):
            log.warning(f"Запись с датой {date_str} и цифровым кодом {i} уже существует в базе данных")

        if set(indexes) == set(index_result):
            return False, None, indexes

        indexes = list(set(indexes) - set(index_result))

        return False, index, indexes

    cur.execute("SELECT id FROM CURRENCY_ORDER;")
    list_id = cur.fetchall()
    max_id = list_id[-1][0]
    max_id += 1

    return True, max_id, indexes


def set_data(id, date, data, currency_order, cur = cur, conn = conn):
    '''
    Добавление данных в базу данных
    '''
    
    date = date.strftime("%d.%m.%Y")
    
    if currency_order:
        order = (id, date)
        cur.execute("INSERT INTO CURRENCY_ORDER VALUES(?, ?);", order)

    if id != None:
        for i in data:
            Vname, Vcode, VchCode, Vnom, Vcurs = i["Vname"].rstrip(), i["Vcode"], i["VchCode"], i["Vnom"], i["Vcurs"]
            rates = (id, Vname, Vcode, VchCode, Vnom, Vcurs)
            cur.execute("INSERT INTO URRENCY_RATES VALUES(?, ?, ?, ?, ?, ?);", rates)
            
            log.info(f"Запись с датой {date} и цифровым кодом {Vcode} добавлена в базу данных")
            print(id, date, Vname, Vnom, Vcurs, sep = ", ")
  
    conn.commit()     


if __name__ == '__main__':

    date, indexes = get_date_indexes(argv)
    currency_order, id, indexes = chek_data(date, indexes)
    if id != None:
        data = df.data(date, url)
        f_data = filter_data(indexes, data)
        set_data(id, date, f_data, currency_order)

       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       