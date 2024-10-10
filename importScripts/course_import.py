"""
This file contains script to import scraped data to "courses" table.
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
cur.execute("""TRUNCATE TABLE courses CASCADE;""")

folder_path = 'courseInfo'

# Open file and load data from file
for file_path in glob.glob(os.path.join(folder_path, '*.json')):
    with open(file_path) as file:
        data = json.load(file)
    
    
    # Get course name from file
    course_title = data ['Course name']

    # Get course code from file
    course_code = data ['Course code']

    # Get course overview from file
    overview_extracted = data ['Overview text'] if 'Overview text' in data else None 
    if overview_extracted is not None:
        overview_text = convert_list_into_text(overview_extracted)
    
    # For debugging
    print("Importing data for: " + course_code + "(" + course_title + ")")
    
    overview_table = data ['Overview table']
    # Informations from 'Overview table'
    award_title = overview_table['Award title'] if 'Award title' in overview_table else None
    start_year = int(overview_table['Year & campus'][0:4])
    location = overview_table['Year & campus'][6:]
    crisco = overview_table['CRICOS code'] if 'CRICOS code' in overview_table else None
    fees_information = overview_table['Fees information']
    study_level = overview_table['Study level & type']
    aqf_level = overview_table['AQFlevel'] if 'AQFlevel' in overview_table else None
    credit_points = overview_table['Credit points'] if 'Credit points' in overview_table else None
    duration = overview_table['Duration']
    


    course_structure = data.get("Course Structure", {})
    course_structure_clean = json.dumps(clean_lines(course_structure))

    requirements = data['Entry and participation requirements']
    entry_requirements = json.dumps(clean_lines(requirements['Entry requirements'])) if 'Entry requirements' in requirements else None
    inherent_requirements = json.dumps(clean_lines(requirements['Inherent requirements (core participation requirements)']))
    attributes = convert_dict_to_text(data['Attribute, outcomes and skills'])

            

    # Insert information from file to table
    cur.execute("""
        INSERT INTO courses(aqf_level, credit_points, crisco, duration, fees_information, location, start_year, 
                            study_level, course_structure, inherent_requirements, entry_requirements, 
                            attributes_outcomes_skills, course_code, course_name)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (course_code) DO NOTHING """
        ,(aqf_level, credit_points, crisco, duration, fees_information, location, start_year,
          study_level, course_structure_clean, inherent_requirements, entry_requirements, attributes, 
          course_code, course_title))
    
            
    
#Commit the transaction    
conn.commit()

#Close the cursor
cur.close()
conn.close()

print("--------SUCCEED IN IMPORTING DATA!-----------\n")
  