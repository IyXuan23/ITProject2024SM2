import csv

def load_subjects(csv_path='./subject_info.csv'):
    """
    Load subject information from a CSV file.
    :param csv_path: Path to the subject CSV file.
    :return: Dictionary of subjects with subject codes as keys.
    """
    subjects = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            subject_code = row.get("subject code")
            if subject_code:
                subjects[subject_code] = row
    return subjects

def load_majors(csv_path='./major_info.csv'):
    """
    Load major information from a CSV file.
    :param csv_path: Path to the major CSV file.
    :return: Dictionary of majors with major names as keys.
    """
    majors = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            major_name = row.get("major name")
            if major_name:
                majors[major_name] = row
    return majors

def load_courses(csv_path='./course_info.csv'):
    """
    Load course information from a CSV file.
    :param csv_path: Path to the course CSV file.
    :return: Dictionary of courses with course names as keys.
    """
    courses = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            course_name = row.get("course code")
            if course_name:
                courses[course_name] = row
    return courses