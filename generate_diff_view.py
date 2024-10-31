import os

import open3d as o3d
import numpy as np
from PIL import Image
import random


# def random_camera_pose(distance_range=(1.0, 3.0)):
def random_camera_pose(distance_range=(1.0, 10)):
    # Random distance within the specified range
    distance = random.uniform(*distance_range)

    # Random spherical coordinates
    theta = random.uniform(0, 2 * np.pi)
    phi = random.uniform(0, np.pi)

    x = distance * np.sin(phi) * np.cos(theta)
    y = distance * np.sin(phi) * np.sin(theta)
    z = distance * np.cos(phi)

    camera_position = np.array([x, y, z])
    target = np.array([0.0, 0.0, 0.0])
    up = np.array([0.0, 0.0, 1.0])

    return camera_position, target, up


def render_image(mesh, width=640, height=480, distance_range=(1.0, 3.0)):
    # Create a visualizer
    vis = o3d.visualization.Visualizer()
    vis.create_window(width=width, height=height, visible=False)

    # Add the mesh to the visualizer
    vis.add_geometry(mesh)

    # Get random camera pose
    camera_position, target, up = random_camera_pose(distance_range)

    print(camera_position)
    print(target)
    print(up)

    # Set the view control
    ctr = vis.get_view_control()
    ctr.set_lookat(target)
    ctr.set_up(up)
    ctr.set_front(camera_position - target)
    # ctr.set_zoom(0.5)  # Adjust the zoom level if necessary
    random_number = round(random.uniform(0.5, 1), 1)
    ctr.set_zoom(random_number)  # Adjust the zoom level if necessary

    # Render the scene
    vis.poll_events()
    vis.update_renderer()

    # Capture the image
    img = vis.capture_screen_float_buffer(do_render=True)
    vis.destroy_window()

    # Convert to numpy array
    img = np.asarray(img)
    img = (img * 255).astype(np.uint8)

    return img


def save_image(image_array, filename):
    image = Image.fromarray(image_array)
    image.save(filename)


def main():
    # Load the GLB file
    mesh = o3d.io.read_triangle_mesh(r'G:\NewCR\CR_360\tianbao.glb')
    save_path = r"C:\Users\DELL\Desktop\1"
    time = 10
    for i in range(0, time):
        formatted_number = "{:04d}".format(i)

        save_cur_path = os.path.join(save_path, str(formatted_number) + ".png")

        # Render the image
        image_array = render_image(mesh)

        # Save the image
        # save_image(image_array, 'output.png')
        save_image(image_array, save_cur_path)


if __name__ == "__main__":
    main()