# -*- coding: utf-8 -*-

import unittest
import df

class Test_bank(unittest.TestCase):
        
    text_list_xml = 'etd354!#$@xmlns=""><ValuteCursOnDate>1<ValuteCursOnDate>2#<ValuteCursOnDate>a+-*<ValuteCursOnDate>bdя </ValuteData>%&#$(*648gde'
    result_text_list_xml = ['1', '2#', 'a+-*', 'bdя ']
    
    def test_get_data_xml(self, data = text_list_xml, result = result_text_list_xml ):
        self.assertEqual(df.get_data_xml(data), result)

    #-------------------------------------------------------------------------------------------------------------
        
    text_list = ['24356<Vname>ABc </Vname>56476<Vnom>123</Vnom>4#%<Vcurs>125.236</Vcurs>sd<Vcode>1fп/ </Vcode>вап<VchCode>254авп</VchCode>gghng', 
                 'апапр<Vname>Абв dcdв</Vname>dhfh<Vnom>456</Vnom>@$%ht65<Vcurs>84.325</Vcurs>46<Vcode>25eот*</Vcode>rgv<VchCode>347</VchCode>:№%;*(']
    
    result_text_list = {'1fп/ ':{'Vnom':'123', 'Vcurs':'125.236', 'Vcode':'1fп/ ', 'VchCode':'254авп', 'Vname':'ABc '},
                        '25eот*':{'Vnom':'456', 'Vcurs':'84.325', 'Vcode':'25eот*', 'VchCode':'347', 'Vname':'Абв dcdв'}}
    
    def test_get_data(self, data = text_list, result = result_text_list ):
        self.assertEqual(df.get_data(data), result)


if __name__ == "__main__":
    unittest.main()
