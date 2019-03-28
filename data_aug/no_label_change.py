"""
不改变标注信息的数据扩充方式,通过python PIL.ImageEnhance来实现,
包括:

1. 图像色彩平衡调节:PIL.ImageEnhance.Color()
2. 图像对比度调节:PIL.ImageEnhance.Contrast()
3. 图像亮度调节:PIL.ImageEnhance.Brightness()
4. 图像加噪声:通过skimage.util.random_noise()实现,支持:高斯噪声、盐/椒噪声、泊松噪声、乘法噪声

"""
import PIL
import numpy as np 
from PIL import Image,ImageEnhance,ImageFilter
from skimage.util import random_noise
from IPython import embed
class keep_size(object):

    def color(self,image,boxes,num=1.3):
        """
        func:   对图像进行色彩平衡调节
        input:
            image:  待增强原始图像的路径,PIL格式
            num:    亮度调节的程度,0表示黑白,1.0表示原始色彩,默认设置1.3
            boxes:  图像中待检测物体的标注框信息,以list格式传入
        output:
            image:  PIL格式的图像
            boxes_changed:  改变后的标注框,无改变时为原始框,list格式
        """
        assert isinstance(image,PIL.JpegImagePlugin.JpegImageFile)
        image = image.copy()
        enh_color = ImageEnhance.Color(image)
        image_enhanced = enh_color.enhance(num)

        return image_enhanced,boxes
    
    def contrast(self,image,boxes,num=1.3):
        """
        func:   对图像进行对比度调节
        input:
            image:  待增强原始图像的路径,PIL格式
            num:    对比度的调节,0表示纯灰色,1.0表示原始对比,默认设置1.3
            boxes:  图像中待检测物体的标注框信息,以list格式传入
        output:
            image:  PIL格式的图像
            boxes_changed:  改变后的标注框,无改变时为原始框,list格式
        """
        assert isinstance(image,PIL.JpegImagePlugin.JpegImageFile)
        image = image.copy()
        enh_contrast = ImageEnhance.Contrast(image)
        image_enhanced = enh_contrast.enhance(num)

        return image_enhanced,boxes
    
    def brightness(self,image,boxes,num=1.3):
        """
        func:   对图像进行亮度调节
        input:
            image:  待增强原始图像的路径,PIL格式
            num:    对比度的调节,0表示黑色,1.0表示原始亮度,默认设置1.3
            boxes:  图像中待检测物体的标注框信息,以list格式传入
        output:
            image:  PIL格式的图像
            boxes_changed:  改变后的标注框,无改变时为原始框,list格式
        """
        assert isinstance(image,PIL.JpegImagePlugin.JpegImageFile)
        image = image.copy()
        enh_brightness = ImageEnhance.Brightness(image)
        image_enhanced = enh_brightness.enhance(num)

        return image_enhanced,boxes

    def noise(self,image,boxes,noise_type="gaussian"):
        """
        func:   对图像增加噪声
        input:
            image:  待增强原始图像的路径,PIL格式
            noise_type:    噪声类别,包括高斯/盐椒噪声/泊松噪声等
            boxes:  图像中待检测物体的标注框信息,以list格式传入
        output:
            image:  PIL格式的图像
            boxes_changed:  改变后的标注框,无改变时为原始框,list格式
        """
        assert isinstance(image,PIL.JpegImagePlugin.JpegImageFile)
        image = image.copy()
        noised_image = (random_noise(np.array(image),mode=noise_type,seed=2020)*255).astype(np.uint8) 
        changed_image = Image.fromarray(noised_image)

        return changed_image,boxes 

    def blur(self,image,boxes,filter_type="gaussian",radius=5):
        """
        func: 对图像进行模糊滤波
        input:
            image:  待增强原始图像的路径,PIL格式
            filter_type:  模糊方式,包括"original"和"gaussian"
            boxes:  图像中待检测物体的标注框信息,以list格式传入
        output:
            image:  PIL格式的图像
            boxes_changed:  改变后的标注框,无改变时为原始框,list格式
        """
        assert isinstance(image,PIL.JpegImagePlugin.JpegImageFile)
        image = image.copy()
        if filter_type == "original":
            blured_image = image.filter(ImageFilter.BLUR)
        elif filter_type == "gaussian":
            blured_image = image.filter(ImageFilter.GaussianBlur(radius=radius))
        else:
            print("ERROR!Blur type not support,please check it later!")
            pass
        return blured_image,boxes 