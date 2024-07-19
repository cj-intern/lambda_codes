import boto3
import os
import json
import pymysql


config = {
        'user': 'admin',
        'password': '0}7(fwXLF[S0TI:BucRP{vOy$n$7',
        'host': 'intern-rds-2.coxwo6u60is7.ap-northeast-2.rds.amazonaws.com',
        'database': 'mydb'
    }
        # MySQL 연결
connection = pymysql.connect(user=config['user'],
                            password=config['password'],
                            host=config['host'],
                            database=config['database'],
                            charset="utf8")
def get_production_items(product_id):
    # MySQL 연결 설정
    try:
        with connection.cursor() as cursor:
            # Example query to fetch rows from a table named 'your_table'
            sql = f"SELECT * FROM products WHERE product_id={product_id}"
            cursor.execute(sql)
            rows = cursor.fetchall()
        
        # Return the fetched rows
        return rows
    except Exception as e:
        return {'error': str(e)}
    #finally:
        # connection.close()

def get_recommend(user_id):
    # MySQL 연결 설정
    try:
        with connection.cursor() as cursor:
            # Example query to fetch rows from a table named 'your_table'
            sql = f"SELECT * FROM recommendations WHERE user_id='{user_id}'"
            cursor.execute(sql)
            rows = cursor.fetchall()
        
        # Return the fetched rows
        return rows
    except Exception as e:
        return {'error': str(e)}
    #finally:
        #connection.close()
    
result = []

for i in get_recommend("rlwjddl1596@naver.com"):
    for x in get_production_items(i[2]):
        print(x)
        tmp = dict()
        tmp["product_id"] = x[0]
        tmp["product_name"] = x[1] 
        tmp["moisture"] =  x[2]
        tmp["sensitivity"] = x[3]
        tmp["texture"] = x[4]
        tmp["acne"] = x[5]
        tmp["wrinkle"] = x[6]
        tmp["whitening"] = x[7]
        tmp["price"] = x[8]
        tmp["url"]= x[9]
        result.append(tmp)


print(result)