# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import csv, datetime
class GetCars(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS(executable_path="phantomjs")
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.otomoto.pl/"
        self.verificationErrors = []
        self.accept_next_alert = True
        
    
    def test_get_cars(self):
        driver = self.driver

        make_dict = {
            #'mitsubishi':['asx'],
                    #'volvo':['s60','s40''s40', 'xc-70','v50','v70'],
                    'ford':['mustang'],            

                    }
        yearFromText = "2009"
        yearToText = "2016"
        engineCapFromText = "1500"
        engineCapToText = "5000"
        fuelText = "petrol"


        for make, models in make_dict.items():
            for i in range(0,len(models)):
                link = ("https://www.otomoto.pl/osobowe/"+make+"/"+models[i]+
                "/?search%5Bfilter_float_year%3Afrom%5D="+yearFromText+
                "&search[filter_float_year%3Ato]="+yearToText+
                "&search[filter_float_engine_capacity%3Afrom]="+engineCapFromText+
                "&search[filter_float_engine_capacity%3Ato]="+engineCapToText+
                "&search%5Bfilter_enum_fuel_type%5D%5B0%5D="+fuelText+
                "&search%5Bcountry%5D=")

                driver.get(link)
                page_count = driver.execute_script('return window.ninjaPV.page_count')
                page_count = int(page_count)
                items = []
                if page_count>1:
                    for page in range(1,page_count+1):
                        link2 = link + '&page='+str(page)
                        items += self.get_items(driver, link2)
                    self.save_items(models[i], make, items)
                else:
                    items = self.get_items(driver, link)
                    self.save_items(models[i], make, items)
                    
    def save_items(self, model, make, items):
        with open('cars_' + make + '_'+model+ str(datetime.datetime.now()) + '.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            for k in items:
                k = [w.replace(' ', '') for w in k]
                k = [w.replace('PLN', '') for w in k]
                k = [w.replace('km', '') for w in k]
                writer.writerow(k)

    def get_items(self, driver, link):
        driver.get(link)
        print('collecting items from link: '+link)
        items = []
        for item in driver.find_elements_by_class_name('offer-item'):
            params = []
            for param in item.find_elements_by_class_name('offer-item__params-item'):
                params.append(param.find_element_by_xpath('span').text)
            params.append(item.find_element_by_class_name('offer-price__number').text)
            params.append(item.find_element_by_class_name('offer-title__link').get_attribute('data-ad-id'))
            items.append(params)
        print('items count = '+str(len(items)))
        for i in items:
            print(i)
        return items
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
