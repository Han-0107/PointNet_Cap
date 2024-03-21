import os
import numpy as np
from torch.utils.data import Dataset


class MyDataLoader(Dataset):
    def __init__(self, root='/pub/zwz/PointNetCap/data/Cap_Dataset/dataset/', train = True):
        self.root = root
        self.data_info = os.listdir(root)
        split_index = int(len(self.data_info)*0.7)
        if train:
            self.data_info = self.data_info[:split_index]
        else:
            self.data_info = self.data_info[split_index:]

    def __len__(self):
        return len(self.data_info)


    def __getitem__(self, index):
        file_name = self.data_info[index]
        label = float(file_name.strip('.txt'))
        file_path = self.root + file_name
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        points = []
        for line in lines:
            point = line.strip(',\n').split(',')
            point = [float(i) for i in point]
            points.append(point)
        
        for i in range(256 - len(points)):
            points.append([0,0,0,0,0,0])
        points = np.array(points)

        return points, label


if __name__ == '__main__':
        
    import torch

    data = MyDataLoader()
    DataLoader = torch.utils.data.DataLoader(data, batch_size=12, shuffle=True)
    for points, label in DataLoader:
        print(points.shape)
        print(label.shape)
        break
