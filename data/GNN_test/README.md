# GNN_test

## 运行方法
* 先运行cap_data.py，得到初始的cap信息
* 再运行cap_relation.py，模拟GNN-Cap构造出的可能的耦合关系
* 然后运行real_relation.py，得到真实的耦合关系
* 最后运行main.py，将GNN-Cap和真实的耦合关系进行对比，得到GNN-Cap的命中率

## 简要介绍
首先，cap_data.py和real_relation.py匹配了fs_1.txt中的net信息，将所有信息通过net的编号进行表示，最终生成real_relation.json文件。其次，cap_relation.py模仿了GNN-Cap生成Graph的方式，根据导体的中心距离判定可能的耦合关系。但在这里，层间距离远远小于阈值，且文件中的导体所在层数较少，因此layer的判定条件基本不起作用。为了减少程序运行时间，我设置了up_threshold，如果两个导体距离特别远，说明其所在net的距离基本不会发生耦合效应。根据GNN-Cap原文，较远的耦合情况也只是四倍threshold的距离，因此我们这样设置。最后，main.py将GNN-Cap得到的耦合关系和正确耦合关系进行对比，得到最终结果。

## 效果
一般来说，GNN-Cap这种简单粗暴的方式会导致许多其预测的耦合关系事实上并不存在，从而造成其预测准确性并不高。另外，GNN-Cap所能得到的正确的耦合关系数目与threshold直接相关，threshold越大，所能得到的正确关系就越多，但准确率也会显著下降。
