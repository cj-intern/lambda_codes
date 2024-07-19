import pandas as pd
import time
import numpy as np
# 사용자 데이터 로드
user_csv_path = '/home/whatup/lambda/csvs/user_with_numeric_attributes.csv'
product_csv_path = '/home/whatup/lambda/csvs/final.csv'

user_df = pd.read_csv(user_csv_path)
product_df = pd.read_csv(product_csv_path)

# 상호작용 데이터 생성
interaction_data = []

event_type = []
for _, user in user_df.iterrows():
    for _, product in product_df.iterrows():
        # 조건 1: SKIN_TYPE과 MOISTURE
        condition1 = user['SKIN_TYPE'] >= 1 and product['MOISTURE'] < 5
        condition7 = user['SKIN_TYPE'] < 1 and product['MOISTURE'] >= 5
        # 조건 2: SENSITIVE
        condition2 = user['SENSITIVE'] == product['SENSITIVE_SKIN']
        # 조건 3: ACNE와 ACNE_CARE
        condition3 = user['ACNE'] == 1 and product['ACNE_CARE'] == 1
        # 조건 4: SKIN_TONE과 WHITENING
        condition4 = user['SKIN_TONE'] == 2 and product['CATEGORY_L1'] == "YES"
        # 조건 5: AGE와 WRINKLE_CARE
        condition5 = user['AGE'] > 26 and product['WRINKLE_CARE'] == 1
        # 조건 6: ACNE 또는 나이가 적을 때 ACNE_CARE
        condition6 = (user['ACNE'] == 1 or user['AGE'] < 25) and product['ACNE_CARE'] == 1
        
        cnt = 0
        if condition1:
            cnt += 1
        if condition2:
            cnt += 1
        if condition3:
            cnt += 1
        if condition4:
            cnt += 1
        if condition5:
            cnt += 1
        if condition6:
            cnt += 1
        if condition7:
            cnt += 1
        if cnt > 5:
            interaction_data.append([user['USER_ID'], product['ITEM_ID']])
            event_type.append('PURCHASE')
        elif cnt > 4:
            interaction_data.append([user['USER_ID'], product['ITEM_ID']])
            event_type.append('VIEW')
        elif cnt > 3:
            interaction_data.append([user['USER_ID'], product['ITEM_ID']])
            event_type.append('CLICK')

for i in range(len(event_type)):
    interaction_data[i].append(event_type[i])

# 상호작용 데이터 프레임 생성
interaction_df = pd.DataFrame(interaction_data, columns=['USER_ID', 'ITEM_ID', 'EVENT_TYPE'])

# 새로운 CSV 파일로 저장
interaction_csv_path = 'interaction.csv'
interaction_df.to_csv(interaction_csv_path, index=False, encoding='utf-8-sig')

print(f"Interaction data saved to {interaction_csv_path}")
