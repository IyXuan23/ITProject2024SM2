from datetime import datetime

def convert_to_daterange(period_str):
    """
    Converts a period string (e.g., "26 February 2024 to 26 May 2024")
    into a PostgreSQL daterange string (e.g., "[2024-02-26,2024-05-26]").
    
    Args:
    period_str (str): A string with the format "start_date to end_date".
    
    Returns:
    str: A PostgreSQL daterange formatted string.
    """
    start_date_str, end_date_str = period_str.split(" to ")
    start_date = datetime.strptime(start_date_str, "%d %B %Y").date()
    end_date = datetime.strptime(end_date_str, "%d %B %Y").date()

    daterange_str = f'[{start_date},{end_date}]'

    return daterange_str

def convert_to_date(date_str):
    """
    Converts a string (e.g., "26 February 2024")
    into a PostgreSQL date (e.g., "2024-02-26").
    
    Args:
    date_str (str): A string with the format "day month year".
    
    Returns:
    str: A PostgreSQL date formatted string.
    """
    date = datetime.strptime(date_str, "%d %B %Y").date()  # Fix applied here
    return date