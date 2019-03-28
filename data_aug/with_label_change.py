"""
需要改变标注框大小、位置等信息的数据扩充方式,支持的方式如下:
主要依赖opencv,numpy完成

1. 旋转:选择0-360度范围内的旋转
2. 翻转:水平翻转,垂直翻转
3. 缩放:按照一定比例缩放图片

"""
import cv2
import PIL
import numpy as np 
from .box_utils import *
from PIL import Image

class change_size(object):
    def __init__(self,config):
        self.config = config

    def rotate(self,image,boxes,angle):
        """
        按给定角度旋转图像
        input:
            image: PIL格式图像
            boxes: 原始标注框信息,list格式
            angle: 待旋转的角度
        output:
            image: 旋转后的图像,PIL格式
            boxes: 翻转后的框
        """        
        assert isinstance(image,PIL.JpegImagePlugin.JpegImageFile)
        assert isinstance(boxes,list)
        boxes = np.array(boxes).astype(np.float64)
        image = np.array(image.copy())   
        ## get image info
        weight,height = image.shape[1],image.shape[0]  
        cx,cy = weight//2,height//2
        corners = get_corners(boxes)
        corners = np.hstack((corners,boxes[:,4:]))
        img = rotate_im(image,angle)
        corners[:,:8] = rotate_box(corners[:,:8],angle,cx,cy,height,weight)
        ## create new box
        new_bbox = get_enclosing_box(corners)
        scale_factor_x = img.shape[1] / weight
        scale_factor_y = img.shape[0] / height
        img = cv2.resize(img,(weight,height))
        new_bbox[:,:4] /= [scale_factor_x,scale_factor_y,scale_factor_x,scale_factor_y]
        boxes = new_bbox
        boxes = clip_box(boxes,[0,0,weight,height],0.25)

        return Image.fromarray(img),boxes.astype(np.int64)

    def horizontal_flip(self,image,boxes):
        """
        水平翻转
        input:
            image: PIL格式图像
            boxes: 原始标注框信息,list格式
        output:
            image: 水平翻转后的图像,PIL格式
            boxes: 翻转后的框
        """
        assert isinstance(image,PIL.JpegImagePlugin.JpegImageFile)
        assert isinstance(boxes,list)
        boxes = np.array(boxes).astype(np.float64)
        image = np.array(image.copy())
        #get image center
        img_center = np.array(image.shape[:2])[::-1]/2
        img_center = np.hstack((img_center,img_center))
        #horizontal flip image
        img_hor_flip = image[:,::-1,:]
        #change boxes for horizontal direction
        boxes[:,[0,2]] += 2 * (img_center[[0,2]] - boxes[:,[0,2]])
        box_w = abs(boxes[:,0] - boxes[:,2])
        #finetune box
        boxes[:,0] -= box_w
        boxes[:,2] += box_w

        return Image.fromarray(img_hor_flip),boxes.astype(np.int64)

    def vertical_flip(self,image,boxes):
        """
        垂直翻转
        input:
            image: PIL格式图像
            boxes: 原始标注框信息,list格式
        output:
            image: 垂直翻转后的图像,PIL格式
            boxes: 翻转后的框
        """
        assert isinstance(image,PIL.JpegImagePlugin.JpegImageFile)
        assert isinstance(boxes,list)
        boxes = np.array(boxes).astype(np.float64)
        image = np.array(image.copy())
        #get image center
        img_center = np.array(image.shape[:2])[::-1]/2
        img_center = np.hstack((img_center,img_center))
        #horizontal flip image
        img_hor_flip = image[::-1,:,:]
        #change boxes for horizontal direction
        boxes[:,[1,3]] += 2 * (img_center[[1,3]] - boxes[:,[1,3]])
        box_h = abs(boxes[:,1] - boxes[:,3])
        #finetune box
        boxes[:,1] -= box_h
        boxes[:,3] += box_h

        return Image.fromarray(img_hor_flip),boxes.astype(np.int64)
    
    def scale(self,image,boxes,ratio=[0.2,0.2]):
        """
        按给定尺度压缩图像
        input:
            image: PIL格式图像
            boxes: 原始标注框信息,list格式
            ratio: 压缩比例,[x,y] 两个方向
        output:
            image: 旋转后的图像,PIL格式
            boxes: 翻转后的框
        """ 
        assert isinstance(image,PIL.JpegImagePlugin.JpegImageFile)
        assert isinstance(boxes,list)      
        assert isinstance(ratio,list)  
        assert ratio[0] < 1
        assert ratio[1] < 1
        boxes = np.array(boxes).astype(np.float64) 
        scale_x,scale_y = ratio
        img = np.array(image)
        img_shape = img.shape
        # resize
        resize_scale_x = 1 - scale_x
        resize_scale_y = 1 - scale_y
        img = cv2.resize(img,None,fx=resize_scale_x,fy=resize_scale_y)
        boxes[:,:4] *= [resize_scale_x,resize_scale_y,resize_scale_x,resize_scale_y]
        canvas = np.zeros(img_shape,dtype=np.uint8)

        y_lim = int(min(resize_scale_y,1) * img_shape[0])
        x_lim = int(min(resize_scale_x,1) * img_shape[1])

        canvas[:y_lim,:x_lim,:] = img[:y_lim,:x_lim,:]
        img = canvas
        boxes = clip_box(boxes,[0,0,1+img_shape[1],img_shape[0]],0.25)

        return Image.fromarray(canvas),boxes.astype(np.int64)


