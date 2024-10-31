import math
import os
import random
import cv2

def read_yolo_labels(txt_file_path):
    labels = []
    with open(txt_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
            labels.append((class_id, x_center, y_center, width, height))
    return labels

def read_yolo_regions(txt_file_path):
    regions = []
    with open(txt_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
            regions.append((x_center, y_center, width, height))
    return regions

def overlay_images(background_image_path, layer_image_path, output_image_path, save_cur_txtPath, regions_txt_path, layer_labels_path):
    # 加载背景图片和图层图片
    background_image = cv2.imread(background_image_path)
    layer_image = cv2.imread(layer_image_path, -1)
    layer_labels = read_yolo_labels(layer_labels_path)

    # 获取图层图片的尺寸和背景图片的尺寸
    layer_height, layer_width, _ = layer_image.shape
    background_height, background_width, _ = background_image.shape

    # 读取固定区域信息
    regions = read_yolo_regions(regions_txt_path)

    # 随机选择一个区域
    selected_region = random.choice(regions)
    x_center, y_center, region_width, region_height = selected_region

    # 转换YOLO格式到像素坐标
    x_center *= background_width
    y_center *= background_height
    region_width *= background_width
    region_height *= background_height

    # 计算随机放置图层图片的位置
    max_x = int(x_center + region_width / 2 - layer_width)
    min_x = int(x_center - region_width / 2)
    max_y = int(y_center + region_height / 2 - layer_height)
    min_y = int(y_center - region_height / 2)

    # 检查并修正最大最小值
    if max_x < min_x:
        max_x = min_x
    if max_y < min_y:
        max_y = min_y

    random_x = random.randint(min_x, max_x)
    random_y = random.randint(min_y, max_y)

    # 提取图层图片的 Alpha 通道作为蒙版
    alpha_mask = layer_image[:, :, 3] / 255.0
    layer_rgb = layer_image[:, :, :3]

    # 将图层图片合成到背景图片上
    for c in range(0, 3):
        background_image[random_y:random_y + layer_height, random_x:random_x + layer_width, c] = \
            alpha_mask * layer_rgb[:, :, c] + \
            (1 - alpha_mask) * background_image[random_y:random_y + layer_height, random_x:random_x + layer_width, c]

    # 计算图层图片中的目标框在背景图片中的新位置并保存为 YOLO 格式
    new_labels = []
    for label in layer_labels:
        class_id, x, y, w, h = label
        x = (random_x + x * layer_width) / background_width
        y = (random_y + y * layer_height) / background_height
        w = w * layer_width / background_width
        h = h * layer_height / background_height
        new_labels.append((class_id, x, y, w, h))

    # 保存合成后的图片
    cv2.imwrite(output_image_path, background_image)

    # 保存新位置的目标框信息到文本文件
    with open(save_cur_txtPath, 'w') as f:
        for label in new_labels:
            class_id, x, y, w, h = label
            f.write(f'{class_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n')

# 画出一个框来规定顾客取出商品的区域
area_txt = r"G:\auto_macihine\final_project\view_img\train_fileMake\real_scene\area_\area_txt.txt"

# 每个视频提取关键帧，

all_keyFramePath = r"G:\auto_macihine\final_project\view_img\train_fileMake\real_scene\all_frames_key_frame"
all_video_names = os.listdir(all_keyFramePath)
all_normal = r"G:\auto_macihine\final_project\view_img\train_fileMake\now_split_final\test\nomal\final_results\all_img_split"
all_in = r"G:\auto_macihine\final_project\view_img\train_fileMake\now_split_final\test\in\final_results\all_img_split"


all_normal_txt = r"G:\auto_macihine\final_project\view_img\train_fileMake\now_split_final\test\nomal\final_results\final\txt_files"
all_in_txt = r"G:\auto_macihine\final_project\view_img\train_fileMake\now_split_final\test\in\final_results\final\txt_files"

in_prob = 0.7
all_clsNames = os.listdir(all_in)

save_path = r"G:\auto_macihine\final_project\view_img\train_fileMake\multi_stra\all_scenes"
save_txtPath = r"G:\auto_macihine\final_project\view_img\train_fileMake\multi_stra\all_scenes_box"

save_GT_path = r"G:\auto_macihine\final_project\view_img\train_fileMake\multi_stra\GT_txtSave.txt"

for i in range(0, len(all_video_names)):

    cur_videoPath = os.path.join(all_keyFramePath, all_video_names[i])
    all_frames = os.listdir(cur_videoPath)

    normal_frame_num = math.floor((1 - in_prob) * len(all_frames))
    in_frame_num = len(all_frames) - normal_frame_num



    for index in range(0, len(all_clsNames)):

        cur_cls_normal = os.path.join(all_normal, all_clsNames[index])
        all_nor_bg = os.listdir(cur_cls_normal)
        cur_cls_in = os.path.join(all_in, all_clsNames[index])
        all_in_bg = os.listdir(cur_cls_in)
        # 当前处理的是 all_clsNames[index] 类别的index
        # 每次从all_frames中随机选出
        # 从列表中随机选择 3 个元素

        normal_frame_names = random.sample(all_frames, normal_frame_num)
        normal_forView_names = random.sample(all_nor_bg, normal_frame_num)
        in_forView_names = random.sample(all_in_bg, in_frame_num)

        normal_c = 0
        in_c = 0
        for index_index in range(0, len(all_frames)):
            cur_frame_name = all_frames[index_index]
            cur_bg = os.path.join(cur_videoPath, all_frames[index_index])

            if cur_frame_name in normal_frame_names:
                # 从all_nor_bg中随机挑出一个
                cur_for = os.path.join(cur_cls_normal, normal_forView_names[normal_c])
                cur_for_txt = os.path.join(all_normal_txt, all_clsNames[index], normal_forView_names[normal_c].split(".")[0] + ".txt")
                # jml_vendingMach_00003!frame_9!bingtangxueli!0829_block.png
                save_cur_framePath = os.path.join(save_path, all_video_names[i] + "!" + all_clsNames[index] + "!" + cur_frame_name.split(".")[0] + "!" + normal_forView_names[normal_c].split(".")[0].split("!")[1] + ".png")

                save_cur_frameTxtPath = os.path.join(save_txtPath, all_video_names[i] + "!" + all_clsNames[index] + "!" + cur_frame_name.split(".")[0] + "!" + normal_forView_names[normal_c].split(".")[0].split("!")[1] + ".txt")
                # print(save_cur_frameTxtPath)
                normal_c = normal_c + 1
                # print("{}".format())

            else:
                cur_for = os.path.join(cur_cls_in, in_forView_names[in_c])
                cur_for_txt = os.path.join(all_in_txt, all_clsNames[index], in_forView_names[in_c].split(".")[0] + ".txt")


                save_cur_framePath = os.path.join(save_path, all_video_names[i] + "!" + all_clsNames[index]+ "!" + cur_frame_name.split(".")[0] + "!" + in_forView_names[in_c].split(".")[0].split("!")[1] + ".png")

                save_cur_frameTxtPath = os.path.join(save_txtPath, all_video_names[i] + "!" + all_clsNames[index] + "!" + cur_frame_name.split(".")[0] + "!" + in_forView_names[in_c].split(".")[0].split("!")[1] + ".txt")

                # save_cur_framePath = os.path.join(save_path, all_video_names[i] + "_" + )
                in_c = in_c + 1
            # if cur_frame_name in normal_frame_names:
            #     print(save_cur_framePath)
            #     print(save_cur_frameTxtPath)
            #     print("{}".format())
            # print(cur_for)
            # overlay_images(cur_bg, cur_for, save_cur_framePath, save_cur_frameTxtPath)
            overlay_images(cur_bg, cur_for, save_cur_framePath, save_cur_frameTxtPath,
                           area_txt, cur_for_txt)
        txt_str = all_video_names[i] + "!" + all_clsNames[index] + ":" + all_clsNames[index] + "\n"
        # 合成图片 保存
        with open(save_GT_path, 'a') as f:
            f.write(txt_str)
        # txt保存
