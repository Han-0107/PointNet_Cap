import json
from tqdm import tqdm 

json_file_path = '/ugra/yhhan/PointNetCap/data/GNN_test/files/cap_data.json' 
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

threshold = 1000    # 构造边的距离阈值
up_threshold = 50000
layer_distance = 0.144
data_list = []

for item in tqdm(data, desc="Processing nets", mininterval=60):
    number = item['number']
    data_array = item['data']

    entry = {
        "number": number,
        "cap_relation": []
    }

    for index, sublist in enumerate(data_array):
        x_coordinate = int(sublist[0])
        y_coordinate = int(sublist[1])
        layer = int(sublist[2])
        type = int(sublist[3])
        imme_1 = int(sublist[4])
        imme_2 = int(sublist[5])

        for other_item in data:
            if other_item['number'] == number:
                continue

            for other_sublist in other_item['data']:
                other_x_coordinate = int(other_sublist[0])
                other_y_coordinate = int(other_sublist[1])
                other_layer = int(other_sublist[2])

                distance_condition = (abs(x_coordinate - other_x_coordinate) < threshold) and (abs(y_coordinate - other_y_coordinate) < threshold)
                layer_condition = layer == other_layer or abs(layer - other_layer) * layer_distance < threshold
                up_diatance_condition = (abs(x_coordinate - other_x_coordinate) > up_threshold) or (abs(y_coordinate - other_y_coordinate) > up_threshold)

                if up_diatance_condition:
                    break

                if distance_condition and layer_condition:
                    if other_item['number'] not in entry['cap_relation']:
                        entry['cap_relation'].append(other_item['number'])
                        break   # 当前的net已经加入到耦合关系中，跳到下一个net
    data_list.append(entry)

json_dir = '/ugra/yhhan/PointNetCap/data/GNN_test/files/cap_relation.json'
with open(json_dir, 'w') as file:
    json.dump(data_list, file, indent=4)
