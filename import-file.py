import csv
import glob
import json
import os

# File to save course information
output_file = 'major_info.csv'

# Open CSV file and write data
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Major Title'])
    
    # Loop through JSON files and write course information
    folder_path = 'majorInfo'
    for file_path in glob.glob(os.path.join(folder_path, '*.json')):
        with open(file_path, encoding='utf-8') as file:
            data = json.load(file)
        
        # Get course name and code
        course_title = data['major name']
        
        # Write course information to CSV
        writer.writerow([course_title])

print("--------SUCCEED IN EXPORTING DATA TO CSV!-----------\n")