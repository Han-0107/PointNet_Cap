# StarRC

## 运行方法
* 和GNN_test类似，不过因为文件格式不同，先运行txt_transform.py进行转换
* 先运行cap_data.py，得到初始的cap信息
* 再运行cap_relation.py，模拟GNN-Cap构造出的可能的耦合关系
* 然后运行real_relation.py，得到真实的耦合关系
* 最后运行main.py，将GNN-Cap和真实的耦合关系进行对比，得到GNN-Cap的命中率
