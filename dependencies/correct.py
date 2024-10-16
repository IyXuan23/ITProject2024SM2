import Levenshtein
from dependencies.model1 import ask_gpt_for_keywords
from dependencies.database import load_subjects, load_majors, load_courses
from fuzzywuzzy import fuzz
from jellyfish import jaro_winkler_similarity

# Load subjects, majors, and courses data
subjects = load_subjects()
majors = load_majors()
courses = load_courses()

def get_similarity_score(input_str, option_str):
    """
    Calculate the overall similarity score between two strings using multiple algorithms.
    """
    input_str_lower = input_str.lower()
    option_str_lower = option_str.lower()

    # Levenshtein distance
    lev_ratio = Levenshtein.ratio(input_str_lower, option_str_lower)

    # Jaro-Winkler similarity
    jw_similarity = jaro_winkler_similarity(input_str_lower, option_str_lower)

    # Fuzzy matching
    fuzz_ratio = fuzz.token_set_ratio(input_str_lower, option_str_lower) / 100  # Normalize to 0-1

    # Overall score (weights can be adjusted as needed)
    total_score = (lev_ratio + jw_similarity + fuzz_ratio) / 3

    return total_score

def get_best_match(user_input, options):
    """
    Find the closest match from a list of options using similarity scores.
    """
    scores = []

    for option in options:
        total_score = get_similarity_score(user_input, option)
        scores.append((option, total_score))

    # Sort by score in descending order
    scores.sort(key=lambda x: x[1], reverse=True)

    # Set similarity threshold
    if scores and scores[0][1] >= 0.6:
        return scores[0][0]
    return None

def correct_query(key_field, key_subject):
    """
    Generate a corrected query statement based on user input for fields, subjects, majors, or courses.
    """
    # First, check how many digits are in key_subject
    num_digits = sum(c.isdigit() for c in key_subject)
    if num_digits == 5:
        # key_subject has exactly 5 digits
        # Now, check if key_subject exists in the database
        if key_subject in subjects.keys() or key_subject in majors.keys() or key_subject in courses.keys():
            # key_subject exists in the database, proceed normally without correction
            return key_subject
        else:
            # key_subject does not exist in database
            return f"{key_subject} is not available."
        
    # No input cleaning is performed here
    key_subject_raw = key_subject.strip().lower()

    # Create a combined dictionary of all possible options
    all_options = {
        'subject': [data['subject name'] for data in subjects.values()] + list(subjects.keys()),
        'major': list(majors.keys()),
        'course': [data['course name'] for data in courses.values()] + list(courses.keys())
    }

    # Initialize variables to track the best match
    highest_score = 0
    best_match = None
    best_category = None

    # Iterate over each category to find the best match
    for category, options in all_options.items():
        match = get_best_match(key_subject_raw, options)
        if match:
            score = get_similarity_score(key_subject_raw, match)
            if score > highest_score:
                highest_score = score
                best_match = match
                best_category = category

    if best_match:
        corrected_subject = best_match
        # Return the desired output format
        return corrected_subject + "(" + best_category + ")"
    else:
        corrected_subject = key_subject
        return f"Sorry, we couldn't find any information matching '{corrected_subject}'. Please check your input and try again."

def correct_subject(user_input):
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

        # Correct query statement
        corrected_query = correct_query(key_field, key_subject)
        return corrected_query

    except Exception as e:
        # Handle errors and log them
        print("An error occurred during processing. Please try again.")
