import glob
import json
import os
import psycopg2

# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres.seqkcnapvgkwqbqipqqs",
                        password="IT Web Server12", host="aws-0-ap-southeast-2.pooler.supabase.com", port=6543)
cur = conn.cursor()
cur.execute("""TRUNCATE TABLE course CASCADE;""")

folder_path = 'course'

for file_path in glob.glob(os.path.join(folder_path, '*.json')):
    with open(file_path) as file:
        data = json.load(file)

    # Convert the list of indicative content into a string
    overview = data['Overview text']
    if isinstance(data['Overview text'], list):
        overview = ' '.join([item + ';' for item in data['Overview text']])

    if "Entry and participation requirements" in data and data["Entry and participation requirements"]:
        if ("Entry requirements" in data["Entry and participation requirements"] and
                data["Entry and participation requirements"]["Entry requirements"]):
            entry_requirements = data["Entry and participation requirements"]["Entry requirements"]
            if isinstance(data["Entry and participation requirements"]['Entry requirements'], list):
                entry_requirements = ' '.join([item + ';' for item in
                                               data["Entry and participation requirements"]['Entry requirements']])
        if ("Inherent requirements (core participation requirements)" in data["Entry and participation requirements"]
                and data["Entry and participation requirements"]
                ["Inherent requirements (core participation requirements)"]):
            inherent_requirements = (
                data)["Entry and participation requirements"]["Inherent requirements (core participation requirements)"]
            if isinstance(data["Entry and participation requirements"]
                          ["Inherent requirements (core participation requirements)"], list):
                inherent_requirements = ' '.join([item + ';' for item in data["Entry and participation requirements"]
                ["Inherent requirements (core participation requirements)"]])
    professional_accreditation = ""
    if "Attribute, outcomes and skills" in data and data["Attribute, outcomes and skills"]:
        if ("Professional accreditation" in data["Attribute, outcomes and skills"] and
                data["Attribute, outcomes and skills"]["Professional accreditation"]):
            professional_accreditation = data["Attribute, outcomes and skills"]["Professional accreditation"]
            if isinstance(data["Attribute, outcomes and skills"]["Professional accreditation"], list):
                professional_accreditation = ' '.join([item + ';' for item in data["Attribute, outcomes and skills"]
                ["Professional accreditation"]])

    if "Award title" in data['Overview table'] and data['Overview table']['Award title']:
        award_title = data['Overview table']["Award title"]
    if "Year & campus" in data['Overview table'] and data['Overview table']['Year & campus']:
        year_campus = data['Overview table']["Year & campus"]
    if "CRICOS code" in data['Overview table'] and data['Overview table']['CRICOS code']:
        CRICOS = data['Overview table']["CRICOS code"]
    if "Fees information" in data['Overview table'] and data['Overview table']['Fees information']:
        fees_information = data['Overview table']["Fees information"]
    if "Duration" in data['Overview table'] and data['Overview table']['Duration']:
        duration = data['Overview table']["Duration"]
    if "Credit points" in data['Overview table'] and data['Overview table']['Credit points']:
        credit_points = data['Overview table']["Credit points"]
    if "Study level & type" in data['Overview table'] and data['Overview table']['Study level & type']:
        study_level_type = data['Overview table']['Study level & type']
    if "AQFlevel" in data['Overview table'] and data['Overview table']['AQFlevel']:
        aqf_level = data['Overview table']['AQFlevel']

    if "Further Study" in data and data["Further Study"]:
        further_study = data["Further Study"]
        if isinstance(data["Further Study"], list):
            further_study = ' '.join([item + ';' for item in data["Further Study"]])

    # Insert subject data into the database
    cur.execute("""
        INSERT INTO course (course_id, aqf_level, credit_point, crisco, duration, fees_information, location, 
        entry_requirements, study_level, learning_outcomes, overview, start_year)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (course_id) DO NOTHING
    """, (
        award_title, aqf_level, credit_points.split(" ")[0], CRICOS, duration, fees_information,
        year_campus.split("— ")[1], entry_requirements, study_level_type, professional_accreditation,
        overview, year_campus.split("— ")[0]
    ))

conn.commit()
# Closed communication
cur.close()
conn.close()
print("Data imported successfully!")
