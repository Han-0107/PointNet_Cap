import json

json1_file_path = '/ugra/yhhan/PointNetCap/data/GNN_test/real_relation.json'
json2_file_path = '/ugra/yhhan/PointNetCap/data/GNN_test/cap_relation_5000_20000.json'

key = 2  # 输入第一个net的编号
gnn_right_counter = 0  # GNN预测正确的耦合关系数
gnn_total_counter = 0  # GNN预测的耦合关系总数
real_total_number = 0  # 真实的耦合关系总数

with open(json1_file_path, 'r') as file:
    data1 = json.load(file)  # 真实的耦合关系数据

with open(json2_file_path, 'r') as file:
    data2 = json.load(file)  # GNN预测的耦合关系数据

cap_relation_data = {item["number"]: item["cap_relation"] for item in data2}

while True:
    key_str = str(key)
    if key_str in data1:
        real_relation_set = set(data1[key_str])
        real_total_number += len(real_relation_set)

        if key_str in cap_relation_data:
            predicted_relation_set = set(cap_relation_data[key_str])
            gnn_total_counter += len(predicted_relation_set)
            gnn_right_counter += len(real_relation_set & predicted_relation_set) 

        key += 1  
    else:
        break

# 计算准确率
accuracy = gnn_right_counter / gnn_total_counter
print(f"Accuracy: {accuracy*100:.2f}%")

# 输出所有结果
print(f"GNN预测正确的耦合关系数: {gnn_right_counter}")
print(f"GNN预测的耦合关系总数: {gnn_total_counter}")
print(f"真实的耦合关系总数: {real_total_number}")
