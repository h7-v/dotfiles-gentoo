import os
import random
import subprocess
import time


def get_random_image_from_directory(directory_path, exclude_list):
    if not os.path.isdir(directory_path):
        print("Error: The specified directory does not exist.")
        return None

    image_files = [file for file in os.listdir(directory_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print("Error: No image files found in the specified directory.")
        return None

    # Remove the excluded images from the available images
    available_images = [image for image in image_files if image not in exclude_list]

    if not available_images:
        print("Error: All images in the directory have been picked in the last three selections.")
        return None

    random_image = random.choice(available_images)
    return os.path.join(directory_path, random_image)


# Path to dir containing images
directory_path = '/home/h7/Pictures/hyprpaper_wallpapers'

# Initialize an empty list to keep track of the last three picked image filenames
last_three_picks = []

# Sleep for 20 secs on initial wallpaper
time.sleep(20)

# Infinite loop
while True:
    # Select a random image that is not in the last_three_picks list
    while True:
        random_image_path = get_random_image_from_directory(directory_path, last_three_picks)
        if random_image_path not in last_three_picks:
            break

    if random_image_path:
        # Print the randomly picked image and add it to the last_three_picks list
        print("Randomly picked image:", random_image_path)
        last_three_picks.append(random_image_path)

        # If the list of last_three_picks exceeds three elements, remove the oldest element
        if len(last_three_picks) > 3:
            last_three_picks.pop(0)

        # Run command: hyprctl hyprpaper preload "<wallpaper_path.jpg>"
        preload_command = f'hyprctl hyprpaper preload "{random_image_path}"'
        subprocess.run(preload_command, shell=True)

        # Wait for 10 seconds
        time.sleep(10)

        # Run command: hyprctl hyprpaper wallpaper "HDMI-A-1,<wallpaper_path.jpg>"
        wallpaper_command = f'hyprctl hyprpaper wallpaper "HDMI-A-1,{random_image_path}"'
        subprocess.run(wallpaper_command, shell=True)

        # Wait for 5 seconds
        time.sleep(5)

        # Run command: hyprctl hyprpaper unload "<wallpaper_path.jpg>"
        unload_command = f'hyprctl hyprpaper unload "{random_image_path}"'
        subprocess.run(unload_command, shell=True)

        # Wait for 15 seconds before the next iteration
        time.sleep(15)
