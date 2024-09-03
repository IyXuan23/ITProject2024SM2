import glob
import json
import os
import psycopg2

# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres.seqkcnapvgkwqbqipqqs",
                        password="IT Web Server12", host="aws-0-ap-southeast-2.pooler.supabase.com", port=6543)
cur = conn.cursor()
cur.execute("""TRUNCATE TABLE subject, assessments, neccessary_prerequisite, non_allowed_subject, one_of_prerequisite,
 prerequisite_options CASCADE;""")

folder_path = 'subject'

for file_path in glob.glob(os.path.join(folder_path, '*.json')):
    with open(file_path) as file:
        data = json.load(file)

    # Convert the list of indicative content into a string
    result = data['indicative content']
    if isinstance(data['indicative content'], list):
        result = ' '.join([item + ';' for item in data['indicative content']])

    aims = data['aims']
    if isinstance(data['aims'], list):
        aims = ' '.join([item + ';' for item in data['aims']])

    # Insert subject data into the database
    cur.execute("""
        INSERT INTO subject (subject_code, subject_name, aims, indicative_contents)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (subject_code) DO NOTHING
    """, (
        data['subject code'],
        data['subject name'],
        aims,
        result
    ))

    # # Insert subject availability data into the database
    # for semester in data['subject availability']:
    #     cur.execute("""
    #         INSERT INTO availability (subject_code, semester)
    #         VALUES (%s, %s)
    #     """, (
    #         data['subject code'],
    #         semester
    #     ))

    # for non_allowed_subject in data.get("non-allowed subjects", []):
    #     print(non_allowed_subject,data['subject code'])
    #     cur.execute("""
    #                 INSERT INTO non_allowed_subject (subject_code, non_allowed_subject_code, description)
    #                 VALUES (%s, %s, %s)
    #                 ON CONFLICT DO NOTHING;
    #             """, (data['subject code'], non_allowed_subject, non_allowed_subject))

    # if 'one of pre-requisite' in data:
    #     for prereq in data['one of pre-requisite']:
    #         cur.execute("""
    #             INSERT INTO prerequisites (subject_code, one_of_prerequisite)
    #             VALUES (%s, %s)
    #         """, (
    #             data['subject code'],
    #             prereq
    #         ))
    #
    # if 'alternate pre-requisite' in data:
    #     for prereq in data['alternate pre-requisite']:
    #         cur.execute("""
    #             INSERT INTO prerequisites (subject_code, alternate_prerequisite)
    #             VALUES (%s, %s)
    #         """, (
    #             data['subject code'],
    #             prereq
    #         ))
    #
    for assessment in data['assessments']:
        cur.execute("""
                INSERT INTO assessments (subject_code, description, timing, percentage)
                VALUES (%s, %s, %s, %s)
            """, (
                    data['subject code'],
                    assessment['description'],
                    assessment['timing'],
                    assessment['percentage']
                    ))
    #
    # if isinstance(data['contact information'][0], str) and len(data['contact information']) == 2:
    #     cur.execute("""
    #                     INSERT INTO contact_info (subject_code, name, email)
    #                     VALUES (%s, %s, %s)
    #                 """, (
    #         data['subject code'],
    #         data['contact information'][0],
    #         data['contact information'][1]
    #         ))
    # else:
    #     for contact in data['contact information']:
    #         # Handle Case there's semester in contact information
    #         for semester, info in contact.items():
    #             names = info.get('name', [])
    #             emails = info.get('email', [])
    #             for name, email in zip(names, emails):
    #                 cur.execute("""
    #                                INSERT INTO contact_info (subject_code, semester, name, email)
    #                                VALUES (%s, %s, %s, %s)
    #                            """, (
    #                     data['subject code'],
    #                     semester,
    #                     name if name else 'Unknown',
    #                     email
    #                 ))
    #
    # for case in data['dates and times']:
    #     for semester, info in case.items():
    #         principal_coordinator = None
    #         coordinator = None
    #         mode_of_delivery = None
    #         contact_hours = None
    #         total_time_commitment = None
    #         teaching_period = None
    #         last_self_enrol_date = None
    #         census_date = None
    #         last_day_to_withdraw_without_fail = None
    #         assessment_period_ends = None
    #
    #         for item in info:
    #             if 'Principal coordinator' in item:
    #                 principal_coordinator = item['Principal coordinator']
    #             elif 'Coordinator' in item:
    #                 coordinator = item['Coordinator']
    #             elif 'Mode of delivery' in item:
    #                 mode_of_delivery = item['Mode of delivery']
    #             elif 'Contact hours' in item:
    #                 contact_hours = item['Contact hours']
    #             elif 'Total time commitment' in item:
    #                 total_time_commitment = item['Total time commitment']
    #             elif 'Teaching period' in item:
    #                 teaching_period = item['Teaching period']
    #             elif 'Last self-enrol date' in item:
    #                 last_self_enrol_date = item['Last self-enrol date']
    #             elif 'Census date' in item:
    #                 census_date = item['Census date']
    #             elif 'Last date to withdraw without fail' in item:
    #                 last_day_to_withdraw_without_fail = item['Last date to withdraw without fail']
    #             elif 'Assessment period ends' in item:
    #                 assessment_period_ends = item['Assessment period ends']
    #         cur.execute("""
    #             INSERT INTO subject_info (subject_code, semester, principal_coordinator, coordinator,
    #             delivery_mode, contact_hours, total_time_commitment, teaching_period,
    #             last_self_enrol_date, census_date, last_date_to_withdraw_without_fail, assessment_period_end)
    #             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    #             """, (
    #             data['subject code'],
    #             semester,
    #             principal_coordinator,
    #             coordinator,
    #             mode_of_delivery,
    #             contact_hours,
    #             total_time_commitment,
    #             teaching_period,
    #             last_self_enrol_date,
    #             census_date,
    #             last_day_to_withdraw_without_fail,
    #             assessment_period_ends
    #         ))


conn.commit()
# Closed communication
cur.close()
conn.close()
print("Data imported successfully!")
