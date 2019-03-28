import os
import cv2
import numpy as np 
import pandas as pd 
from tqdm import tqdm 
from glob import glob
from PIL import Image
from data_aug import *
from config import config
from IPython import embed
all_augumentors = ["color","contrast","brightness","noise","blur","rotate",
                    "horizontal_flip","vertical_flip","scale"]
all_noise_type = ["gaussian","localvar","poisson","salt","pepper","s&p","speckle"]

class Augumentor():
    def __init__(self):
        self.image_paths = glob(config.raw_images+"/*.%s"%config.image_format)   # 默认图片格式为jpg
        self.annotations_path = config.raw_csv_files
        self.nlc = keep_size()     # 不改变原始图像大小的增强方式
        self.wlc = change_size(config)   # 改变原始图像大小的增强方式

    def fit(self):
        total_boxes = {}
        # read box info for csv format
        annotations = pd.read_csv(self.annotations_path,header=None).values
        for annotation in annotations:
            key = annotation[0].split(os.sep)[-1]
            value = np.array([annotation[1:]])
            if key in total_boxes.keys():
                total_boxes[key] = np.concatenate((total_boxes[key],value),axis=0)
            else:
                total_boxes[key] = value      
        # read image and process boxes
        for image_path in tqdm(self.image_paths):
            image = Image.open(image_path)
            #embed()
            raw_boxes = total_boxes[image_path.split(os.sep)[-1]].tolist()  # convert csv box to list

            # do augumentation: keep size
            img_file_name = config.augmented_images+image_path.split(os.sep)[-1].split("."+config.image_format)[0]
            # color banlance
            colored_image,colored_box = self.nlc.color(image,raw_boxes,num=1.4)
            self.write_csv(img_file_name+"_colored.%s"%config.image_format,colored_box)
            self.write_image(colored_image,img_file_name+"_colored.%s"%config.image_format)
            # contrast enhance
            contrasted_image,contrasted_box = self.nlc.contrast(image,raw_boxes,num=1.4)
            self.write_csv(img_file_name+"_contrasted.%s"%config.image_format,contrasted_box)
            self.write_image(contrasted_image,img_file_name+"_contrasted.%s"%config.image_format)
            # brightness change
            brightness_image,brightness_box = self.nlc.brightness(image,raw_boxes,num=1.4)
            self.write_csv(img_file_name+"_brightness.%s"%config.image_format,brightness_box)
            self.write_image(brightness_image,img_file_name+"_brightness.%s"%config.image_format)                       
            # noise change default guassion
            gau_noise_image,gau_noise_box = self.nlc.noise(image,raw_boxes,noise_type="gaussian")
            self.write_csv(img_file_name+"_gau_noise.%s"%config.image_format,gau_noise_box)
            self.write_image(gau_noise_image,img_file_name+"_gau_noise.%s"%config.image_format)  
            # blur default guassion
            blured_image,blured_box = self.nlc.blur(image,raw_boxes,filter_type="gaussian",radius=0.9)
            self.write_csv(img_file_name+"_blured.%s"%config.image_format,blured_box)
            self.write_image(blured_image,img_file_name+"_blured.%s"%config.image_format)  

            # change image size
            # rotate image
            raw_labels = np.array(raw_boxes)[:,-1]
            for angle in (90,180,270):
                trans_boxes = np.array(raw_boxes)[:,:-1].tolist()   # 传入改变图像大小函数中
                rotated_image,rotated_box = self.wlc.rotate(image,trans_boxes,angle)

                self.write_csv(img_file_name+"_rotated_{}.{}".format(str(angle),config.image_format),[raw_labels,rotated_box],original=False)
                self.write_image(rotated_image,img_file_name+"_rotated_{}.{}".format(str(angle),config.image_format))   

            # horizontal_flip 
            hf_image,hf_box = self.wlc.horizontal_flip(image,np.array(raw_boxes)[:,:-1].tolist())
            self.write_csv(img_file_name+"_hf.%s"%config.image_format,[raw_labels,hf_box],original=False)
            self.write_image(hf_image,img_file_name+"_hf.%s"%config.image_format)   

            # vertical_flip 
            vf_image,vf_box = self.wlc.vertical_flip(image,np.array(raw_boxes)[:,:-1].tolist())
            self.write_csv(img_file_name+"_vf.%s"%config.image_format,[raw_labels,vf_box],original=False)
            self.write_image(vf_image,img_file_name+"_vf.%s"%config.image_format)          

            # scale 
            scale_image,scale_box = self.wlc.scale(image,np.array(raw_boxes)[:,:-1].tolist(),ratio=[0.3,0.3])
            self.write_csv(img_file_name+"_scale.%s"%config.image_format,[raw_labels,scale_box],original=False)
            self.write_image(scale_image,img_file_name+"_scale.%s"%config.image_format)          


    def write_csv(self,filename,boxes,original=True):
        saved_file = open(config.augmented_csv_file,"a+")
        if original:
            new_boxes = boxes
            for new_box in new_boxes:
                label = new_box[-1]
                saved_file.write(filename+","+str(new_box[0])+","+str(new_box[1])+","+str(new_box[2])+","+str(new_box[3]) + ","+label+"\n")
        else:
            labels, new_boxes= boxes[0],boxes[1]
            for label,new_box in zip(labels,new_boxes):
                saved_file.write(filename+","+str(new_box[0])+","+str(new_box[1])+","+str(new_box[2])+","+str(new_box[3]) + ","+label+"\n")

    def write_image(self,image,filename):
        image.save(filename) 

if __name__ == "__main__":
    if not os.path.exists(config.augmented_images):
        os.makedirs(config.augmented_images)
    if not os.path.exists(config.augmented_csv_file):
        os.makedirs(config.augmented_csv_file)        
    detection_augumentor = Augumentor()
    detection_augumentor.fit()
