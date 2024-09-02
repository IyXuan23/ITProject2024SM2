import os
import json

def json_to_plaintext(json_file_path, output_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open(output_file_path, 'w', encoding='utf-8') as txt_file:
        for key, value in data.items():
            if isinstance(value, list):
                txt_file.write(f"{key}:\n")
                for item in value:
                    if isinstance(item, dict):
                        for sub_key, sub_value in item.items():
                            txt_file.write(f"  {sub_key}: {sub_value}\n")
                    else:
                        txt_file.write(f"  - {item}\n")
            elif isinstance(value, dict):
                txt_file.write(f"{key}:\n")
                for sub_key, sub_value in value.items():
                    txt_file.write(f"  {sub_key}: {sub_value}\n")
            else:
                txt_file.write(f"{key}: {value}\n")
            txt_file.write("\n")  # Add a blank line between sections


def convert_all_json_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            json_file_path = os.path.join(folder_path, filename)
            output_file_path = os.path.join(folder_path, filename.replace('.json', '.txt'))
            json_to_plaintext(json_file_path, output_file_path)
            print(f"Converted: {filename} to {output_file_path}")


if __name__ == "__main__":
    folder_path = 'subjectInfo'  # Specify the folder containing your JSON files
    convert_all_json_in_folder(folder_path)

    print("All JSON files in the folder have been converted.")
