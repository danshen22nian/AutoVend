import shutil

from PIL import Image, ImageFilter, ImageDraw
import random
import os
import random

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def add_distracting_lines(image):
    width, height = image.size
    canvas = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(canvas)

    for _ in range(100):  # 控制线条数量
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=random_color(), width=random.randint(1, 3))

    masked_image = Image.blend(image, canvas, alpha=0.3)  # 将线条图与原始图像混合

    return masked_image

# 添加抖动效果
def pixelate(image):
    pixelated_image = image.resize((50, 50), resample=Image.NEAREST)
    pixelated_image = pixelated_image.resize(image.size, Image.NEAREST)
    return pixelated_image
# 添加遮挡效果
def add_noise(image):
    width, height = image.size
    noisy_image = Image.new('RGB', (width, height))

    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            if random.random() < 0.05:  # 5%的像素点做遮挡
                r, g, b = 0, 0, 0
            noisy_image.putpixel((x, y), (r, g, b))

    return noisy_image

img_filePath = r"G:\auto_macihine\3D_test\ori_data\train_dataPicked\test\img\tianbao\rename_2"
img_names = os.listdir(img_filePath)
txt_filePath = r"G:\auto_macihine\3D_test\ori_data\train_dataPicked\test\labels\tianbao\rename_2"

save_imgExp_path = r"G:\auto_macihine\3D_test\ori_data\train_dataPicked\test\img\tianbao\rename_2_exp"
save_txtExp_path = r"G:\auto_macihine\3D_test\ori_data\train_dataPicked\test\labels\tianbao\rename_2_exp"

if os.path.exists(save_imgExp_path) == False:
    os.makedirs(save_imgExp_path)

if os.path.exists(save_txtExp_path) == False:
    os.makedirs(save_txtExp_path)

for i in range(0, len(img_names)):

    cur_ori_imgPath = os.path.join(img_filePath, img_names[i])
    cur_ori_txtPath = os.path.join(txt_filePath, img_names[i].split(".")[0] + ".txt")

    # 打开需要处理的图片
    # original_image = Image.open(r'C:\Users\DELL\Desktop\test\44.png')
    original_image = Image.open(cur_ori_imgPath)
    # 添加高斯模糊
    blurred_image = original_image.filter(ImageFilter.GaussianBlur(radius=5))
    pixelated_image = pixelate(original_image)
    noisy_image = add_noise(original_image)
    distract_image = add_distracting_lines(original_image)

    # # 创建文件夹保存处理后的图片
    # output_folder = r'C:\Users\DELL\Desktop\test\final'
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)

    save_blurPath = os.path.join(save_imgExp_path, img_names[i].split(".")[0] + "_blurred" + ".png")
    save_pixelatedPath = os.path.join(save_imgExp_path, img_names[i].split(".")[0] + "_pixelated" + ".png")
    save_noisyPath = os.path.join(save_imgExp_path, img_names[i].split(".")[0] + "_noisy" + ".png")
    save_distractPath = os.path.join(save_imgExp_path, img_names[i].split(".")[0] + "_distract" + ".png")

    # 保存处理后的图片
    # blurred_image.save(os.path.join(save_imgExp_path, 'blurred_image1.jpg'))
    # pixelated_image.save(os.path.join(save_imgExp_path, 'pixelated_image1.jpg'))
    # noisy_image.save(os.path.join(save_imgExp_path, 'noisy_image1.jpg'))
    # distract_image.save(os.path.join(save_imgExp_path, 'distract_image1.jpg'))

    blurred_image.save(save_blurPath)
    pixelated_image.save(save_pixelatedPath)
    noisy_image.save(save_noisyPath)
    distract_image.save(save_distractPath)

    save_txtBlurPath = os.path.join(save_txtExp_path, img_names[i].split(".")[0] + "_blurred" + ".txt")
    save_txtPixelatedPath = os.path.join(save_txtExp_path, img_names[i].split(".")[0] + "_pixelated" + ".txt")
    save_txtNoisyPath = os.path.join(save_txtExp_path, img_names[i].split(".")[0] + "_noisy" + ".txt")
    save_txtDistractPath = os.path.join(save_txtExp_path, img_names[i].split(".")[0] + "_distract" + ".txt")

    shutil.copy(cur_ori_txtPath, save_txtBlurPath)
    shutil.copy(cur_ori_txtPath, save_txtPixelatedPath)
    shutil.copy(cur_ori_txtPath, save_txtNoisyPath)
    shutil.copy(cur_ori_txtPath, save_txtDistractPath)



    print("图片处理完成，处理后的图片保存在 'processed_images' 文件夹中。")
