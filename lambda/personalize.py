import boto3
import os
import json
import pymysql


def get_production_items(product_id):
    # MySQL 연결 설정
    config = {
        'user': 'admin', # os.environ["user"],
        'password': '0}7(fwXLF[S0TI:BucRP{vOy$n$7',# os.environ["password"],
        'host': 'intern-rds-2.coxwo6u60is7.ap-northeast-2.rds.amazonaws.com',# os.environ["host"],
        'database': 'mydb'# os.environ["db"]
    }
        # MySQL 연결
    connection = pymysql.connect(user=config['user'],
                                password=config['password'],
                                host=config['host'],
                                database=config['database'],
                                charset="utf8")
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
    finally:
        connection.close()
    
personalize_runtime = boto3.client('personalize-runtime')  # 필요에 따라 region 설정

response = personalize_runtime.get_recommendations(
    campaignArn='arn:aws:personalize:ap-northeast-2:634371522187:campaign/intern-campaign',
    userId='rlwjddl1596@naver.com'
)

result = []

for i in response['itemList'][:8]:
    for x in get_production_items(i['itemId']):
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

print(json.dumps(result, default=str, ensure_ascii=False))
# return {
#     'statusCode': 200,
#     'body': json.dumps(result, default=str)  # Convert rows to JSON
# }
