
import os






def read_yolo_classes(file_path):
    cls_list = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts:
                cls_list.append(parts[0])  # cls是每一行的第一个元素
    return cls_list




all_calss = ['bingtangxueli', 'c1day_green', 'c1day_red', 'c1day_yellow', 'cacui2_flower_tea',
                 'cacui2_puer', 'cacui2_wulong', 'cacui_flower_tea', 'cacui_green_tea', 'cacui_red_tea',
                 'cacui_wulong', 'fengmiyouzi', 'green_tea', 'mangdun_apple', 'mangdun_grape', 'mangdun_lemon',
                 'mangdun_peach', 'molimicha', 'red_tea', 'soda_blue', 'soda_pink', 'tianbao']

def find_most_common_element(lst):
    """
    找出列表中出现次数最多的元素。

    :param lst: 输入列表
    :return: 出现次数最多的元素及其出现次数
    """
    most_common_element = max(set(lst), key=lst.count)
    count = lst.count(most_common_element)
    return most_common_element, count

img_txtPath = r""
img_names = os.listdir(img_txtPath)


video_gt = r"F:\lb\zzzzz\final_tetssssssssssssssssss\multi_data\multi_strass\GT_txtSave.txt"

# 读gt
all_videos = []
all_GTs = []
# 打开文件并读取所有行
with open(video_gt, 'r', encoding='utf-8') as file:
    lines = file.readlines()
# 打印所有行
for line in lines:
    cur_line = line.strip()
    cur_video_name = cur_line.split(":")[0]
    cur_GT = cur_line.split(":")[1]
    all_videos.append(cur_video_name)
    all_GTs.append(cur_GT)


correct_rate = 0
for video_index in range(0, len(all_videos)):

    cur_video_name = all_videos[video_index]
    video_frames = []

    cur_video_GT = all_GTs[video_index]
    # 找出所有前缀为
    for frame_index in range(0, len(img_names)):
        if img_names[frame_index].split("!")[0] +"!"+ img_names[frame_index].split("!")[1] == cur_video_name:
            video_frames.append(img_names[frame_index])

    video_frames_Vote = []
    for i in range(0, len(video_frames)):
        cur_imgPath = os.path.join(img_txtPath, video_frames[i])

        pred_classes = read_yolo_classes(cur_imgPath)
        for index in range(0, len(pred_classes)):
            video_frames_Vote.append(pred_classes[index])

    element, frequency = find_most_common_element(video_frames_Vote)
    pred_GT = all_calss[int(element)]

    if pred_GT == cur_video_GT:
        correct_rate = correct_rate + 1

print("准确率是：{}".format(correct_rate / len(all_videos)))
