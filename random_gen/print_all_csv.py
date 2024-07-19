import pandas as pd
import random
from faker import Faker

# Initialize Faker
fake = Faker('ko_KR')

# Load the provided user CSV file
user_df = pd.read_csv('/home/whatup/lambda/updated_product_reordered.csv')

cnt = 0
for i in range(0, len(user_df['WHITENING'])):
    user_df['WHITENING'][i] = 'YES' if user_df['WHITENING'][i] == 1 else 'No'
    print(user_df['WHITENING'][i])

user_df.to_csv('price.csv', index=False)
