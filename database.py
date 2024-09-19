import os
import json

def load_subjects(json_dir='./subjectinfo'):
    subjects = {}
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(json_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                subject_data = json.load(f)
                subject_code = subject_data.get("subject code")
                if subject_code:
                    subjects[subject_code] = subject_data
    return subjects
