import pandas as pd
import random
from faker import Faker

# Initialize Faker
fake = Faker('ko_KR')

# Load the provided user CSV file
user_df = pd.read_csv('/home/whatup/lambda/random_gen/user.csv')

# Function to generate random user data
def generate_random_user_data(num_users, existing_user_ids):
    random_user_data = []
    while len(random_user_data) < num_users:
        user_id = fake.email()
        if user_id not in existing_user_ids:
            random_user_data.append([
                user_id,
                fake.name(),
                random.choice(['Male', 'Female']),
                random.choice(['Dry', 'Oily', 'Combination']),
                random.choice(['Yes', 'No']),
                random.choice(['Yes', 'No']),
                random.choice(['Fair', 'Medium', 'Dark']),
                random.randint(18, 60)
            ])
            existing_user_ids.add(user_id)
    return pd.DataFrame(random_user_data, columns=['USER_ID', 'USER_NAME', 'GENDER', 'SKIN_TYPE', 'SENSITIVE', 'ACNE', 'SKIN_TONE', 'AGE'])

# Generate 27 random users
existing_user_ids = set(user_df['USER_ID'])
random_user_df = generate_random_user_data(27, existing_user_ids)

# Combine the existing users with the newly generated users
combined_user_df = pd.concat([user_df, random_user_df], ignore_index=True)

# Save the combined user data to a CSV file (UTF-8 encoding)
output_path = 'combined_user_data_utf8.csv'
combined_user_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"Combined user data saved to {output_path}")
