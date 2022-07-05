# -*- coding: utf-8 -*-

import requests
import re
import datetime


def get_text(date, url):
    
    '''
    Получение ответа по запросу
    '''

    body = f"""
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <GetCursOnDateXML xmlns="http://web.cbr.ru/">
          <On_date>{date}</On_date>
        </GetCursOnDateXML>
      </soap:Body>
    </soap:Envelope>
    """
    
    body = body.encode('utf-8')
    
    session = requests.session()
    session.headers = {"Content-Type": "text/xml; charset=utf-8"}
    session.headers.update({"Content-Length": str(len(body))})
    response = session.post(url=url, data=body, verify=True)
    
    text = response.text
    
    return text


def get_data_xml(text: str) -> list[str]:
    '''
    Разбиение текста ответа на части по валютам
    '''
    text = re.findall(r'xmlns="">(.+)</ValuteData>', text)
    text = text[0]
    data = text.split("<ValuteCursOnDate>")
    data_list = data[1:]
        
    return data_list
   
 
def get_data(data_xml: list[str]) -> dict[str, dict[str, str]]:
    '''
    Преобразование каждой части в словарь с данными
    '''
    data = {}
    for i in data_xml:
        Vname = re.findall(r'<Vname>(.+)</Vname>', i)
        Vnom = re.findall(r'<Vnom>(.+)</Vnom>', i)
        Vcurs = re.findall(r'<Vcurs>(.+)</Vcurs>', i)
        Vcode = re.findall(r'<Vcode>(.+)</Vcode>', i)
        VchCode = re.findall(r'<VchCode>(.+)</VchCode>', i)
        data[Vcode[0]] = {"Vname":Vname[0], "Vnom":Vnom[0], "Vcurs":Vcurs[0], "Vcode":Vcode[0], "VchCode":VchCode[0]}
    
    return data



def data(date, url: str) -> dict[str, dict[str, str]]:
    '''
    Объединяющая функция для получения данных напрямую из даты и адреса ресурса
    '''
    text = get_text(date, url)
    data_xml = get_data_xml(text)
    data = get_data(data_xml)
    return data


if __name__ == "__main__":
    
    url = 'https://www.cbr.ru/dailyinfowebserv/dailyinfo.asmx?wsdl'
    date = datetime.date(2022, 6, 23)
    text = get_text(date, url)
    data_xml = get_data_xml(text)
    data = data(date, url)
    


























