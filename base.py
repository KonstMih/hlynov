# -*- coding: utf-8 -*-


import sqlite3


def make_base():
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