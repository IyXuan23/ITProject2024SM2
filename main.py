import logging
import Levenshtein
import re
from model import ask_gpt_for_keywords
from database import load_subjects, load_majors, load_courses
from fuzzywuzzy import fuzz
from jellyfish import jaro_winkler_similarity

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load subjects, majors, and courses data
subjects = load_subjects()
majors = load_majors()
courses = load_courses()

def clean_input(user_input):
    """
    Clean user input by removing special characters and unnecessary spaces.
    """
    user_input = re.sub(r'[^\w\s]', '', user_input)  # Retain only letters, numbers, and spaces
    return user_input.strip().lower()

def get_best_match(user_input, options):
    """
    Use multiple algorithms (Levenshtein distance, Jaro-Winkler similarity, fuzzy matching) to find the closest match.
    """
    user_input_lower = user_input.lower()
    scores = []

    for option in options:
        option_lower = option.lower()

        # Levenshtein distance
        lev_ratio = Levenshtein.ratio(user_input_lower, option_lower)

        # Jaro-Winkler similarity
        jw_similarity = jaro_winkler_similarity(user_input_lower, option_lower)

        # Fuzzy matching
        fuzz_ratio = fuzz.token_set_ratio(user_input_lower, option_lower) / 100  # Normalize to 0-1

        # Overall score (weights can be adjusted as needed)
        total_score = (lev_ratio + jw_similarity + fuzz_ratio) / 3

        scores.append((option, total_score))

    # Sort by score in descending order
    scores.sort(key=lambda x: x[1], reverse=True)

    # Set similarity threshold
    if scores and scores[0][1] >= 0.7:
        return scores[0][0]
    return None

def correct_query(key_field, key_subject):
    """
    Generate a corrected query statement based on user input for fields, subjects, majors, or courses.
    """
    key_subject_cleaned = clean_input(key_subject)

    # Retrieve all subject names and codes
    all_subject_names = [data['subject name'] for data in subjects.values()]
    all_subject_codes = [subject_code for subject_code in subjects.keys()]

    # Retrieve all major names
    all_major_names = [major_name for major_name in majors.keys()]

    # Retrieve all course names
    all_course_names = [course_name for course_name in courses.keys()]

    # Combine names and codes of subjects, majors, and courses
    all_names = all_subject_names + all_subject_codes + all_major_names + all_course_names

    # Retrieve available fields
    sample_data = next(iter(subjects.values()))
    available_fields = [field for field in sample_data.keys()]

    # Add fields from majors
    if majors:
        sample_major_data = next(iter(majors.values()))
        available_fields += [field for field in sample_major_data.keys()]

    # Add fields from courses
    if courses:
        sample_course_data = next(iter(courses.values()))
        available_fields += [field for field in sample_course_data.keys()]

    available_fields = list(set(available_fields))

    # Match field name
    closest_field = get_best_match(key_field, available_fields)
    if not closest_field:
        closest_field = key_field

    # Match subject/major/course code or name
    closest_subject = get_best_match(key_subject_cleaned, all_names)
    if closest_subject:
        # Check if found in subjects
        for subject_code, data in subjects.items():
            if data['subject name'] == closest_subject or subject_code == closest_subject:
                corrected_subject = data['subject name'] if data['subject name'] == closest_subject else subject_code
                break
        else:
            # Check if found in majors
            for major_name in majors.keys():
                if major_name == closest_subject:
                    corrected_subject = major_name
                    break
            else:
                # Check if found in courses
                for course_name in courses.keys():
                    if course_name == closest_subject:
                        corrected_subject = course_name
                        break
                else:
                    corrected_subject = key_subject
    else:
        corrected_subject = key_subject

    # Return corrected query statement
    return f"Please provide information about {closest_field} for {corrected_subject}."

def main(user_input):
    try:
        # Extract keywords using GPT model
        response = ask_gpt_for_keywords(user_input)
        
        # Validate response format
        if response.count('\n') < 1:
            raise ValueError("Invalid format received from GPT.")

        # Split response into lines
        lines = response.strip().split('\n')
        if len(lines) < 2:
            raise ValueError("Incomplete information received from GPT.")

        key_field = lines[0].replace('Key Field: ', '').strip()
        key_subject = lines[1].replace('Key Subject: ', '').strip()

        # Display extracted field and subject/major/course
        print(f"Key Field: {key_field}")
        print(f"Key Subject: {key_subject}")
        
        # Correct query statement
        corrected_query = correct_query(key_field, key_subject)
        print(f"Corrected Query: {corrected_query}")

        # Log user query and corrected result
        logging.info(f"User Input: {user_input} | Corrected Query: {corrected_query}")

    except Exception as e:
        # Handle errors and log them
        print("An error occurred during processing. Please try again.")
        logging.error(f"Error: {str(e)}")

# Example usage
if __name__ == "__main__":
    user_input = input("Enter your question: ").strip()
    main(user_input)