import re
import os

def read_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("File not found.")
        return None


def process(data):
    positon = data.find("M")
    pattern = r'\((.*?)\)'
    matches = re.findall(pattern, data, re.DOTALL)
    first = matches[0].split()
    sec = matches[1].split()
    if "RECT" in data:
        result = first
        result.append(data[positon + 1])
        result.append('0')
        result.append(sec[2])
        result.append(sec[3])
    else:
        result = first
        result.append(data[positon + 1])
        result.append('1')
        if sec[0] == '*':
            result.append(str(int(sec[1]) - int(first[0])))
            result.append("0")
        else:
            result.append(str(int(sec[0]) - int(first[0])))
            result.append("1")
    return result


def save_dict_to_txt(dictionary, filename):
    with open(filename, 'w') as file:
        for key, value in dictionary.items():
            file.write("{i_key}: {i_value}\n".format(i_key=key, i_value=value))


def delete_files_with_more_than_256_lines(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) > 256:
                os.remove(file_path)
                print(f"Deleted {filename} because it has more than 256 lines.\n")
