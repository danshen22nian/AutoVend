import math
import os
import random
import cv2
import itertools

all_class_Name = ['bingtangxueli', 'c1day_green', 'c1day_red', 'c1day_yellow', 'cacui2_flower_tea',
                 'cacui2_puer', 'cacui2_wulong', 'cacui_flower_tea', 'cacui_green_tea', 'cacui_red_tea',
                 'cacui_wulong', 'fengmiyouzi', 'green_tea', 'mangdun_apple', 'mangdun_grape', 'mangdun_lemon',
                 'mangdun_peach', 'molimicha', 'red_tea', 'soda_blue', 'soda_pink', 'tianbao']

def random_pairs_as_lists(elements, n):
    # 生成所有可能的两两组合
    all_pairs = [list(pair) for pair in itertools.combinations(elements, 2)]

    # 随机打乱所有组合
    random.shuffle(all_pairs)

    # 选择前 n 对组合
    selected_pairs = all_pairs[:n]

    return selected_pairs

    # return selected_pairs


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


def merge_and_remove_duplicates(list1, list2):
    # 合并两个列表
    combined_list = list1 + list2

    # 去除重复元素并保持顺序
    unique_list = list(dict.fromkeys(combined_list))

    return unique_list


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


def overlay_images(background_image_path, layer_image_path, output_image_path, save_cur_txtPath, regions_txt_path,
                   layer_labels_path):
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
    with open(save_cur_txtPath, 'a') as f:
        for label in new_labels:
            class_id, x, y, w, h = label
            f.write(f'{class_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n')


# 画出一个框来规定顾客取出商品的区域
area_txt = r"G:\auto_macihine\final_project\view_img\train_fileMake\real_scene\area_\area_txt.txt"

all_scenes = r"G:\auto_macihine\final_project\view_img\train_fileMake\multi_stra3_two_cls\all_scenes"
all_scene_names = os.listdir(all_scenes)
all_scenes_box = r"G:\auto_macihine\final_project\view_img\train_fileMake\multi_stra3_two_cls\all_scenes_box"
video_gt = r"G:\auto_macihine\final_project\view_img\train_fileMake\multi_stra3_two_cls\GT_txtSave.txt"


all_normal = r"G:\auto_macihine\final_project\view_img\train_fileMake\now_split_final\test\nomal\final_results\all_img_split"
all_in = r"G:\auto_macihine\final_project\view_img\train_fileMake\now_split_final\test\in\final_results\all_img_split"


all_normal_txt = r"G:\auto_macihine\final_project\view_img\train_fileMake\now_split_final\test\nomal\final_results\final\txt_files"
all_in_txt = r"G:\auto_macihine\final_project\view_img\train_fileMake\now_split_final\test\in\final_results\final\txt_files"



in_prob = 0.3

# 读gt
all_videos = []

# 打开文件并读取所有行
with open(video_gt, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 打印所有行
for line in lines:
    cur_line = line.strip()
    cur_video_name = line.split(":")[0]
    all_videos.append(cur_video_name)

print(all_videos)

random_List = [0, 1]

for video_index in range(0, len(all_videos)):

    cur_pair = all_videos[video_index].split("!")[1].split("-")
    cur_video_name = all_videos[video_index]
    video_frames = []
    # 找出所有前缀为
    for frame_index in range(0, len(all_scene_names)):
        if all_scene_names[frame_index].split("!")[0] +"!"+ all_scene_names[frame_index].split("!")[1] == cur_video_name:
            video_frames.append(all_scene_names[frame_index])

    normal_frame_num = math.floor((1 - in_prob) * len(video_frames))
    in_frame_num = len(video_frames) - normal_frame_num

    in_normal_frames = random.sample(video_frames, in_frame_num)

    for index in range(0, len(in_normal_frames)):
        # 然后挑选cur_pair中一个
        cur_frame_path = os.path.join(all_scenes, in_normal_frames[index])
        cur_frame_txtPath = os.path.join(all_scenes_box, in_normal_frames[index].split(".")[0] + ".txt")
        with open(cur_frame_txtPath, 'r', encoding='utf-8') as file:
            first_line = file.readline().strip()  # 读取第一行并去除首尾空白字符
            cur_cls = all_class_Name[int(first_line.split(" ")[0])]


        if cur_pair[0] == cur_cls:
            add_cls = cur_pair[1]
        else:
            add_cls = cur_pair[0]

        cur_cls_normal = os.path.join(all_normal, add_cls)
        all_nor_bg = os.listdir(cur_cls_normal)
        cur_cls_in = os.path.join(all_in, add_cls)
        all_in_bg = os.listdir(cur_cls_in)


        sel_num = random.choice(random_List)

        if sel_num == 0:
            cur_normal_name = random.choice(all_nor_bg)
            cur_for = os.path.join(cur_cls_normal, cur_normal_name)
            cur_for_txt = os.path.join(all_normal_txt, cur_normal_name.split(".")[0].split("!")[0],
                                       cur_normal_name.split(".")[0] + ".txt")

            # cur_frame_path = os.path.join(all_scenes, in_normal_frames[index])
            # cur_frame_txtPath = os.path.join(all_scenes_box, in_normal_frames[index].split(".")[0] + ".txt")

            # 往原图上画上第二个类别瓶子 然后把瓶子的位置写入 cur_frame_txtPath 中

            overlay_images(cur_frame_path, cur_for, cur_frame_path, cur_frame_txtPath,
                           area_txt, cur_for_txt)

        else:
            cur_in_name = random.choice(all_in_bg)
            cur_for = os.path.join(cur_cls_in, cur_in_name)
            cur_for_txt = os.path.join(all_in_txt, cur_in_name.split(".")[0].split("!")[0],
                                       cur_in_name.split(".")[0] + ".txt")

            # cur_frame_path = os.path.join(all_scenes, in_normal_frames[index])
            # cur_frame_txtPath = os.path.join(all_scenes_box, in_normal_frames[index].split(".")[0] + ".txt")
            overlay_images(cur_frame_path, cur_for, cur_frame_path, cur_frame_txtPath,
                           area_txt, cur_for_txt)
#     # 从video_frames里面找出
#     print(video_frames)
#     print(print("{}".format()))
#
# print("{}".format())















