# Rename all the image files and create an image dataset
import os, shutil
import tkinter as tk
from tkinter import filedialog

RGB_IMAGE_FOLDERS = 'video rec'
DISPARITY_IMAGE_FOLDERS = 'video_disp'
IMAGE_DATASET = 'image_dataset'
IMAGE_DATASET_TEMP = 'image_data_temp'          # Temporary folder to hold the images while renaming the files.

_last_copied_file_id = 0


def get_source_folders():
    root = tk.Tk()
    root.withdraw()

    # Get the parent directory of the dataset.
    source_path = filedialog.askdirectory()

    return source_path


def copy_data_files(source_folder, destination_folder, string_prefix="", rename=True):
    files_list = []
    global _last_copied_file_id
    relevant_file_count = 0

    try:
        files_list = os.listdir(source_folder)

        # Sort the list alphabetically
        files_list.sort()

        for file_id in range(len(files_list)):
            origin_path = os.path.join(source_folder, files_list[file_id])
            destination_path = os.path.join(destination_folder, files_list[file_id])

            split_file_name = os.path.splitext(files_list[file_id])

            if (split_file_name[1] == '.jpg') or (split_file_name[1] == '.jpeg'):
                relevant_file_count = relevant_file_count + 1

                try:
                    if not rename:
                        shutil.copyfile(origin_path, destination_path)
                    else:
                        destination_file_id = _last_copied_file_id + file_id
                        destination_path = os.path.join(destination_folder, string_prefix + str(destination_file_id))
                        shutil.copyfile(origin_path, destination_path)

                except shutil.SameFileError:
                    print(f"Same file name exist in the destination.")

                except PermissionError:
                    print(f"Permission denied.")

    except:
        print(f"Unknown Error!.")

    finally:
        _last_copied_file_id = relevant_file_count + 1


def main():
    source_directory_path = get_source_folders()

    folders_list = os.listdir(source_directory_path)

    image_folders_list = []

    try:

        dataset_folder_exist = False
        dataset_temp_folder_exist = False

        if len(folders_list) > 0:

            dataset_path = ""
            temp_data_path = ""

            for folder_id in range(len(folders_list)):
                if RGB_IMAGE_FOLDERS in folders_list[folder_id]:
                    print(f"Image folder selected")
                    image_folders_list.append(folders_list[folder_id])

                # Create image dataset folder if it doesn't exist
                if IMAGE_DATASET in folders_list[folder_id]:
                    dataset_folder_exist = True

                if IMAGE_DATASET_TEMP in folders_list[folder_id]:
                    dataset_temp_folder_exist = True

            dataset_path = os.path.join(source_directory_path, IMAGE_DATASET)
            temp_data_path = os.path.join(source_directory_path, IMAGE_DATASET_TEMP)

            if not dataset_folder_exist:
                os.mkdir(dataset_path)

            if not dataset_temp_folder_exist:
                os.mkdir(temp_data_path)

            if not dataset_path.isspace():

                for folder_id in range(len(image_folders_list)):
                    image_folder = os.path.join(source_directory_path, image_folders_list[folder_id])
                    print(f"Image folder : {image_folder}")

                    print(f"Temp folder : {temp_data_path}")
                    copy_data_files(image_folder, dataset_path, "image", True)

            if __debug__:
                print(f"Source path: {source_directory_path}")

        else:
            print(f"No image sub folders in the source folder.")

    except Exception:
        print(f"File read error. {Exception}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
