"""
This file contains script to import scraped data to "subjects" table.
"""
import glob
import json
import os
import psycopg2


# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres.seqkcnapvgkwqbqipqqs",
                        password="IT Web Server12", host="aws-0-ap-southeast-2.pooler.supabase.com", port=6543)
cur = conn.cursor()
cur.execute("""TRUNCATE TABLE subjects CASCADE;""")

folder_path = 'subjectInfo'

# Open file and load data from file
for file_path in glob.glob(os.path.join(folder_path, '*.json')):
    with open(file_path) as file:
        data = json.load(file)
    
    
    # Get subject related info from file
    subject_code = data['subject code']
    subject_name = data['subject name']
    subject_level = int(subject_code[4])

    content = data.get('indicative content', [])
    if not isinstance(content, list):
        content = []

    aims = data.get('aims', [])
    if not isinstance(aims, list):
        aims = []

    #Insert information from file to table
    cur.execute("""
                INSERT INTO subjects(subject_code, subject_name, aims, indicative_content, subject_level)
                VALUES (%s,%s,%s,%s,%s)
                ON CONFLICT (subject_code) DO NOTHING """
                ,(subject_code, subject_name, aims, content, subject_level))
    
#Commit the transaction    
conn.commit()

#Close the cursor
cur.close()
conn.close()
    