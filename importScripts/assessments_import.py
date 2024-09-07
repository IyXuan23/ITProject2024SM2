"""
This file contains script to import scraped data to "subject_info" table.
"""
import glob
import json
import os
import psycopg2


# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres.seqkcnapvgkwqbqipqqs",
                        password="IT Web Server12", host="aws-0-ap-southeast-2.pooler.supabase.com", port=6543)
cur = conn.cursor()
cur.execute("""TRUNCATE TABLE assessments CASCADE;""")

folder_path = 'subjectInfo'

# Open file and load data from file
for file_path in glob.glob(os.path.join(folder_path, '*.json')):
    with open(file_path) as file:
        data = json.load(file)
    
    
    # Get subject code from file
    subject_code = data['subject code']

    # Extract assessments info
    assessments = data['assessments']

    # For debugging
    print("Importing data for " + subject_code)
    
    # Initialize variables to store informations from 'assessments'
    description = None
    timing = None 
    percentage = None

    # Collect and import info in "assessments" if available
    if assessments != None:
        for info in assessments:
            description = info ['description']
            timing = info ['timing']
            percentage = info['percentage']
            
            # Insert information from file to table for each assessment
            cur.execute("""
                INSERT INTO assessments(subject_code,description,timing,percentage)
                VALUES (%s,%s,%s,%s)
                """
                ,(subject_code, description, timing, percentage))
    
            
    
#Commit the transaction    
conn.commit()

#Close the cursor
cur.close()
conn.close()

print("--------SUCCEED IN IMPORTING DATA!-----------\n")
    