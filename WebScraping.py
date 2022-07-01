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

def Scrape():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("C:/Users/pralo/Downloads/DE/chromedriver", chrome_options=options)

    driver.get('https://www.panamacompra.gob.pa/Inicio/#/acceso-directo/cotizaciones-en-linea')
    # driver.get('https://www.panamacompra.gob.pa/Inicio/#!/')
    sleep(5)

    sourcecode = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    # print(sourcecode)

    soup = BeautifulSoup(sourcecode,"html.parser")
    # results = soup.findAll("th",{"scope":"row"})
    results = soup.findAll("td", {"class" : "align-middle"})
    # Number = soup.findAll("a", {"class":"text-decoration-none text-blue-dark"})

    table = soup.find('table' ,attrs={'class':'table caption-top table-hover'})
    # print(table)
    # table_rows = table.find_all('td')
    table_rows = table.find_all('tr')
    # print(table_rows)
    l = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        l.append(row)
    # print("l----------------------------------------------------------\n",l)
    df=pd.DataFrame(l, columns=["Number","Description","Entity-PurchasingUnit","Dependence","Date","AwardModality","Condition"])[1:]
    print(df)


def db():
    db_string = "postgres://postgres:root@localhost:5432/main"
    db = create_engine(db_string)

    # Create  
    result_set = db.execute('select * from public."OnlineQuote"')
    for r in result_set:  
        print(r)
        print("here")


def ScrapeSecScreen():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("C:/Users/pralo/Downloads/DE/chromedriver", chrome_options=options)

    driver.get('https://www.panamacompra.gob.pa/Inicio/v2/#!/vistaPreviaCP?NumLc=2022-0-30-0-08-CL-024792&esap=0&nnc=0&it=1')
    sleep(5)
    sourcecode = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    # print(sourcecode)
    soup = BeautifulSoup(sourcecode,"html.parser")
    # print(soup)

    #######################################################################################################################################################
    table1 = soup.find('table' ,attrs={'class':'table table-condensed table-bordered last-line-table'})

    # table_rows = table.find_all('td')
    table_rows1 = table1.find_all('tr')
    # print(table_rows1)
    l1,l2 = [],[]
    for tr in table_rows1:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        # l.append(row[1])
    # print("l----------------------------------------------------------\n",l)
    # df=pd.DataFrame(l, columns=["Number","Description","Entity-PurchasingUnit","Dependence","Date","AwardModality","Condition"])[1:]
    # print(df)
    #######################################################################################################################################################
    tablelist1=soup.findAll('table',{'class':'table table-condensed table-bordered last-line-table'})
    for tr in tablelist1:
        td = tr.find_all('tr')
        row = [tr.text for tr in td]
        l1.append(row)
    # print(l1)
    # print(l1[0][0])

    #######################################################################################################################################################
    # div=soup.find('div',{'class':'panel panel-default export-pdf'})
    # print(div)
    # tablelist2=div.findAll('table',{'class':'table table-condensed table-bordered last-line-table'})
    # for tr in tablelist2:
    #     td = tr.find_all('tr')
    #     row = [tr.text for tr in td]
    #     l2.append(row)
    # print(l2)
    # print(l2[0][0])

    print(tablelist1)




# Scrape()
ScrapeSecScreen()
