import shutil
import os
import cv2
import matplotlib.pyplot as plt

def list_image_paths(data_directory):
    all_image_paths = []
    for folder_name in os.listdir(data_directory):
        folder_path = os.path.join(data_directory, folder_name)
        if os.path.isdir(folder_path):
            image_paths = [os.path.join(folder_path, image_name) for image_name in os.listdir(folder_path)]
            all_image_paths.extend(image_paths)
    return all_image_paths

def clear_directory(directory_path):
    # Remove all files and subdirectories in the directory
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    print("Contents of train_detected_face cleared.")

def show_selected_folders(working_directory,selected_folders):
    fig, axes = plt.subplots(nrows=5, ncols=5, figsize=(15, 15))
    for i, folder_name in enumerate(selected_folders):
        folder_path = os.path.join(working_directory, folder_name)
        image_paths = [os.path.join(folder_path, image_name) for image_name in os.listdir(folder_path)[:5]]

        for j, image_path in enumerate(image_paths):
            # Read the image using OpenCV
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Display the image
            axes[i, j].imshow(img)
            axes[i, j].set_title(f'{folder_name} - {j + 1}')
            axes[i, j].axis('off')

    plt.tight_layout()
    plt.show()
def show_img_by_pathlist(image_paths):
    imgs = 1
    if len(image_paths)>1:
        imgs = len(image_paths)
    fig, axes = plt.subplots(nrows=1, ncols=imgs, figsize=(15, 15))
    for j, image_path in enumerate(image_paths):
        # Read the image using OpenCV
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Display the image
        axes[0, j].imshow(img)
        axes[0, j].set_title(f' ')
        axes[0, j].axis('off')

    plt.tight_layout()
    plt.show()