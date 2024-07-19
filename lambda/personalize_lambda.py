import boto3
import os
import json
import pymysql


def get_production_items(product_id):
    # MySQL 연결 설정
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
        personalize_runtime = boto3.client('personalize-runtime',
                                        aws_access_key_id="AKIAZHM35H2F4KTF2I4L",
                                        aws_secret_access_key="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",
                                        region_name='ap-northeast-2'  # 필요에 따라 region 설정
                                        )
        print("connect start")
        response = personalize_runtime.get_recommendations(
            campaignArn='arn:aws:personalize:ap-northeast-2:634371522187:campaign/intern-campaign',
            userId=id 
        )
        print(response)
        print("done")
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

        return{
            'statusCode': 200,
            "headers": {
            "Access-Control-Allow-Origin": "*",  # Allow all origins
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",  # Allow specific methods
            "Access-Control-Allow-Headers": "Content-Type"  # Allow specific headers
            },
            'body': json.dumps(result, default=str, ensure_ascii=False)
        }
                
