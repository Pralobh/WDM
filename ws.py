# import these two modules bs4 for selecting HTML tags easily
from distutils.filelist import findall
from time import sleep
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.dialects.mysql import insert


def Scrape():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("C:/Users/pralo/Downloads/DE/chromedriver", chrome_options=options)

    driver.get('https://www.panamacompra.gob.pa/Inicio/#/')
    sleep(10)
    driver.find_element(By.XPATH,'//button[text()=" Iniciar sesión"]').click()
    # driver.find_element("button.btn:nth-child(3)").click()
    print("clicked 1")
    sleep(5)
    # userid = driver.find_element_by_id('userName')
    # userid.send_keys("yulenny27")
    # password = driver.find_element_by_id('password')
    # password.send_keys('Soluciones22')
    # driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/ng-component/div/form/div[1]/button').click()
    # sleep(5)
    # sourcecode = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    # soup = BeautifulSoup(sourcecode,"html.parser")
    # table = soup.find('table' ,attrs={'class':'table caption-top table-hover'})
    # print('table--------------------------------\n',table)

Scrape()



      