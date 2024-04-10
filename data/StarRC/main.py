import json
import numpy as np

json1_file_path = '/ugra/yhhan/PointNetCap/data/StarRC/files/real_relation.json'
json2_file_path = '/ugra/yhhan/PointNetCap/data/StarRC/files/star_relation.json'
json3_file_path = '/ugra/yhhan/PointNetCap/data/StarRC/files/real_relation_cap.json'

with open(json1_file_path, 'r') as file:
    data1 = json.load(file)  # 真实的耦合关系数据
with open(json2_file_path, 'r') as file:
    data2 = json.load(file)  # StarRC预测的耦合关系数据
with open(json3_file_path, 'r') as file:
    data3 = json.load(file)  # 耦合关系值数据

value_data = {}
for key, entries in data3.items():
    value_data[key] = {entry["net_num"]: entry["value"] for entry in entries}

# cap_relation_data = {item["number"]: item["cap_relation"] for item in data2}

key = 2  # 输入第一个net的编号
gnn_right_counter = 0  # StarRC预测正确的耦合关系数
gnn_total_counter = 0  # StarRC预测的耦合关系总数
real_total_number = 0  # 真实的耦合关系总数
missed_info = []
while True:
    key_str = str(key)
    if key_str in data1:
        real_relation_set = set(data1[key_str])
        real_total_number += len(real_relation_set)

        if key_str in data2:
            predicted_relation_set = set(data2[key_str])
            gnn_total_counter += len(predicted_relation_set)
            correct_predictions = real_relation_set & predicted_relation_set
            gnn_right_counter += len(correct_predictions)

            missed_predictions = real_relation_set - predicted_relation_set
            
            for item in missed_predictions:
                if item in value_data[key_str]:
                    missed_info.append(value_data[key_str][item])
        key += 1
    else:
        break

# 计算准确率
accuracy = gnn_right_counter / gnn_total_counter if gnn_total_counter > 0 else 0
print(f"Accuracy: {accuracy*100:.2f}%")

# 输出所有结果
print(f"StarRC预测正确的耦合关系数: {gnn_right_counter}")
print(f"StarRC预测的耦合关系总数: {gnn_total_counter}")
print(f"真实的耦合关系总数: {real_total_number}")

# 输出未被估计到的电容平均值
result = np.mean(missed_info)
print(f"未被估计到的电容平均值: {result}")
