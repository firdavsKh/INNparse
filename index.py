from fastapi import FastAPI
import schedule
import time
import requests
import random
from threading import Thread
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import traceback
import cryptocode

key = "Admin7117"
app = FastAPI()
PORT = 3000
proxies = [
    'http://183.240.196.55:38080',
    'http://43.129.201.43:443'
]

def get_random_proxy():
    return random.choice(proxies)
def get_random_code():
    connection = psycopg2.connect(user="f1090364_xtdzl1",password="stat4omor",host="141.8.193.236",port="5432",database="f1090364_xtdzl1")
    cursor = connection.cursor()
    sql_query  = 'SELECT * FROM sma_stat_dep.tbl_tax_queue ORDER BY id DESC LIMIT 1'
    cursor.execute(sql_query)
    res = cursor.fetchone()
    if(res==None):
        sql_query = "INSERT INTO sma_stat_dep.tbl_tax_queue (inn_code,region_section_code,last_seven_numb,status) VALUES('035000001','03','5000001',true)"
        cursor.execute(sql_query)
        connection.commit()
        res = ['035000001','03','5000001']
    cursor.close()
    connection.close()
    return res


def add_one(in_arg):
    return str(int(in_arg) + 1).zfill(len(in_arg))
def job():
    proxy = get_random_proxy()
    proxies_dict = {
        "http": proxy,
        "https": proxy
    }
    try:
        try:
            response = requests.get(f"https://andoz.tj/ForTaxpayer/getInfoByInn?inn={get_random_code()[1]}", proxies=proxies_dict)
        except:
            response = requests.get(f"https://andoz.tj/ForTaxpayer/getInfoByInn?inn={get_random_code()[1]}")
        if response.status_code == 200:
            connection = psycopg2.connect(user="f1090364_xtdzl1",password="stat4omor",host="141.8.193.236",port="5432",database="f1090364_xtdzl1")
            cursor = connection.cursor()
            status = 'false'
            if(response.json().get('userInfo')!=None):
                print(response.json().get('userInfo'))
                person = response.json().get('userInfo')[0]
                sql_query = f"""WITH first_insert AS (
                        INSERT INTO sma_stat_dep.tbl_tax_id (inn, upload_tstmp, required_update)
                        VALUES ('{get_random_code()[1]}', CURRENT_TIMESTAMP, 'false')
                        RETURNING id AS first_table_id
                    ),
                    second_insert AS (
                        INSERT INTO sma_stat_dep.tbl_individuals (tax_id, fst_name, lst_name, full_name, sex, brth_date, citizenship_1, upload_tstmp)
                        SELECT first_table_id,'{cryptocode.encrypt(person["Name"],key)}','{cryptocode.encrypt(person["Fam"],key)}','{cryptocode.encrypt(person["Full_nameK"],key)}','{person["pol"]}','{person["Date_roj"]}','{person["Citizenship"]}',CURRENT_TIMESTAMP
                        FROM first_insert
                    ),
                    third_insert AS (
                        INSERT INTO sma_stat_dep.tbl_document (document_id,document_type, issuer, issue_date, upload_tstmp, status)
                        SELECT '{person["N_Passport"]}','N_Passport','{person["PassportVidanName"]}','{person["Date_vidach"]}',CURRENT_TIMESTAMP,true
                        FROM first_insert
                    )
                    INSERT INTO sma_stat_dep.tbl_addresses (inspection_name,inspection_code,inspection_id,address_text,address_phone,upload_tstmp)
                    SELECT '{cryptocode.encrypt(person["inspectionName"],key)}','{person["inspectionRamz"]}','{person["id_insp"]}','{cryptocode.encrypt(person["adr_txt"],key)}','{person["adr_phone"]}',CURRENT_TIMESTAMP
                    FROM first_insert"""
                
                cursor.execute(sql_query)
                connection.commit()
                status = 'true'
            else:
                status = 'false'
            randcode = get_random_code()
            region = randcode[2]
            if(randcode[3]==9999999):
                region = add_one(randcode[2])
            sql_query = f"INSERT INTO sma_stat_dep.tbl_tax_queue (inn_code,region_section_code,last_seven_numb,status) VALUES('{add_one(randcode[1])}','{region}','{add_one(randcode[3])}',{status})"
            cursor.execute(sql_query)
            connection.commit()
            cursor.close()
            connection.close()
        else:
            print(f"Ошибка: {response.status_code}")
        
    except Exception as e:
        print(f"Ошибка: {e}",traceback.print_exc())
    
    

def run_scheduler():
    schedule.every(5).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()
