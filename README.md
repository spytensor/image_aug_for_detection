**背景**

**深度学习三把斧第一把: "数据增广"**

### 1. 更新

```version 0.1.0```

第一次提交版本,涵盖图像长宽变化的增广方式以及不改变图像长宽的方式.

### 2. 介绍

#### 2.1 依赖

`PIL`,`opencv`,`skimage`

#### 2.2 数据扩充

#### 2.2.1 功能介绍

数据扩充按照是否改变图像尺寸分为两大类 keep_size 和 change_size,

keep_size支持的数据扩充方式:

1. 图像色彩平衡调节:PIL.ImageEnhance.Color()
2. 图像对比度调节:PIL.ImageEnhance.Contrast()
3. 图像亮度调节:PIL.ImageEnhance.Brightness()
4. 图像加噪声:通过skimage.util.random_noise()实现,支持:高斯噪声、盐/椒噪声、泊松噪声、乘法噪声
5. 图像模糊:PIL.ImageFilter

change_size支持的数据扩充方式:

1. 旋转:选择0-360度范围内的旋转
2. 翻转:水平翻转,垂直翻转
3. 缩放:按照一定比例缩放图片

#### 2.2.2 使用方法

Step 1: 准备 csv 格式的标注文件 `train_labels.csv` ,样例如下
```
/mfs/home/zhuchaojie/ds/data/000.jpg,145,245,324,654,helmet
```
Step 2: 修改 `config.py`相关配置,解释如下
```
class DefaultConfigs(object):
    raw_images = "./data/raw/images/"                                       # 原始图片路径
    raw_csv_files = "./data/raw/csv_files/train_labels.csv"                 # 原始csv格式标签
    augmented_images = "./data/augmented/images/"                           # 增强后的图片保存路径
    augmented_csv_file = "./data/augmented/csv_files/augmented_labels.csv"  # 增强后的csv格式的标注文件
    image_format = "jpg"                                                    # 默认图片格式
config = DefaultConfigs()
```

Step 3: 执行 ``python example.py``

**温馨提示: 记得将扩充的数据和原始数据合并后再转换格式**

### 2.3 标注格式转换:

详情移步: [目标检测系列一：如何制作数据集?](http://www.spytensor.com/index.php/archives/48/)

说明:由于csv,txt格式过于简单,不提供转换脚本,直接使用 python open就可以完成.

目前支持的格式转换:

- csv to coco2017
- csv to voc2007
- labelme to coco2017
- labelme to voc2007
- txt to coco2017

### 2.4 增强效果

![]()