import os
import json
from func import *

pattern_1 = r'^\*(\d+)+\s(.*)'
net_name = []
net_numbers = []
fs_path = "/ugra/yhhan/PointNetCap/data/originFile/cc_nredu_1_output.txt"
case_path = "PointNetCap/data/originFile/case1.txt"

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

data_list = []
for name, capacitance, num in zip(net_name, net_capacitance, net_numbers):
    entry = {
        "name": name,
        "number": num,
        "capacitance": capacitance,
        "data": []
    }
    for sublist in all_name:
        if name in sublist:
            index = all_name.index(sublist)
            content = all_value[index]
            entry["data"] = content
            break
    data_list.append(entry)

# 写入包含所有数据的 JSON 文件
json_dir = 'PointNetCap/data/StarRC/files/cap_data.json'
with open(json_dir, 'w') as file:
    json.dump(data_list, file, indent=4)
