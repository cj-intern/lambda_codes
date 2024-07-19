import pandas as pd

# Load the CSV file
file_path = '/home/whatup/lambda/bill/event_history.csv'


data = pd.read_csv(file_path)

# Group by 'User name' and 'Event name' and count occurrences, ensuring all users are included
event_counts = data.groupby(['User name', 'Event name'], as_index=False).size()

# Pivot the data to get a table with users as rows and event names as columns
event_counts_pivot = event_counts.pivot_table(index='User name', columns='Event name', values='size', fill_value=0)

# Ensure all columns are displayed
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

f = open("./tmp.txt", "w")
# Display the result
f.write(str(event_counts_pivot))
f.close()
print(event_counts_pivot)