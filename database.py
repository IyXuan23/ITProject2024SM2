import os
import json

def load_subjects(json_dir='./subjectinfo'):
    """
    Load subject information from JSON files in the given directory.
    :param json_dir: Directory containing subject JSON files.
    :return: Dictionary of subjects with subject codes as keys.
    """
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

def load_majors(json_dir='./majorInfo'):
    """
    Load major information from JSON files in the given directory.
    :param json_dir: Directory containing major JSON files.
    :return: Dictionary of majors with major names as keys.
    """
    majors = {}
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(json_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Check if data is a list
                if isinstance(data, list):
                    for major_data in data:
                        # Ensure each entry in the list is a dictionary
                        if isinstance(major_data, dict):
                            major_name = major_data.get("major name")
                            if major_name:
                                majors[major_name] = major_data
                elif isinstance(data, dict):
                    major_name = data.get("major name")
                    if major_name:
                        majors[major_name] = data
    return majors

def load_courses(json_dir='./courseInfo'):
    """
    Load course information from JSON files in the given directory.
    :param json_dir: Directory containing course JSON files.
    :return: Dictionary of courses with course names as keys.
    """
    courses = {}
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(json_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                course_data = json.load(f)
                course_name = course_data.get("Course name")
                if course_name:
                    courses[course_name] = course_data
    return courses
