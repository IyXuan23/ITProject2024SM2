"""
This file contains script to import scraped data to "subjects" table.
"""
import glob
import json
import os
import psycopg2
from utils import clean_lines


# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres.seqkcnapvgkwqbqipqqs",
                        password="IT Web Server12", host="aws-0-ap-southeast-2.pooler.supabase.com", port=6543)
cur = conn.cursor()
cur.execute("""TRUNCATE TABLE electives CASCADE;""")

subject_path = 'subjectInfo'
course_path = 'courseInfo'

# Open file and load subject['further info']['Breadth options'] from file
for file_path in glob.glob(os.path.join(course_path, '*.json')):
    with open(file_path) as file:
        data = json.load(file)
    
    # Get subject breadth info from file
    course_code = data['Course code']
    electives_struct = None

    # For debugging
    print("Importing data for " + course_code)

    course_structure = data['Course Structure']
    if course_code.startswith('B-'):
        for info_key,info_value in course_structure.items():
            if 'electives' in info_key.lower():
                electives_struct = json.dumps(clean_lines(info_value))
                break


            for sub_info_key,sub_info_value in course_structure['Course structure'].items():
                if 'electives' in sub_info_key.lower():
                    electives_struct = json.dumps(clean_lines(sub_info_value))
                
                if 'subject options' in sub_info_key.lower():
                    subject_options = 'Subject options' if 'Subject options' in course_structure['Course structure'] else 'Subject Options'
                    for key,value in course_structure['Course structure'][subject_options].items():
                        if 'electives' in key.lower():
                            electives_struct = json.dumps(clean_lines(value))
                            break
            
                if 'discipline subjects' in sub_info_key.lower():
                    electives_struct = json.dumps(clean_lines(sub_info_value))

    # Insert information from file to table for each semester
    cur.execute("""
                INSERT INTO electives(course_code,electives_structure)
                VALUES (%s,%s)
                 """
                ,(course_code, electives_struct))
    
#Commit the transaction    
conn.commit()

#Close the cursor
cur.close()
conn.close()
print("--------SUCCEED IN IMPORTING DATA!-----------\n")
    