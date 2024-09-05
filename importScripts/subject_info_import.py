"""
This file contains script to import scraped data to "subject_info" table.
"""
import glob
import json
import os
import psycopg2
from utils import convert_to_daterange, convert_to_date


# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres.seqkcnapvgkwqbqipqqs",
                        password="IT Web Server12", host="aws-0-ap-southeast-2.pooler.supabase.com", port=6543)
cur = conn.cursor()
cur.execute("""TRUNCATE TABLE subject_info CASCADE;""")

folder_path = 'subjectInfo'

# Open file and load data from file
for file_path in glob.glob(os.path.join(folder_path, '*.json')):
    with open(file_path) as file:
        data = json.load(file)
    
    
    # Get subject related info from file
    subject_code = data['subject code']

    # Extract "further info" from the file (if it exists)
    further_info = data['further info']

    # Convert the further info to a JSON string (for storage in the DB)
    further_info_json = json.dumps(further_info)


    # Loop over semesters in "dates and times"
    for sem_info in data['dates and times']:
        for sem, details in sem_info.items():
            
            # Initialize variables to be inserted for this semester
            p_coordinator = None
            delivery_mode = None
            contact_hours = None
            hours = None
            teaching_period = None
            last_self_enrol = None
            census = None
            last_date_withdraw = None
            assessment_end = None

            for detail in details:
                for key, value in detail.items():
                    if key == 'Principal coordinator':
                        p_coordinator = value
                    elif key == 'Mode of delivery':
                        delivery_mode = [value]  # Wrap in a list
                    elif key == 'Contact hours':
                        contact_hours = value
                    elif key == 'Total time commitment':
                        total_time_string = value
                        print(total_time_string)
                        hours = int(total_time_string.split()[0].replace(',', ''))
                    elif key == 'Teaching period':
                        teaching_period = convert_to_daterange(value)
                    elif key == 'Last self-enrol date':
                        last_self_enrol = convert_to_date(value)
                    elif key == 'Census date':
                        census = convert_to_date(value)
                    elif key == 'Last date to withdraw without fail':
                        last_date_withdraw = convert_to_date(value)
                    elif key == 'Assessment period ends':
                        assessment_end = convert_to_date(value)

            # Insert information from file to table for each semester
            cur.execute("""
                INSERT INTO subject_info(subject_code, semester, principal_coordinator, delivery_mode, contact_hours, 
                        teaching_period, total_time_commitment, last_self_enrol_date, census_date, 
                        last_date_to_withdraw_without_fail, assessment_period_ends,further_info)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (subject_code,semester) DO NOTHING """
                ,(subject_code, sem, p_coordinator, delivery_mode,
                  contact_hours, teaching_period, hours, last_self_enrol, census, last_date_withdraw, assessment_end,further_info_json))
    
            
    
#Commit the transaction    
conn.commit()

#Close the cursor
cur.close()
conn.close()
    