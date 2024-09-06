from datetime import datetime

def convert_to_daterange(period_str):
    #print("Perod_str is" + period_str)
    """
    Converts a period string (e.g., "26 February 2024 to 26 May 2024")
    into a PostgreSQL daterange string (e.g., "[2024-02-26,2024-05-26]").
    
    Args:
    period_str (str): A string with the format "start_date to end_date".
    
    Returns:
    str: A PostgreSQL daterange formatted string.
    """
    # Replace ' - ' or '-' with ' to ' for compatibility
    if '-' in period_str:
        return None  # Return None if both start and end are invalid
    try:
        # Split the string into start and end dates
        start_date_str, end_date_str = period_str.split(" to ")
        # Try parsing the start and end dates
        start_date = datetime.strptime(start_date_str.strip(), "%d %B %Y").date()
        end_date = datetime.strptime(end_date_str.strip(), "%d %B %Y").date()

        # Return the daterange string
        return f'[{start_date},{end_date}]'
    
    # Occur if no date range provided.
    except ValueError as e:
        print(f"Error parsing date range '{period_str}': {e}, return None. Don't worry, this means a date range isn't provided")
        return None

def convert_to_date(date_str):
    """
    Converts a string (e.g., "26 February 2024")
    into a PostgreSQL date (e.g., "2024-02-26").
    
    Args:
    date_str (str): A string with the format "day month year".
    
    Returns:
    str: A PostgreSQL date formatted string.
    """
    # Check for invalid placeholders like '—' or empty strings
    if '—' in date_str or not date_str.strip():
        return None
    
    try:
        # Try parsing the date string
        return datetime.strptime(date_str.strip(), "%d %B %Y").date()
    except ValueError as e:
        # Handle any ValueError due to improper date formatting
        print(f"Error parsing date '{date_str}': {e}. Don't worry, this means a date isn't provided")
        return None
    
def convert_listdict_to_list(input_list: list) -> None | list:
    """
    Converts a list of dictionaries 
    into a single of list of values from all dictionaries
    
    Args:
    input_list (list): A list of dictionaries.
    
    Returns:
    None if list is empty.
    """
    return_list = []
    for info in input_list:
        for value in info.values():
            if value != None:
                for sub in value:
                    if isinstance(sub,list):
                        for elt in sub:
                            elt = elt +  '; '
                            return_list.append(elt)
                    else:
                        return_list.append(sub)
                    continue
    return None if len(return_list) == 0 else return_list
            
