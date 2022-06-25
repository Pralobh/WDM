# import these two modules bs4 for selecting HTML tags easily
from time import sleep
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("C:/Users/pralo/Downloads/DE/chromedriver", chrome_options=options)

driver.get('https://www.panamacompra.gob.pa/Inicio/#/acceso-directo/cotizaciones-en-linea')
# driver.get('https://www.panamacompra.gob.pa/Inicio/#!/')
sleep(5)
# venue = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="list-group-item hvr-icon-forward"]')))
# venue.click()
sourcecode = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
print(sourcecode)

soup = BeautifulSoup(sourcecode,"html.parser")
# results = soup.findAll("th",{"scope":"row"})
results = soup.findAll("td", {"class" : "align-middle"})
# Number = soup.findAll("a", {"class":"text-decoration-none text-blue-dark"})
print(type(results))
# print(results)
count=1

table = soup.find('table' ,attrs={'class':'table caption-top table-hover'})
print(table)
table_rows = table.find_all('th')
# table_rows = table.find_all('tr')
# print(table_rows)
l = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    l.append(row)
# df=pd.DataFrame(l, columns=["Num","Number","Description","Entity / Purchasing unit","Dependence","Date","Award modality","Condition"])[1:]\
print(l)

# print(df)
# from sqlalchemy import create_engine
# engine = create_engine('postgresql://postgres:root@localhost:5433/flasksql')
# df.to_sql('data1', engine)
# print("Done")
