

# UVM-YOLO: 基于改进YOLOv5s的无人售货机商品识别算法
UVM-YOLO: An Improved YOLOv5s-Based Product Recognition Algorithm for Unmanned Vending Machines

## 目录

- [代码目录](#代码目录)
- [代码说明](#代码说明)
- [数据集说明](#数据集说明)
- [使用到的库](#使用到的库)


### 代码目录

```
filetree 
├── generate_diff_view.py
├── add_nosiy.py
├── real_scene_generate.py
├── multi_desicion_simple.py
├── multi_desicion_hard.py
├── f_one_cls.py
├── f_two_cls.py
```
### 代码说明
- generate_diff_view.py 用于对商品3D模型进行多视角投影
- add_nosiy.py 用于对多视角2D投影图片进行加噪
- real_scene_generate.py 用于合成模拟真实场景数据集
- multi_desicion_simple.py 用于合成多帧决策简单场景数据集
- multi_desicion_hard.py 用于合成多帧决策复杂场景数据集
- f_one_cls.py 用于简单场景指标计算
- f_two_cls.py 用于复杂场景指标计算

### 数据集说明
在该链接中，分享了真实无人自动售货机拍摄的数据，以及22类商品的3D模型：
百度云盘链接：https://pan.baidu.com/s/111i3MkAVJn9KkbJ0P4ajZw 
提取码：an3n

### 使用到的库
- pytorch
- numpy
- open3d



