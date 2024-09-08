"""
This file contains script to import scraped data to "subject_info" table.
"""
import glob
import json
import os
import psycopg2
from utils import copy_random_files, copy_specific_file, convert_list_into_text



# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres.seqkcnapvgkwqbqipqqs",
                        password="IT Web Server12", host="aws-0-ap-southeast-2.pooler.supabase.com", port=6543)
cur = conn.cursor()
cur.execute("""TRUNCATE TABLE prerequisite_options CASCADE;""")

folder_path = 'subjectInfo'

# For debugging, more info in utils.py
"copy_random_files('subjectInfo','subjectInfoTest',10)"

# Open file and load data from file
for file_path in glob.glob(os.path.join(folder_path, '*.json')):
    with open(file_path) as file:
        data = json.load(file)
    
    
    # Get subject code from file
    subject_code = data['subject code']

    # For debugging
    print("Importing data for " + subject_code)

    # Loop over each option in "pre-requisite"
    for prerequisite_option in data['pre-requisites']:
        
        option = prerequisite_option['option']
        one_of_list = prerequisite_option['one of pre-requisite']
        nec = prerequisite_option['necessary pre-requisite']
        alt = prerequisite_option['alternate pre-requisite'] if 'alternate pre-requisite' in prerequisite_option else None
        add = prerequisite_option['additional pre-requisite'] if 'additional pre-requisite' in prerequisite_option else None
        #print("Option_num is " + option)

        one_of = []
        necessary = []
        alternate = convert_list_into_text(alt)
        addtional = convert_list_into_text(add)
        
        if one_of_list != None:
            for elt in one_of_list:
                if isinstance(elt,list): one_of.extend(elt)
                else: one_of.append(elt)
        
        for counter, n in enumerate(nec):
            if isinstance(n,list):
                if (counter > 0) and (isinstance(nec[counter-1],str)) and ('the following' in nec[counter-1] or ('The following' in nec[counter-1])):
                    sub_list = []
                    necessary.pop(len(necessary)-1)
                    header = nec[counter-1]
                    sub_list.append(header)
                    sub_list.append(n)
                    sub_text = convert_list_into_text(sub_list)
                    necessary.append(sub_text)
                else:
                    necessary.extend(n)
                continue
            necessary.append(n)
            





        # Insert information from file to table for each prerequisite option
        cur.execute("""
            INSERT INTO prerequisite_options(option, subject_code, one_of_prerequisite, necessary_prerequisite, 
                    alternate_requirements, additional_requirement)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (option, subject_code) DO NOTHING
            """, (option, subject_code, one_of, necessary, alternate, addtional))
            
   
#Commit the transaction    
conn.commit()

#Close the cursor
cur.close()
conn.close()

print("--------SUCCEED IN IMPORTING DATA!-----------\n")    