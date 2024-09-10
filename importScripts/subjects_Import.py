"""
This file contains script to import scraped data to "subjects" table.
"""
import glob
import json
import os
import psycopg2
from utils import convert_list_into_text


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

    # For debugging
    print("Importing data for " + subject_code)

    content = data.get('indicative content', [])
    if not isinstance(content, list):
        content = []
    else: 
        content_import = convert_list_into_text(content)
        
    aims = data.get('aims', [])
    if not isinstance(aims, list):
        aims = []
    else:
        aims_import = convert_list_into_text(aims)

    learning_outcomes = data.get('intended learning outcomes', [])
    if not isinstance(learning_outcomes, list):
        learning_outcomes = []
    else:
        learning_outcomes_import = convert_list_into_text(learning_outcomes)

    overview = data.get('overview',[])
    if not isinstance(overview,list):
        overview = []
    else:
        overview_import = convert_list_into_text(overview)

    print(overview_import)

            
    # Insert information from file to table for each semester
    cur.execute("""
                INSERT INTO subjects(subject_code, subject_name, aims, indicative_content,subject_level,learning_outcomes,overview)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (subject_code) DO NOTHING """
                ,(subject_code, subject_name, aims_import, content_import, subject_level, learning_outcomes_import,overview_import))
    
#Commit the transaction    
conn.commit()

#Close the cursor
cur.close()
conn.close()
print("--------SUCCEED IN IMPORTING DATA!-----------\n")
    