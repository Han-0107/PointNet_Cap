import os
import json
from func import *

pattern_1 = r'^\*(\d+)+\s(.*)'
net_name = []
net_numbers = []
fs_path = "PointNetCap/data/originFile/fs_1.txt"
case_path = "PointNetCap/data/originFile/case1.txt"
folder_name = "database"

with open(fs_path, 'r', encoding='utf-8') as file:
    for line in file:
        for match in re.finditer(pattern_1, line):
            num = match.group(1)  
            name = match.group(2)  
            net_numbers.append(num)
            net_name.append(name)

pattern_2 = r'\*D_NET \*\d+ .*?(\d+(?:\.\d+)?)(?=\s*\*END)'
net_capacitance = []

with open(fs_path, 'r', encoding='utf-8') as file:
    content = file.read()
    blocks = re.finditer(pattern_2, content, re.DOTALL)
    for block in blocks:
        net_cap = block.group(1)  
        net_capacitance.append(net_cap)

file_content = read_txt_file(case_path)
pattern = r'- (.*?)\n;'
matches = re.findall(pattern, file_content, re.DOTALL)
all_name = []
all_value = []
for section in matches:
    pattern1 = r'(.*?)\n\n\t'
    name = re.findall(pattern1, section, re.MULTILINE)
    value = []
    pattern2 = r'\+\s*(.*?)$'
    rew = re.findall(pattern2, section, re.DOTALL)
    split_items = rew[0].split('\n\t')
    for data in split_items:
        result = process(data)
        value.append(result)
    all_value.append(value)    
    all_name.append(name)     

current_directory = "PointNetCap/data/"
target_directory = os.path.join(current_directory, folder_name)

if not os.path.exists(target_directory):
    os.makedirs(target_directory)

for cap, name in zip(net_capacitance, net_name):
    file_name = '{capacitance}.txt'.format(capacitance=cap)
    file_path = os.path.join(target_directory, file_name)
    for sublist in all_name:
        for i in sublist:
            if i == name:
                with open(file_path, "w", encoding="utf-8") as file:
                    index = all_name.index(sublist)
                    content = all_value[index]
                    for row in content:
                        for item in row:
                            file.write(str(item) + ',')
                        file.write('\n')

delete_files_with_more_than_256_lines(target_directory)

# 生成json文件，便于data_postprocess的查找
data_dictionary = dict(zip(net_name, net_capacitance))
json_dir = 'PointNetCap/data/cap.json'

with open(json_dir, 'w') as file:
    json.dump(data_dictionary, file, indent=4)
