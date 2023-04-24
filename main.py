import os
import boto3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Configure the S3 client
from local_tkt import FileExplorerFrame
from observer import Subscriber
from s3_tkt import S3FileExplorerFrame
from s3_utils import upload_encrypted_file_to_s3, download_and_decrypt_file_from_s3

s3 = boto3.client('s3')
from PIL import Image, ImageTk
import glob


class DualExplorerApp(tk.Tk, Subscriber):
    def __init__(self):
        super().__init__()

        self.title("Cloud Cryptonic")

        self.folder_icon = ImageTk.PhotoImage(Image.open("icons/file.ico"))
        self.file_icon = ImageTk.PhotoImage(Image.open("icons/folder.ico"))
        self.encryption_icon = ImageTk.PhotoImage(Image.open("icons/key.ico"))

        self.custom_font = ("Arial", 12)
        self.geometry("1600x600")
        self.configure(bg="white")
        self.upload_state = tk.DISABLED
        self.download_state = tk.DISABLED
        self.create_widgets()
        self.encryption_var = tk.BooleanVar()
        self.create_toolbar()

    def notify(self):

        print('In Notification')
        ## Upload
        if self.left_frame.selected_file.get_value() and self.right_frame.selected_bucket.get_value():
            print('Upload Active')
            file = self.left_frame.selected_file.get_value()
            bucket = self.right_frame.selected_bucket.get_value()
            print(file, bucket)
            self.upload_button['state'] = tk.NORMAL
        else:
            self.upload_button['state'] = tk.DISABLED
            # self.upload_state =

        # Download
        if self.right_frame.selected_object.get_value():
            object = self.right_frame.selected_object.get_value()
            print(object)
            print('Download Active')
            self.download_button['state'] = tk.NORMAL

        else:
            self.download_button['state'] = tk.DISABLED

    def create_widgets(self):
        self.left_frame = FileExplorerFrame(self)
        self.left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.left_frame.selected_file.subscribe(self)
        self.right_frame = S3FileExplorerFrame(self)
        self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.right_frame.selected_object.subscribe(self)
        self.right_frame.selected_bucket.subscribe(self)

        self.upload_button = ttk.Button(self, text="Upload to S3", command=self.upload_to_s3, state=self.upload_state)
        self.upload_button.place(x=660, y=570)

        self.download_button = ttk.Button(self, text="Download from S3", command=self.download_from_s3,
                                          state=self.download_state)
        self.download_button.place(x=860, y=570)

        style = ttk.Style()
        style.configure("Custom.Treeview", font=self.custom_font)
        style.configure("Custom.Treeview.Heading", font=self.custom_font)

        # # Apply the custom style to the treeview widgets
        # self.left_treeview.config(style="Custom.Treeview")
        # self.right_treeview.config(style="Custom.Treeview")
        #
        # # Insert icons for the left_treeview
        # self.left_treeview.tag_configure("folder", image=self.folder_icon)
        # self.left_treeview.tag_configure("file", image=self.file_icon)

    def upload_to_s3(self):
        filename = self.left_frame.selected_file.get_value()
        s3_bucket = self.right_frame.selected_bucket.get_value()
        key = self.selected_key if self.encryption_var.get() else None
        upload_encrypted_file_to_s3(s3_bucket, filename, filename.split('/')[-1], key)
        # Refresh the S3 file explorer frame
        self.right_frame.reset()
        self.right_frame.populate_tree(s3_bucket)

    def download_from_s3(self):

        target_path = self.left_frame.selected_folder
        s3_bucket = self.right_frame.selected_bucket.get_value()
        s3_key = self.right_frame.selected_object.get_value()
        download_and_decrypt_file_from_s3(s3_bucket, s3_key, target_path + '/' + s3_key)
        # s3.download_file(s3_bucket, s3_key, target_path + '/' + s3_key)

        # Refresh the local file explorer frame
        self.left_frame.reset()
        self.left_frame.populate_tree(target_path)

    def create_toolbar(self):
        self.toolbar = tk.Frame(self, bg="white", height=30, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        encryption_icon_label = tk.Label(self.toolbar, bg="white")
        encryption_icon_label.pack(side=tk.LEFT, padx=(10, 0))

        encryption_checkbox = ttk.Checkbutton(self.toolbar, text="Enable Encryption", variable=self.encryption_var,
                                              command=self.toggle_encryption, )

        encryption_checkbox.pack(side=tk.LEFT, padx=10)

        ssh_folder = os.path.expanduser("~/.ssh")
        key_files = glob.glob(os.path.join(ssh_folder, "*"))

        self.key_var = tk.StringVar()
        if key_files:
            self.key_var.set(key_files[0])

        self.encryption_dropdown = ttk.OptionMenu(self.toolbar, self.key_var, *key_files, command=self.choose_key)
        self.encryption_dropdown.config(state=tk.DISABLED)
        self.encryption_dropdown.pack(side=tk.LEFT)

    def choose_key(self, selection):
        self.selected_key = selection

    def toggle_encryption(self):
        encryption_enabled = self.encryption_var.get()
        encryption_state = tk.NORMAL if encryption_enabled else tk.DISABLED

        self.encryption_dropdown.config(state=encryption_state)


if __name__ == "__main__":
    app = DualExplorerApp()
    app.mainloop()
