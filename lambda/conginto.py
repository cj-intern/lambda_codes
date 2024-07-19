import os
import json
import pymysql

def insert_into_rds(id, email, name):

    # MySQL 연결 설정
    config = {
        'user': os.environ["user"],
        'password': os.environ["password"],
        'host': os.environ["host"],
        'database': os.environ["db"]
    }

    try:
        # MySQL 연결
        connection = pymysql.connect(user=config['user'],
                                    password=config['password'],
                                    host=config['host'],
                                    database=config['database'])

        cursor = connection.cursor()

        # 삽입할 데이터 정의
        add_data = "INSERT INTO users (user_id, user_email, user_name) VALUES (%s, %s, %s)"
        data = (id, email, name)

        # 데이터 삽입
        cursor.execute(add_data, data)

        # 변경사항 커밋
        connection.commit()

        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
        return "Data inserted successfully!"

    except pymysql.MySQLError as e:
        return f"Error: {e}"

def lambda_handler(event, context):
    user_data = event["request"]["userAttributes"]
    id = user_data["email"]
    email = user_data["email"]
    name = user_data["name"]
    print(insert_into_rds(id, email, name))
    event["response"] = "Login succeeded"
    return event