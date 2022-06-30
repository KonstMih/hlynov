# -*- coding: utf-8 -*-

import df
import logger
import base
from datetime import datetime
from sys import argv

url = 'http://www.cbr.ru/dailyinfowebserv/dailyinfo.asmx?wsdl'

conn, cur = base.make_base()

name_log = argv[0]
name_log = name_log.split('.')[0]
log = logger.set_logger(name_log)


def get_date_indexs(arg: list):
    date = datetime.strptime(arg[1], "%d.%m.%Y")
    date = date.date()
    indexes = argv[2:]
    return date, indexes


def filter_data(indexes: list[str], data: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    f_data = [data[i] for i in indexes]
    return f_data


def set_data(id, date, data, currency_order, cur = cur, conn = conn):
    
    date = date.strftime("%d.%m.%Y")
    
    if currency_order:
        order = (id, date)
        cur.execute("INSERT INTO CURRENCY_ORDER VALUES(?, ?);", order)

    if id != None:
        for i in data:
            Vname, Vcode, VchCode, Vnom, Vcurs = i["Vname"].rstrip(), i["Vcode"], i["VchCode"], i["Vnom"], i["Vcurs"]
            rates = (id, Vname, Vcode, VchCode, Vnom, Vcurs)
            cur.execute("INSERT INTO URRENCY_RATES VALUES(?, ?, ?, ?, ?, ?);", rates)
            
            log.info(f"Запись с датой {date} и цифровым кодом {Vcode} добавлена в таблицу")
            print(id, date, Vname, Vnom, Vcurs, sep = ", ")
  
    conn.commit()     


def chek_data(date, indexes,  cur = cur, conn = conn):
    
    date_str = date.strftime("%d.%m.%Y")
    
    cur.execute("SELECT * FROM CURRENCY_ORDER;")
    date_result = cur.fetchall()
    
    if date_result == []:
        return True, 1, indexes
    
    date_result = {i[1]:i[0] for i in date_result}
    
    if date_str in date_result.keys():
        index = date_result[date_str]
        
        cur.execute("SELECT order_id, numeric_code FROM URRENCY_RATES WHERE order_id=?;", [(index)])
        index_result = cur.fetchall()
        index_result = [i[1] for i in index_result]
        
        for i in set(indexes)&set(index_result):
            log.warning(f"Запись с датой {date_str} и цифровым кодом {i} уже существует в таблице")
        
        if set(indexes) == set(index_result):
            return False, None, indexes
                              
        indexes = list(set(indexes)-set(index_result))
   
        return False, index, indexes
    
    cur.execute("SELECT id FROM CURRENCY_ORDER;")
    list_id = cur.fetchall()
    max_id = list_id[-1][0]
    max_id += 1
     
    return True, max_id, indexes
        

    

if __name__ == '__main__':
    
    date, indexes = get_date_indexs(argv)
    currency_order, id, indexes = chek_data(date, indexes)
    if id != None:
        data = df.data(date, url)
        f_data = filter_data(indexes, data)
        set_data(id, date, f_data, currency_order)
        
        

    
        
    
    
    '''
    date, indexes = get_date_indexs(argv)
    data = df.data(date, url)
    f_data = filter_data(indexes, data)
    id_1 = chek_data(date)
    set_data(id_1, date, f_data)
'''

    
    

    
     
    '''
    date_today  = datetime.date.today()
    date_day  = datetime.date(2022, 6, 23)
    
    
    for i in range(2):
        
        if i == 0:
            id_1 = chek_data(date_today)
            assert id_1 != None, 'Очистить таблицу'
            data = df.data(date_today, url)
            set_data(id_1, date_today, data)
            
            id_2 = chek_data(date_today)
            assert id_2 == None, 'Неверное определение даты в таблице'
            
            id_3 = chek_data(date_day)
            assert id_3 != None, 'Очистить таблицу'
            data = df.data(date_day, url)
            set_data(id_3, date_day, data)
            
            id_4 = chek_data(date_today)
            assert id_4 == None, 'Неверное определение даты в таблице'

    
    
        if i == 1:
            id_1 = chek_data(date_today)
            assert id_1 == None, 'Неверное определение даты в таблице'
            
            id_2 = chek_data(date_today)
            assert id_2 == None, 'Неверное определение даты в таблице'
            
            id_3 = chek_data(date_day)
            assert id_3 == None, 'Неверное определение даты в таблице'
            
            id_4 = chek_data(date_today)
            assert id_4 == None, 'Неверное определение даты в таблице'

       '''
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       