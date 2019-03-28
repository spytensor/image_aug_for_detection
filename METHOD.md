### 1. Python PIL 数据处理库常用方式

## 1.1 PIL.ImageEnhance

1. PIL.ImageEnhance.Color()

2. PIL.ImageEnhance.Contrast()

3. PIL.ImageEnhance.Brightness()

4. PIL.ImageEnhance.Sharpness()

## 1.2 PIL.ImageFilter

1. PIL.ImageFilter.EDGE_ENHANCE : 边缘特征增强滤波
2. PIL.ImageFilter.EDGE_ENHANCE_MORE : 深度边缘特征增强滤波
3. PIL.ImageFilter.EMBOSS: 浮雕滤波
4. PIL.ImageFilter.CONTOUR: 轮廓滤波
5. PIL.ImageFilter.BLUR: 模糊滤波
6. PIL.ImageFilter.DETAIL: 细节滤波
7. PIL.ImageFilter.FIND_EDGES: 寻找边界滤波（找寻图像的边界信息）
8. PIL.ImageFilter.SMOOTH: 平滑滤波
9. PIL.ImageFilter.SMOOTH_MORE: 深度平滑滤波
10. PIL.ImageFilter.SHARPEN：锐化滤波
11. PIL.ImageFilter.GaussianBlur：高斯模糊滤波
12. PIL.ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3)):反锐化掩码滤波
    ①radius：模糊半径②percent：反锐化强度（百分比） ③threshold：被锐化的最小亮度
