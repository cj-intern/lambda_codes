import boto3
import os
import json
import pymysql


config = {
        'user': os.environ["user"],
        'password': os.environ["password"],
        'host': os.environ["host"],
        'database': os.environ["database"]
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

def lambda_handler(event, context):
     if event['httpMethod'] == 'POST':
        # POST 요청의 본문 데이터를 JSON으로 파싱
        body = json.loads(event['body'])

        # 요청 본문에서 변수 추출
        id = body.get('id', 'none')
        if id == 'none':
            return {
                'statusCode': 404,
                'body': json.dumps({"message": "invalid email or none"}, default=str)                  
            }

        result = []

        for i in get_recommend(id):
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


        return{
            'statusCode': 200,
            "headers": {
            "Access-Control-Allow-Origin": "*",  # Allow all origins
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",  # Allow specific methods
            "Access-Control-Allow-Headers": "Content-Type"  # Allow specific headers
            },
            'body': json.dumps(result, default=str, ensure_ascii=False)
        }
                
