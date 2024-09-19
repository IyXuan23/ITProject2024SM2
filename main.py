from model import ask_gpt_for_keywords
from database import load_subjects
import difflib
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load subject information
subjects = load_subjects()

def get_closest_match(user_input, options):
    """
    Use difflib to perform fuzzy matching and find the closest match.
    """
    closest_matches = difflib.get_close_matches(user_input.lower(), options, n=1, cutoff=0.6)
    return closest_matches[0] if closest_matches else None

def detect_field_from_input(user_input):
    """
    Custom function to analyze user input and extract the possible field
    (e.g., 'subject name', 'subject code', etc.).
    """
    # Define common field keywords
    common_fields = {
        'subject name': ['subject name', 'name'],
        'subject code': ['subject code', 'code', 'sub co'],
        'pre-requisites': ['pre-requisite', 'prereq', 'pre-requirement'],
        'overview': ['overview', 'description'],
        # You can add more field keywords here
    }
    
    # Convert user input to lowercase
    user_input_lower = user_input.lower()

    # Iterate through common field keywords to find a match
    for field, keywords in common_fields.items():
        for keyword in keywords:
            if keyword in user_input_lower:
                return field
    
    return None

def correct_query(key_field, key_subject):
    """
    Generate a corrected query based on the user's input field and subject name or code.
    """
    key_subject_lower = key_subject.lower()  # Convert to lowercase for matching
    all_subject_names = [data['subject name'].lower() for data in subjects.values()]
    all_subject_codes = [subject_code.lower() for subject_code in subjects.keys()]

    # Get all available fields
    sample_data = next(iter(subjects.values()))  # Pick any subject's data as a sample
    available_fields = [field.lower() for field in sample_data.keys()]

    # Fuzzy match field name
    closest_field = get_closest_match(key_field, available_fields)
    if closest_field:
        corrected_field = closest_field
    else:
        corrected_field = key_field

    # Fuzzy match subject name or code
    closest_subject_name = get_closest_match(key_subject_lower, all_subject_names)
    closest_subject_code = get_closest_match(key_subject_lower, all_subject_codes)

    if closest_subject_name:
        for subject_code, data in subjects.items():
            if data['subject name'].lower() == closest_subject_name:
                corrected_subject = data['subject name']
                break
    elif closest_subject_code:
        for subject_code, data in subjects.items():
            if subject_code.lower() == closest_subject_code:
                corrected_subject = subject_code
                break
    else:
        corrected_subject = key_subject

    # Return the corrected query
    return f"What is the {corrected_field} for {corrected_subject}?"

def main():
    while True:
        user_input = input("Enter your question (or 'exit' to quit): ").strip()
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        try:
            # Detect field from user input using custom function
            key_field = detect_field_from_input(user_input)
            if not key_field:
                print("Sorry, I couldn't detect the field you are asking about.")
                continue

            # Use GPT model to extract keywords to get subject information (subject code or name)
            response = ask_gpt_for_keywords(user_input)

            # Extract subject information
            key_subject = response.split('\n')[1].replace('Key Subject: ', '').strip()

            # Output the detected field and subject
            print(f"Key Field: {key_field}")
            print(f"Key Subject: {key_subject}")
            
            # Automatically correct the query
            corrected_query = correct_query(key_field, key_subject)
            print(f"Corrected Query: {corrected_query}")

            # Log user query and corrected result
            logging.info(f"User Input: {user_input} | Corrected Query: {corrected_query}")

        except Exception as e:
            # Capture and log errors
            print("An error occurred during processing. Please try again.")
            logging.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
