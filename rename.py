import os, shutil


class RenameAndCopy:
    def __init__(self):
        # self.source_folder = source_folder
        # self.destination_folder = destination_folder
        # self.string_prefix = string_prefix
        # self.rename = rename
        self.last_copied_file_id = 0

    def copy_data_files(self, source_folder, destination_folder, string_prefix="", rename=True):

        files_list = []
        # global _last_copied_file_id
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
                            destination_file_id = self.last_copied_file_id + file_id
                            file_name = string_prefix + str(destination_file_id) + split_file_name[1]
                            destination_path = os.path.join(destination_folder, file_name)
                            shutil.copyfile(origin_path, destination_path)

                    except shutil.SameFileError:
                        print(f"Same file name exist in the destination.")

                    except PermissionError:
                        print(f"Permission denied.")

        except:
            print(f"Unknown Error!.")

        finally:
            self.last_copied_file_id = relevant_file_count + 1
