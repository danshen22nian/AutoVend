import os
import cv2
import numpy as np
import random

def overlay_images(background_image_path, layer_image_path, output_image_path):
    # 加载背景图片和图层图片
    background_image = cv2.imread(background_image_path)
    layer_image = cv2.imread(layer_image_path, -1)

    # 获取图层图片的尺寸和背景图片的尺寸
    layer_height, layer_width, _ = layer_image.shape
    background_height, background_width, _ = background_image.shape

    # 随机计算图层图片的位置
    max_x = background_width - layer_width
    max_y = background_height - layer_height
    random_x = random.randint(0, max_x)
    random_y = random.randint(0, max_y)

    # 提取图层图片的 Alpha 通道作为蒙版
    mask = layer_image[:, :, 3]

    # 将图层图片合成到背景图片上
    roi = background_image[random_y:random_y+layer_height, random_x:random_x+layer_width]
    masked_layer = cv2.bitwise_and(layer_image[:, :, :3], layer_image[:, :, :3], mask=mask)
    masked_background = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask))
    merged_roi = cv2.addWeighted(masked_layer, 1, masked_background, 1, 0)
    background_image[random_y:random_y+layer_height, random_x:random_x+layer_width] = merged_roi

    # 保存合成后的图片
    cv2.imwrite(output_image_path, background_image)

video_filePath = r"G:\auto_macihine\3D_test\ori_data\aaaa\mutli_frame_test\train_frames"
all_video_names = os.listdir(video_filePath)


fore_groundfilePath = r"G:\auto_macihine\3D_test\ori_data\aaaa\qianjing"
all_class_names = os.listdir(fore_groundfilePath)

save_FramePath = r"G:\auto_macihine\3D_test\ori_data\aaaa\mutli_frame_test\hecheng_frames"

# video_name! class! frame_name
for video_index in range(0, len(all_video_names)):
    cur_videoFramesPath = os.path.join(video_filePath, all_video_names[video_index])
    cur_videoFrames = os.listdir(cur_videoFramesPath)

    for frame_index in range(0, len(cur_videoFrames)):
        cur_framePath = os.path.join(cur_videoFramesPath, cur_videoFrames[frame_index])

        frame_name = cur_videoFrames[frame_index].split(".")[0]

        for class_index in range(0, len(all_class_names)):
            save_cur_hechengPath = os.path.join(save_FramePath,all_video_names[video_index] + "!" + all_class_names[class_index]+ "!" + frame_name + "!" + ".png")

            cur_classFilePath = os.path.join(fore_groundfilePath, all_class_names[class_index])
            all_class_frameNames = os.listdir(cur_classFilePath)

            random_element = random.choice(all_class_frameNames)
            layer_image_path = os.path.join(cur_classFilePath, random_element)
            # 调用函数进行图层合成
            overlay_images(cur_framePath, layer_image_path, save_cur_hechengPath)