# -*- coding: utf-8 -*-

import df
import logger
import base
from datetime import datetime
from sys import argv

url = 'http://www.cbr.ru/dailyinfowebserv/dailyinfo.asmx?wsdl'

conn, cur = base.make_base()
log = logger.set_logger()

def get_date_indexs(arg: list):
    date = datetime.strptime(arg[1], "%d.%m.%Y")
    date = date.date()
    indexes = argv[2:]
    return date, indexes



def filter_data(indexes: list[str], data: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    f_data = [data[i] for i in indexes]
    return f_data

def set_data(id, date, data, cur = cur, conn = conn):
        
    date = date.strftime("%d.%m.%Y")
    order = (id, date)
    cur.execute("INSERT INTO CURRENCY_ORDER VALUES(?, ?);", order)

    for i in data:
        rates = (id, i["Vname"], i["Vcode"], i["VchCode"], i["Vnom"], i["Vcurs"])
        cur.execute("INSERT INTO URRENCY_RATES VALUES(?, ?, ?, ?, ?, ?);", rates)
            
    log.info(f"Запись с датой {date} добавлена в таблицу")
        
    conn.commit()

        

def chek_data(date, cur = cur, conn = conn):
    
    """
    Проверка наличия 
    """
    date = date.strftime("%d.%m.%Y")
    
    cur.execute("SELECT ondate FROM CURRENCY_ORDER;")
    date_result = cur.fetchall()
    
    if date_result == []:
        return 1
    
    date_result = [i[0] for i in date_result]
    
    
    if not(date in date_result): 
       cur.execute("SELECT id FROM CURRENCY_ORDER;")
       list_id = cur.fetchall()
       max_id = list_id[-1][0]
       return max_id + 1
   
    
    log.warning(f"Запись с датой {date} уже существует в таблице")
    return None
       


if __name__ == '__main__':
    
    argv = ['main.py', '28.06.2022', '410', '710', '756']
    date, indexes = get_date_indexs(argv)
    data = df.data(date, url)
    f_data = filter_data(indexes, data)
    id_1 = chek_data(date)
    set_data(id_1, date, f_data)


    
    

    
     
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
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       