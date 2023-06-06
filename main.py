# Rename all the image files and create an image dataset
import os, shutil, sys
from enum import Enum
from rename import RenameAndCopy
from PyQt5.QtCore import QSize, QRect, Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QVBoxLayout, QHBoxLayout, QRadioButton,
                             QWidget, QFileDialog, QMainWindow, QTextEdit, QPushButton, QLabel,
                             QButtonGroup, QGroupBox)

RGB_IMAGE_FOLDERS = 'video rec'
DISPARITY_IMAGE_FOLDERS = 'video_disp'
IMAGE_DATASET = 'image_dataset'

_last_copied_file_id = 0

_app_name = "Bulk Rename"
_sub_string = ""


class FoldersSelectOptions(Enum):
    CONTAIN_SUB_STRING = 1
    ALL_FOLDERS_IN_PARENT = 2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.window_width = 1000
        self.window_height = 600

        self.source_path = ""
        self.destination_path = ""

        self.folders_list = []
        self.selected_folder_option = FoldersSelectOptions.CONTAIN_SUB_STRING
        self.generate_main_ui()

    def create_folder_selection_ui_section(self):
        grp_source_folder = QGroupBox("Source folder")

        self.txt_source_path = QTextEdit()
        self.txt_source_path.setFixedSize(QSize(400, 30))

        btn_add_source_folders = QPushButton()
        btn_add_source_folders.setText("+")
        btn_add_source_folders.setFixedSize(QSize(60, 30))
        btn_add_source_folders.clicked.connect(self.get_source_folders)

        hbox_source_layout = QHBoxLayout()
        hbox_source_layout.addWidget(self.txt_source_path)
        hbox_source_layout.addWidget(btn_add_source_folders)

        grp_source_folder.setLayout(hbox_source_layout)

        # Destination folders
        grp_destination_folder = QGroupBox("Destination Folder")

        self.txt_destination_path = QTextEdit()
        self.txt_destination_path.setFixedSize(QSize(400, 30))

        btn_add_destination_folders = QPushButton()
        btn_add_destination_folders.setText("+")
        btn_add_destination_folders.setFixedSize(QSize(60, 30))
        btn_add_destination_folders.clicked.connect(self.get_destination_folder)

        hbox_destination_layout = QHBoxLayout()
        hbox_destination_layout.addWidget(self.txt_destination_path)
        hbox_destination_layout.addWidget(btn_add_destination_folders)

        grp_destination_folder.setLayout(hbox_destination_layout)

        self.hbox_folders = QHBoxLayout()
        self.hbox_folders.addWidget(grp_source_folder)
        self.hbox_folders.addWidget(grp_destination_folder)

    def create_options_ui_section(self):

        lbl_folder_filter_string = QLabel("Filter folders that contain .")

        self.txt_sub_string = QTextEdit()
        self.txt_sub_string.setFixedSize(QSize(120, 30))
        self.txt_sub_string.textChanged.connect(self.on_sub_string_text_changed)

        self.rd_contain_sub_string = QRadioButton("Folder contain sub string")
        self.rd_contain_sub_string.setChecked(True)
        self.rd_contain_sub_string.toggled.connect(lambda:self.on_options_rdbutton_toggled(self.rd_contain_sub_string))

        self.rd_all_files_in_parent = QRadioButton("All the folders in parent folder")
        self.rd_all_files_in_parent.setChecked(False)
        self.rd_all_files_in_parent.toggled.connect(lambda:self.on_options_rdbutton_toggled(self.rd_all_files_in_parent))

        self.rd_option_btn_group = QButtonGroup()
        self.rd_option_btn_group.addButton(self.rd_contain_sub_string, 1)
        self.rd_option_btn_group.addButton(self.rd_all_files_in_parent, 2)

        option_items_layout = QHBoxLayout()
        option_items_layout.addWidget(lbl_folder_filter_string, alignment=Qt.AlignCenter)
        option_items_layout.addWidget(self.txt_sub_string, alignment=Qt.AlignCenter)
        option_items_layout.addWidget(self.rd_contain_sub_string, alignment=Qt.AlignCenter)
        option_items_layout.addWidget(self.rd_all_files_in_parent, alignment=Qt.AlignCenter)

        self.options_group = QGroupBox("Options")
        self.options_group.setLayout(option_items_layout)

    def generate_main_ui(self):

        self.setWindowTitle(_app_name)
        self.setFixedSize(QSize(self.window_width, self.window_height))

        # Source folders
        self.create_folder_selection_ui_section()
        self.create_options_ui_section()

        # Text box for all the files
        self.txt_source_files = QTextEdit()
        txt_renamed_files = QTextEdit()

        hbox_selected_folders_layout = QHBoxLayout()
        hbox_selected_folders_layout.addWidget(self.txt_source_files)
        hbox_selected_folders_layout.addWidget(txt_renamed_files)

        main_ui_layout = QVBoxLayout()
        main_ui_layout.addLayout(self.hbox_folders)

        self.btn_rename_files = QPushButton()
        self.btn_rename_files.setText("Rename")
        self.btn_rename_files.setFixedSize(QSize(100, 30))
        self.btn_rename_files.setDisabled(True)
        self.btn_rename_files.clicked.connect(self.do_action)

        main_ui_layout.addWidget(self.options_group)

        main_ui_layout.addWidget(self.btn_rename_files)

        main_ui_layout.addLayout(hbox_selected_folders_layout)

        window_widget = QWidget()
        window_widget.setLayout(main_ui_layout)

        self.setCentralWidget(window_widget)
        self.show()

    def on_options_rdbutton_toggled(self, rd_btn):

        if rd_btn.isChecked():

            if rd_btn.text() == "Folder contain sub string":
                self.selected_folder_option = FoldersSelectOptions.CONTAIN_SUB_STRING
                print(f"{rd_btn.text()}")

            elif rd_btn.text() == "All the folders in parent folder":
                self.selected_folder_option = FoldersSelectOptions.ALL_FOLDERS_IN_PARENT

    def on_sub_string_text_changed(self):
        global _sub_string

        _sub_string = self.txt_sub_string.toPlainText()

    def get_source_folders(self):
        # Get the parent directory of the dataset.

        dlg_source_folders = QFileDialog()

        self.source_path = str(dlg_source_folders.getExistingDirectory())
        path_string = ""

        try:
            self.folders_list.append(self.source_path)

            if self.source_path and self.destination_path:
                self.btn_rename_files.setEnabled(True)

            if len(self.folders_list) > 0:
                for folder_id in range(len(self.folders_list)):
                    path_string = path_string + self.folders_list[folder_id] + "\n"

                    self.txt_source_path.setText(path_string)
            else:
                print(f"No folders")
        except:
            print(f"Error ")
        # return source_path

    def get_destination_folder(self):
        dlg_destination_folders = QFileDialog()

        self.destination_path = str(dlg_destination_folders.getExistingDirectory())

        try:
            self.txt_destination_path.setText(self.destination_path)

            if self.source_path and self.destination_path:
                self.btn_rename_files.setEnabled(True)

        except:
            print(f"Error")

    def do_action(self):

        selected_data_folders_list = []
        selected_paths_string = ""

        rename_folders = RenameAndCopy()

        try:

            if self.destination_path == "":
                return

            if len(self.folders_list) > 0:

                for folder_id in range(len(self.folders_list)):

                    if self.selected_folder_option == FoldersSelectOptions.CONTAIN_SUB_STRING:

                        if _sub_string == "":
                            print(f"Empty sub string")

                        sub_folders_list = os.listdir(self.folders_list[folder_id])
                        print(f"Getting sub folders {sub_folders_list[50]}")

                        print(f"No of folders{len(sub_folders_list)}")

                        for sub_folder_id in range(len(sub_folders_list)):

                            if sub_folders_list[sub_folder_id] is not None and _sub_string in sub_folders_list[sub_folder_id]:
                                data_folder = os.path.join(self.folders_list[folder_id], sub_folders_list[sub_folder_id])

                                print(f"All the folders are..{data_folder}")
                                selected_data_folders_list.append(data_folder)

                for selected_folder_id in range(len(selected_data_folders_list)):
                    selected_paths_string = selected_paths_string + selected_data_folders_list[selected_folder_id] + "\n"

                self.txt_source_files.setText(selected_paths_string)

                if not self.destination_path.isspace():

                    for folder_id in range(len(selected_data_folders_list)):
                        print(f"Image folder : {selected_data_folders_list[folder_id]}")

                        rename_folders.copy_data_files(selected_data_folders_list[folder_id], self.destination_path, "image", True)

            else:
                print(f"No image sub folders in the source folder.")
                return

        except Exception:
            print(f"File read error. {Exception}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
