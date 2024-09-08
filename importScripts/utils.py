import os
import shutil
import random
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
    into a single of list consisting of all dictionaries values
    
    Args:
    input_list (list): A list of dictionaries.
    
    Returns:
    None if list is empty.
    """
    if not input_list:
        return None
    

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

def convert_list_into_text(input_list: list) -> None | str:
    """
    Converts a list data type into a list
    
    Args:
    input_list (list): A list of strings (may include a sub list)
    
    Returns:
    None if input_list is empty.
    """
    if not input_list:
        return None

    final_list = []
    for i, elt in enumerate(input_list):
        if isinstance(elt, list):
            temp_list = elt.copy()
            temp_list[0] = '(' + temp_list[0]
            temp_list[-1] = temp_list[-1] + ')'
            for n in temp_list:
                if n[-1] not in [',','.',':',')']:
                    n = n + ', '
                final_list.append(n)
        else:
            # Check if it's the last element. If it is append a period.
            if i == len(input_list) - 1:
                elt = elt + '.'
            # If it's not the last element, append a comma.
            else:
                if ('the following' in elt) & (elt[-1] not in [',','.',':']):
                    elt = elt + ': '
                elif elt[-1] not in [',','.',':']:
                    elt = elt + ', '
            final_list.append(elt)
    
    text = ' '.join(final_list) if len(final_list) > 0 else None
    return text





def copy_random_files(source_folder: str, target_folder: str, num_files: int):
    """
    Copies a specified number of random JSON files from the source folder to the target folder.

    Parameters:
    - source_folder (str): The path to the source folder (where the files are).
    - target_folder (str): The path to the destination folder (where files will be copied).
    - num_files (int): The number of random files to copy.

    Behavior:
    - Selects random `.json` files from the source folder.
    - Copies those files to the target folder.
    """
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

        all_files = [f for f in os.listdir(source_folder) if f.endswith('.json')]
        selected_files = random.sample(all_files, num_files)

        for file_name in selected_files:
            src_path = os.path.join(source_folder, file_name)
            dest_path = os.path.join(target_folder, file_name)
            shutil.copy(src_path, dest_path)
            print(f'Copied: {file_name}')
    
    print("--------SUCCEED IN COPYING FILES!-----------\n")

def copy_specific_file(source_folder: str, target_folder :str, file_names: list):
    """
    Copies specific file(s) (by name) from the source folder to the target folder.

    Parameters:
    - source_folder (str): The path to the source folder (where file(s) is located).
    - target_folder (str): The path to the destination folder (where file(s) will be copied).
    - file_name (list): The name of file(s) to copy (including the .json extension).

    Behavior:
    - If file(s) exists in the source folder, they are copied to the target folder.
    - If file(s) does not exist, a message is printed indicating a file was not found.
    """
    
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    for file in file_names:
        src_path = os.path.join(source_folder, file)
        
        # Check if the file exists at the source path
        if os.path.exists(src_path):
            dest_path = os.path.join(target_folder, file)
            shutil.copy(src_path, dest_path)
            print(f'Copied: {file_name}')
        
        else:
            # The file was not found
            print(f'File {file_name} not found in {source_folder}')
            print("--------ERROR!-----------\n")
            break
    print("--------SUCCEED IN COPYING FILES!-----------\n")
