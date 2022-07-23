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

# Number=''
Description=''
EntityPurchasingUnit=''
Dependence=''
Date=''
AwardModality=''
Condition=''
Number=''
DescriptionOfTheRequest=''
ObjectOfTheContract=''
Entity=''
Dependence=''
PurchaseUnit=''
Address=''
Name=''
Position=''
Telephone=''
Email=''
ListingNumber=''
TypeOfProcedure=''
ContractualObject=''
Description1=''
PublicationDate=''
DateAndTimeOfPresentationOfQuotes=''
QuoteOpeningDateAndTime=''
PlaceOfPresentatioOfQuotes=''
EstimatedPrice=''
DeliveryProvince=''
DeliveryMethod=''
DeliveryDays=''
WayToPay=''
R=''
Code=''
Classification=''
Quantity=''
UnitOfMeasurement=''
Description2=''
SES=''

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
    soup = BeautifulSoup(sourcecode,"html.parser")
    table = soup.find('table' ,attrs={'class':'table caption-top table-hover'})
    table_rows = table.find_all('tr')
    l = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        l.append(row)
    # print("l",l[1][0])
    for i in range(1,len(l)):
        Number=l[i][0]
        Description=l[i][1]
        EntityPurchasingUnit=l[i][2]
        Dependence=l[i][3]
        Date=l[i][4]
        AwardModality=l[i][5]
        Condition=l[i][6]
        # df=pd.DataFrame(l, columns=["Number","Description","EntityPurchasingUnit","Dependence","Date","AwardModality","Condition"])[1:]
        # print(df)
        db_string = "postgres://postgres:root@localhost:5432/main"
        db = create_engine(db_string)
        meta1 = MetaData(db)

        onlinequote_table = Table('OnlineQuote', meta1,  
                                Column('Number', String),
                                Column('Description', String),
                                Column('EntityPurchasingUnit', String),
                                Column('Dependence', String),
                                Column('Date', String),
                                Column('AwardModality', String),
                                Column('Condition', String))

        with db.connect() as conn:
            # insert_statement = specs_table.
            insert_statement = insert(onlinequote_table).values(
                Number=Number,
                Description=Description,
                EntityPurchasingUnit=EntityPurchasingUnit,
                Dependence=Dependence,
                Date=Date,
                AwardModality=AwardModality,
                Condition=Condition)
            conn.execute(insert_statement)
            print("DoneFirScreen")

    links = soup.findAll('a',attrs={'class':'text-decoration-none text-blue-dark'})
    link_list=[]
    for link in links:
        link_list.append(link.get('href'))
        # print("link",link)
    # print("link_list",link_list)
    for l in link_list:
        driver.get('https://www.panamacompra.gob.pa'+l)
        sleep(3)
        sc=driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        sp=BeautifulSoup(sc,"html.parser")
        tablelist1=sp.findAll('table', class_='table')
        # print(tablelist1)
        l1 = []
        for tr in tablelist1:
            td = tr.find_all('tr')
            row = [tr.text for tr in td]
            l1.append(row)
        # print("l1-----------------------------\n",l1)

        Number=l1[0][0].split(": ")[1]
        DescriptionOfTheRequest=l1[0][1].split(": ")[1]
        ObjectOfTheContract=l1[0][2].split(": ")[1]
        Entity=l1[1][0].split(": ")[1]
        Dependence=l1[1][1].split(": ")[1]
        PurchaseUnit=l1[1][2].split(": ")[1]
        Address=l1[1][3].split(": ")[1:] #############################
        Name=l1[2][0].split(": ")[1]
        Position=l1[2][1].split(": ")[1]
        Telephone=l1[2][2].split(": ")[1]
        Email=l1[2][3].split(": ")[1]
        ListingNumber=l1[3][0].split(": ")[1]
        TypeOfProcedure=l1[3][1].split(": ")[1]
        ContractualObject=l1[3][2].split(": ")[1]
        Description1=l1[3][3].split(": ")[1]
        PublicationDate=l1[3][4].split(": ")[1]
        DateAndTimeOfPresentationOfQuotes=l1[3][5].split(": ")[1]
        QuoteOpeningDateAndTime=l1[3][6].split(": ")[1]
        PlaceOfPresentatioOfQuotes=l1[3][7].split(": ")[1]
        EstimatedPrice=l1[3][8].split(": ")[1]
        DeliveryProvince=l1[3][9].split(": ")[1]
        DeliveryMethod=l1[4][0].split(": ")[1]
        DeliveryDays=l1[4][1].split(": ")[1]
        WayToPay=l1[4][2].split(": ")[1]

        t=sp.find('table' ,attrs={"ng-if":"item.type=='bs'"})
        l2=[]
        td_t = t.find_all('td')
        for tr in td_t:
            l2.append(tr.text) 

        R=l2[0]
        Code=l2[1]
        Classification=l2[2]
        Quantity=l2[3]
        UnitOfMeasurement=l2[4]
        Description2=l2[5]
        SES=l2[6]

        db_string = "postgres://postgres:root@localhost:5432/main"
        db = create_engine(db_string)
        meta2 = MetaData(db) 
        specs_table = Table('Specifications', meta2,  
                            Column('Number', String),
                            Column('DescriptionOfTheRequest', String),
                            Column('ObjectOfTheContract', String),
                            Column('Entity', String),
                            Column('Dependence', String),
                            Column('PurchaseUnit', String),
                            Column('Address', String),
                            Column('Name', String),
                            Column('Position', String),
                            Column('Telephone', String),
                            Column('Email', String),
                            Column('ListingNumber', String),
                            Column('TypeOfProcedure', String),
                            Column('ContractualObject', String),
                            Column('Description1', String),
                            Column('PublicationDate', String),
                            Column('DateAndTimeOfPresentationOfQuotes', String),
                            Column('QuoteOpeningDateAndTime', String),
                            Column('PlaceOfPresentatioOfQuotes', String),
                            Column('EstimatedPrice', String),
                            Column('DeliveryProvince', String),
                            Column('DeliveryMethod', String),
                            Column('DeliveryDays', String),
                            Column('WayToPay', String),                    
                            Column('R', String),
                            Column('Code', String),
                            Column('Classification', String),
                            Column('Quantity', String),
                            Column('UnitOfMeasurement', String),
                            Column('Description2', String),
                            Column('SES', String)                        
                        )

        with db.connect() as conn:
            # insert_statement = specs_table.
            insert_statement = insert(specs_table).values(
                Number = Number,
                DescriptionOfTheRequest = DescriptionOfTheRequest,
                ObjectOfTheContract = ObjectOfTheContract,
                Entity = Entity,
                Dependence = Dependence,
                PurchaseUnit = PurchaseUnit,
                Address = Address,
                Name = Name,
                Position = Position,
                Telephone = Telephone,
                Email = Email,
                ListingNumber = ListingNumber,
                TypeOfProcedure = TypeOfProcedure,
                ContractualObject = ContractualObject,
                Description1 = Description1,
                PublicationDate = PublicationDate,
                DateAndTimeOfPresentationOfQuotes = DateAndTimeOfPresentationOfQuotes,
                QuoteOpeningDateAndTime = QuoteOpeningDateAndTime,
                PlaceOfPresentatioOfQuotes = PlaceOfPresentatioOfQuotes,
                EstimatedPrice = EstimatedPrice,
                DeliveryProvince = DeliveryProvince,
                DeliveryMethod = DeliveryMethod,
                DeliveryDays = DeliveryDays,
                WayToPay = WayToPay,
                R = R,
                Code = Code,
                Classification = Classification,
                Quantity = Quantity,
                UnitOfMeasurement = UnitOfMeasurement,
                Description2 = Description2,
                SES = SES             
                )
        
            conn.execute(insert_statement)
            print("DoneSecScreen")



def db_read():
    db_string = "postgres://postgres:root@localhost:5432/main"
    db = create_engine(db_string)

    # Create  
    onlinequote_res_set = db.execute('select * from public."OnlineQuote"')
    for r in onlinequote_res_set:  
        print(r)
        print("here1")

    specification_res_set = db.execute('select * from public."Specifications"')
    for r in specification_res_set:  
        print(r)
        print("here2")

def ScrapeSecScreen():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("C:/Users/pralo/Downloads/DE/chromedriver", chrome_options=options)

    driver.get('https://www.panamacompra.gob.pa/Inicio/v2/#!/vistaPreviaCP?NumLc=2022-1-42-0-01-CL-007581&esap=0&nnc=0&it=1')
    sleep(5)
    sourcecode = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    # print(sourcecode)
    soup = BeautifulSoup(sourcecode,"html.parser")
    
    tablelist1=soup.findAll('table', class_='table')
    l1 = []
    for tr in tablelist1:
        td = tr.find_all('tr')
        row = [tr.text for tr in td]
        l1.append(row)

    #######################################################################################################################################################
    Number=l1[0][0].split(": ")[1]
    DescriptionOfTheRequest=l1[0][1].split(": ")[1]
    ObjectOfTheContract=l1[0][2].split(": ")[1]
    Entity=l1[1][0].split(": ")[1]
    Dependence=l1[1][1].split(": ")[1]
    PurchaseUnit=l1[1][2].split(": ")[1]
    Address=l1[1][3].split(": ")[1:] #############################
    Name=l1[2][0].split(": ")[1]
    Position=l1[2][1].split(": ")[1]
    Telephone=l1[2][2].split(": ")[1]
    Email=l1[2][3].split(": ")[1]
    ListingNumber=l1[3][0].split(": ")[1]
    TypeOfProcedure=l1[3][1].split(": ")[1]
    ContractualObject=l1[3][2].split(": ")[1]
    Description1=l1[3][3].split(": ")[1]
    PublicationDate=l1[3][4].split(": ")[1]
    DateAndTimeOfPresentationOfQuotes=l1[3][5].split(": ")[1]
    QuoteOpeningDateAndTime=l1[3][6].split(": ")[1]
    PlaceOfPresentatioOfQuotes=l1[3][7].split(": ")[1]
    EstimatedPrice=l1[3][8].split(": ")[1]
    DeliveryProvince=l1[3][9].split(": ")[1]
    DeliveryMethod=l1[4][0].split(": ")[1]
    DeliveryDays=l1[4][1].split(": ")[1]
    WayToPay=l1[4][2].split(": ")[1]

    
    t=soup.find('table' ,attrs={"ng-if":"item.type=='bs'"})
    
    l2=[]
    td_t = t.find_all('td')
    for tr in td_t:
        l2.append(tr.text) 

    R=l2[0]
    Code=l2[1]
    Classification=l2[2]
    Quantity=l2[3]
    UnitOfMeasurement=l2[4]
    Description2=l2[5]
    SES=l2[6]

    # print(SES)


    db_string = "postgres://postgres:root@localhost:5432/main"
    db = create_engine(db_string)
    meta = MetaData(db) 
    specs_table = Table('Specifications', meta,  
                        Column('Number', String),
                        Column('DescriptionOfTheRequest', String),
                        Column('ObjectOfTheContract', String),
                        Column('Entity', String),
                        Column('Dependence', String),
                        Column('PurchaseUnit', String),
                        Column('Address', String),
                        Column('Name', String),
                        Column('Position', String),
                        Column('Telephone', String),
                        Column('Email', String),
                        Column('ListingNumber', String),
                        Column('TypeOfProcedure', String),
                        Column('ContractualObject', String),
                        Column('Description1', String),
                        Column('PublicationDate', String),
                        Column('DateAndTimeOfPresentationOfQuotes', String),
                        Column('QuoteOpeningDateAndTime', String),
                        Column('PlaceOfPresentatioOfQuotes', String),
                        Column('EstimatedPrice', String),
                        Column('DeliveryProvince', String),
                        Column('DeliveryMethod', String),
                        Column('DeliveryDays', String),
                        Column('WayToPay', String),                    
                        Column('R', String),
                        Column('Code', String),
                        Column('Classification', String),
                        Column('Quantity', String),
                        Column('UnitOfMeasurement', String),
                        Column('Description2', String),
                        Column('SES', String)                        
                       )



    with db.connect() as conn:
        # insert_statement = specs_table.
        insert_statement = insert(specs_table).values(
            Number = Number,
            DescriptionOfTheRequest = DescriptionOfTheRequest,
            ObjectOfTheContract = ObjectOfTheContract,
            Entity = Entity,
            Dependence = Dependence,
            PurchaseUnit = PurchaseUnit,
            Address = Address,
            Name = Name,
            Position = Position,
            Telephone = Telephone,
            Email = Email,
            ListingNumber = ListingNumber,
            TypeOfProcedure = TypeOfProcedure,
            ContractualObject = ContractualObject,
            Description1 = Description1,
            PublicationDate = PublicationDate,
            DateAndTimeOfPresentationOfQuotes = DateAndTimeOfPresentationOfQuotes,
            QuoteOpeningDateAndTime = QuoteOpeningDateAndTime,
            PlaceOfPresentatioOfQuotes = PlaceOfPresentatioOfQuotes,
            EstimatedPrice = EstimatedPrice,
            DeliveryProvince = DeliveryProvince,
            DeliveryMethod = DeliveryMethod,
            DeliveryDays = DeliveryDays,
            WayToPay = WayToPay,
            R = R,
            Code = Code,
            Classification = Classification,
            Quantity = Quantity,
            UnitOfMeasurement = UnitOfMeasurement,
            Description2 = Description2,
            SES = SES             
            )
       
        conn.execute(insert_statement)
        print("Done")


Scrape()
# ScrapeSecScreen()

