"""
This file contains script to import scraped data to "subjects" table.
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

    for sem_info in data['dates and times']:
        for sem, details in sem_info.items():
            for detail in details:
                for key, value in detail.items():
                    if key == 'Principal coordinator':
                        p_coordinator = value
                    elif key == 'Mode of delivery':
                        delivery_mode = [value]
                    elif key == 'Contact hours':
                        contact_hours = value
                    elif key == 'Total time commitment':
                        total_time_string = value
                        hours = int(total_time_string.split()[0])
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

            #Insert information from file to table
            cur.execute("""
                INSERT INTO subjects(subject_code, subject_name, aims, indicative_content, subject_level,
                        semester, principal_coordinator, delivery_mode, contact_hours, teaching_period,
                        total_time_commitement, last_self_enrol_date, census_date, last_date_to_withdraw_without_fail,
                        assessment_period_ends)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (subject_code) DO NOTHING """
                ,(subject_code, subject_name, aims, content, subject_level, sem, p_coordinator, delivery_mode,
                  contact_hours, teaching_period, hours, last_self_enrol, census, last_date_withdraw, assessment_end))
    
#Commit the transaction    
conn.commit()

#Close the cursor
cur.close()
conn.close()
    