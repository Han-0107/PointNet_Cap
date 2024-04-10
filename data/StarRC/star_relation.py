
import re
import json

fs_path = '/ugra/yhhan/PointNetCap/data/originFile/cc_nredu_1_output.txt'
json_path1 = '/ugra/yhhan/PointNetCap/data/StarRC/files/star_relation.json'
json_path2 = '/ugra/yhhan/PointNetCap/data/StarRC/files/star_relation_cap.json'
pattern1 = r'\*(\d+) \*(\d+)'
pattern2 = r'\*(\d+) \*(\d+)\s(\d+\.\d+)'

data_dict = {}
data_dict2 = {}

with open(fs_path, 'r') as file:
    for line in file:
        match = re.search(pattern1, line.strip())
        if match:
            num1, num2 = match.groups()
            if num1 in data_dict:
                data_dict[num1].append(num2)
            else:
                data_dict[num1] = [num2]

# 将数据写入 JSON 文件
with open(json_path1, 'w') as json_file:
    json.dump(data_dict, json_file, indent=4) 

with open(fs_path, 'r') as file:
    for line in file:
        match = re.search(pattern2, line.strip())
        if match:
            num1, num2, num3 = match.groups()
            # 创建一个包含 num2 和 num3 的字典
            entry = {'net_num': num2, 'value': float(num3)}
            if num1 in data_dict2:
                data_dict2[num1].append(entry)
            else:
                data_dict2[num1] = [entry]

# 将数据写入 JSON 文件
with open(json_path2, 'w') as json_file:
    json.dump(data_dict2, json_file, indent=4) 