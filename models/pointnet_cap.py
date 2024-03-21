import torch.nn as nn
import torch.utils.data
import torch.nn.functional as F
from pointnet_utils import PointNetEncoder, feature_transform_reguliarzer

class get_model(nn.Module):
    def __init__(self, k=1):
        super(get_model, self).__init__()
        channel = 6
        self.feat = PointNetEncoder(global_feat=True, feature_transform=False, channel=channel)
        self.fc1 = nn.Linear(1024, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, k)
        self.dropout = nn.Dropout(p=0.4)
        self.bn1 = nn.BatchNorm1d(512)
        self.bn2 = nn.BatchNorm1d(128)
        self.relu = nn.ReLU()

    def forward(self, x):
        x, trans, trans_feat = self.feat(x)
        x = F.relu(self.bn1(self.fc1(x)))
        x = F.relu(self.bn2(self.dropout(self.fc2(x))))
        x = F.relu(self.fc3(x))
        x = torch.squeeze(x)
        return x, trans_feat

class get_loss(torch.nn.Module):
    def __init__(self, mat_diff_loss_scale=0.001):
        super(get_loss, self).__init__()
        self.mat_diff_loss_scale = mat_diff_loss_scale
        self.mse_loss = nn.MSELoss()

    def forward(self, pred, target, trans_feat):
        loss = self.mse_loss(pred, target)

        return loss
    
        loss = F.nll_loss(pred, target)
        # mat_diff_loss = feature_transform_reguliarzer(trans_feat)

        # total_loss = loss + mat_diff_loss * self.mat_diff_loss_scale
        # return total_loss
