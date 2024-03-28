import sqlite3
import os

# Path to the database
db_path = 'cleandataset.db'
output_folder = 'simulations/stu_subs'

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Function to fetch 100 contents from the 'content' column of the 'CodeState' table
def fetch_content(CodeSate):
    cursor.execute(f"SELECT Contents FROM {CodeSate} LIMIT 50;")
    return cursor.fetchall()

# Fetch the content from the 'CodeState' table
submissions = fetch_content('CodeState')

# Write the content to a seperate .py files
for i, submission in enumerate(submissions):
    with open(f'{output_folder}/sub_{i+1}.py', 'w') as f:
        f.write(submission[0])

# Close the database connection
conn.close()
