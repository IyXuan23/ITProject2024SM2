"""
This file contains script to import scraped data to "subject_info" table.
"""
import glob
import json
import os
import psycopg2
from utils import convert_to_daterange, convert_to_date, convert_listdict_to_list


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

    # For debugging
    print("Importing data for " + subject_code)
    
    # Initialize variables to store informations from 'further info'
    subject_texts = None
    subject_notes = None
    subject_ses = None
    subject_cap = None

    # Collect info from each section in 'further info'
    texts = data['further info']['Texts']
    notes = None
    if 'subject notes' in data['further info']:
        notes = data['further info']['subject notes']
    if 'Subject notes' in data['further info']:
        notes = data['further info']['Subject notes']
    cap = data['further info']['Available through the Community Access Program'] if 'Available through the Community Access Program' in data['further info'] else None
    ses = data['further info']['Available to Study Abroad and/or Study Exchange Students'] if 'Available to Study Abroad and/or Study Exchange Students' in data['further info'] else None


    # Reformat the info obtained from each section in 'further info' into appropriate data type.
    subject_texts = convert_listdict_to_list(texts)
    all_notes = []
    if notes != None:
        for note in notes:
            if isinstance(note,dict):
                all_notes = convert_listdict_to_list(notes)
                break
            if (note not in ['LEARNING AND TEACHING METHODS', 'INDICATIVE KEY LEARNING RESOURCES', 'CAREERS / INDUSTRY LINKS']) & (not isinstance(note,list)):
                all_notes.append(note)
            if isinstance(note,list):
                for elt in note:
                    elt = elt + '; '
                    all_notes.append(elt)
        subject_notes = ' '.join(all_notes)
    if cap != None:
        converted_cap = convert_listdict_to_list(cap)
        subject_cap = ' '.join(converted_cap)        
    if ses != None:
        subject_ses = '. '.join(ses)
        
    

    # Collect and import info in "dates and times"
    for sem_info in data['dates and times']:
        for sem, details in sem_info.items():
            
            # Initialize variables
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
                    if key == 'Principal coordinator' or key == 'Coordinator':
                        p_coordinator = value
                    elif key == 'Mode of delivery':
                        delivery_mode = value
                    elif key == 'Contact hours':
                        contact_hours = value
                    elif key == 'Total time commitment':
                        total_time_string = value
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
            
            # Collect and import contact emails
            for contact_info in data['contact information']:
                if sem in contact_info:
                    emails = contact_info[sem]['email']
                else:
                    break
            
            
            
            # Insert information from file to table for each semester
            cur.execute("""
                INSERT INTO subject_info(subject_code, semester, principal_coordinator, delivery_mode, contact_hours, 
                        teaching_period, total_time_commitment, last_self_enrol_date, census_date, 
                        last_date_to_withdraw_without_fail, assessment_period_ends, contact_information, 
                        subject_texts, subject_notes, community_access_program, oversea_study_program)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (subject_code,semester) DO NOTHING """
                ,(subject_code, sem, p_coordinator, delivery_mode,
                  contact_hours, teaching_period, hours, last_self_enrol, census, last_date_withdraw, assessment_end, emails,
                  subject_texts, subject_notes, subject_cap, subject_ses 
                ))
    
            
    
#Commit the transaction    
conn.commit()

#Close the cursor
cur.close()
conn.close()

print("--------SUCCEED IN IMPORTING DATA!-----------\n")
  