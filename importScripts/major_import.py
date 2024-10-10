"""
This file contains script to import scraped data to "majors" table.
"""
import glob
import json
import os
import psycopg2
from utils import *



# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres.seqkcnapvgkwqbqipqqs",
                        password="IT Web Server12", host="aws-0-ap-southeast-2.pooler.supabase.com", port=6543)
cur = conn.cursor()
cur.execute("""TRUNCATE TABLE majors CASCADE;""")

folder_path = 'majorInfo'


# Open file and load data from file
for file_path in glob.glob(os.path.join(folder_path, '*.json')):
    if file_path != 'courseMajorPairing.json':
        with open(file_path) as file:
            data = json.load(file)

            with open ('courseMajorPairing.json') as pairing_file:
                pairing_data = json.load(pairing_file)
                
                # Get subject code from file
                major_name = data['major name']

                course_name = None
                for info in pairing_data:
                    if major_name in info:
                        course_name = info[0]

                # For debugging
                print("Importing data for " + major_name)

                overview = convert_list_into_text(data['overview'])
                ILOs = data['ILOs']
                structure = json.dumps(data['structure'])

                # Insert information from file to table for each prerequisite option
                cur.execute("""
                    INSERT INTO majors(overview,learning_outcomes,course_code,major_name,major_structure)
                        VALUES (%s, %s, %s, %s, %s)""", 
                        (overview,ILOs,course_code,major_name,structure))
                
   
#Commit the transaction    
conn.commit()

#Close the cursor
cur.close()
conn.close()

print("--------SUCCEED IN IMPORTING DATA!-----------\n")    