# -*- coding: utf-8 -*-

import sqlite3

class Base():
    def __init__(self, log):
        self.log = log
        self.conn, self.cur = self.make_base()
        

    def make_base(self):
        '''
        Создание базы данных
        '''
    
        conn = sqlite3.connect('orders.db')
        cur = conn.cursor()
        
        cur.execute("""CREATE TABLE IF NOT EXISTS CURRENCY_ORDER(
           id INT PRIMARY KEY,
           ondate TEXT);
        """)
        conn.commit()
        
        cur.execute("""CREATE TABLE IF NOT EXISTS URRENCY_RATES(
           order_id INT,
           name TEXT,
           numeric_code TEXT,
           alphabetic_code TEXT,
           scale INT,
           rate INT,
           FOREIGN KEY (order_id) REFERENCES CURRENCY_ORDER (id));
        """)
        conn.commit()
        
        return conn, cur
    
    
    def chek_data(self, date, indexes):
        '''
        Проверка даты и цифровых индексов на их наличие в базе данных
        '''
        date_str = date.strftime("%d.%m.%Y")

        self.cur.execute("SELECT * FROM CURRENCY_ORDER;")
        date_result = self.cur.fetchall()

        if date_result == []:
            return True, 1, indexes

        date_result = {i[1]: i[0] for i in date_result}

        if date_str in date_result.keys():
            index = date_result[date_str]

            self.cur.execute("SELECT order_id, numeric_code FROM URRENCY_RATES WHERE order_id=?;", [(index)])
            index_result = self.cur.fetchall()
            index_result = [i[1] for i in index_result]

            for i in set(indexes) & set(index_result):
                self.log.warning(f"Запись с датой {date_str} и цифровым кодом {i} уже существует в базе данных")

            if set(indexes) == set(index_result):
                return False, None, indexes

            indexes = list(set(indexes) - set(index_result))

            return False, index, indexes

        self.cur.execute("SELECT id FROM CURRENCY_ORDER;")
        list_id = self.cur.fetchall()
        max_id = list_id[-1][0]
        max_id += 1

        return True, max_id, indexes
    
    
    def set_data(self, id, date, data, currency_order):
        '''
        Добавление данных в базу данных
        '''
        
        date = date.strftime("%d.%m.%Y")
        
        if currency_order:
            order = (id, date)
            self.cur.execute("INSERT INTO CURRENCY_ORDER VALUES(?, ?);", order)
    
        if id != None:
            for i in data:
                Vname, Vcode, VchCode, Vnom, Vcurs = i["Vname"].rstrip(), i["Vcode"], i["VchCode"], i["Vnom"], i["Vcurs"]
                rates = (id, Vname, Vcode, VchCode, Vnom, Vcurs)
                self.cur.execute("INSERT INTO URRENCY_RATES VALUES(?, ?, ?, ?, ?, ?);", rates)
                
                self.log.info(f"Запись с датой {date} и цифровым кодом {Vcode} добавлена в базу данных")
                print(id, date, Vname, Vnom, Vcurs, sep = ", ")
      
        self.conn.commit()  