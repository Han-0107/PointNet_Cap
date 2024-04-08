# 将json文件中的内容与fs_1.txt中的内容进行对比，计算GNN方法的耦合命中率

import re
import json

fs_path = '/ugra/yhhan/PointNetCap/data/originFile/fs_1.txt'
json_path = '/ugra/yhhan/PointNetCap/data/GNN_test/real_relation.json'

pattern = r'\*(\d+) \*(\d+)'

data_dict = {}

with open(fs_path, 'r') as file:
    for line in file:
        match = re.search(pattern, line.strip())
        if match:
            num1, num2 = match.groups()
            if num1 in data_dict:
                data_dict[num1].append(num2)
            else:
                data_dict[num1] = [num2]

# 将数据写入 JSON 文件
with open(json_path, 'w') as json_file:
    json.dump(data_dict, json_file, indent=4) 
