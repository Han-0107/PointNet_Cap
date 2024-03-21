import re
import glob
import os
import json

pattern = r'^DIEAREA \( (\d+) (\d+) \) \( (\d+) (\d+) \) ;$'

case_file = "PointNetCap/data/originFile/case1.txt"

# 找到整个网络的起始、终止坐标
with open(case_file, "r") as file:
    for line in file:
        match = re.search(pattern, line.strip())
        if match:
            num1_begin, num2_begin, num1_end, num2_end = match.groups()
            break  

# 设置需要分块的大小
scale = 50000
scale_left = int(num1_begin) + scale
scale_right = int(num2_begin) + scale
scale_index = 1

data_directory = "PointNetCap/data/database"
folder_name = "*.txt"
target_file = os.path.join(data_directory, folder_name)

files = glob.glob(target_file)

def rect_condition(numbers):
    right_up = [numbers[0] + numbers[4], numbers[1] + numbers[5]]
    right_down = [numbers[0] + numbers[4], numbers[1] - numbers[5]]
    left_up = [numbers[0] - numbers[4], numbers[1] + numbers[5]]
    left_down = [numbers[0] - numbers[4], numbers[1] - numbers[5]]
    if ((right_up[0] < scale_right and right_up[1] < scale_right and right_up[0] > scale_left and right_up[1] > scale_left) or 
        (right_down[0] < scale_right and right_down[1] < scale_right and right_down[0] > scale_left and right_down[1] > scale_left) or
        (left_up[0] < scale_right and left_up[1] < scale_right and left_up[0] > scale_left and left_up[1] > scale_left) or
        (left_down[0] < scale_right and left_down[1] < scale_right and left_down[0] > scale_left and left_down[1] > scale_left)):
        return 1
    else:
        return 0
    
def line_condition(numbers):
    if numbers[5] == 1:
        right = [numbers[0] + numbers[4], numbers[1]]
        left = [numbers[0], numbers[1]]
    if numbers[5] == 0:
        right = [numbers[0], numbers[1]]
        left = [numbers[0] + numbers[4], numbers[1]]
    if ((right[0] < scale_right and right[1] > scale_left) or
        (left[0] < scale_right and left[1] > scale_left)):
        return 1
    else:
        return 0

def find_key_by_value(json_file_path, value):
    # 加载 JSON 文件
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # 遍历字典，查找给定值对应的键
    for key, val in data.items():
        if str(val) == str(value):  # 将值转换为字符串进行比较
            return key  # 返回找到的第一个键
    return None  # 如果没有找到，返回 None

target_directory = "PointNetCap/data/database2"
json_path = "PointNetCap/data/cap.json"

if not os.path.exists(target_directory):
    os.makedirs(target_directory)

while(scale_right < int(num1_end) + scale):

    while(scale_left < int(num2_end) + scale):
        # 每个区块开始时，标记是否已经处理了文件
        has_written_file_for_current_block = False

        for file in files:
            with open(file, 'r') as f:
                file_content = f.readlines()  # 读取整个文件内容至列表
                
            file_meets_condition = False  # 初始化文件是否满足条件的标记为False

            # 检查文件的每一行，确定是否满足条件
            for line in file_content:
                numbers = [int(num) for num in line.strip(',\n').split(',')]
                
                # 对导体进行分类和判断
                if numbers[3] == 0 and rect_condition(numbers):  # 矩形导体满足条件
                    file_meets_condition = True
                    break  # 找到满足条件的行即可判断整个文件满足条件
                elif numbers[3] == 1 and line_condition(numbers):  # 线性导体满足条件
                    file_meets_condition = True
                    break

            # 如果文件满足条件，写入整个文件内容
            if file_meets_condition:
                cap_number = os.path.splitext(os.path.basename(file))[0]
                index_file_path = f'PointNetCap/data/database2/Index_{scale_index}.txt'
                with open(index_file_path, 'a') as fout:
                    if not has_written_file_for_current_block:
                        fout.write(f'Left: {scale_left}, Right: {scale_right}\n')
                        fout.write(f'Block {scale_index} contains:\n')
                        has_written_file_for_current_block = True
                    found_key = find_key_by_value(json_path, cap_number)
                    fout.write(f'\nThe Net Name is: {found_key}\n')
                    fout.writelines(file_content)  # 写入整个文件内容

        # 当前区块处理完毕，如果成功写入文件，则递增scale_index
        if has_written_file_for_current_block:
            scale_index += 1
        # 准备处理下一个区块
        scale_left += scale

    # 重置scale_left并更新scale_right，准备下一轮迭代
    scale_left = int(num1_begin) + scale
    scale_right += scale
