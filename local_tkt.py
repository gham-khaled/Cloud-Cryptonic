import os
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from observer import Publisher


class FileExplorerFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.selected_folder = "/Users/khaledghamgui/Desktop"
        self.selected_file = Publisher()
        self.configure(bg="white")
        self.folder_icon = tk.PhotoImage(file="icons/folder2.png").subsample(20, 20)
        self.file_icon = tk.PhotoImage(file="icons/file2.png").subsample(20, 20)
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("NoBorder.Treeview.Heading", background="", foreground="black", borderwidth=0)
        style.configure("NoBorder.Treeview", font=("Arial", 15), rowheight=30, background="white", borderwidth=0, highlightthickness=0)

        self.tree = ttk.Treeview(self, style="NoBorder.Treeview")
        self.tree.heading("#0", text="Local Files")
        self.tree.column("#0", stretch=True)
        style.configure("NoBorder.Treeview.Heading", font=("Arial", 15))

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.on_double_click)

        self.tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        border_color = "gray"
        border_frame = tk.Frame(self, width=1, bg=border_color)
        border_frame.pack(side=tk.LEFT, fill=tk.Y)

        #self.scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        #self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #self.tree.configure(yscrollcommand=self.scrollbar.set)
        # ="/Users/khaledghamgui/Desktop/Courses"
        self.populate_tree(self.selected_folder)

    def populate_tree(self, path):
        self.tree.insert('', "end", text='..', image=self.folder_icon)
        for entry in os.scandir(path):
            if entry.is_dir():
                item = self.tree.insert('', "end", text=entry.path, tags='folder', image=self.folder_icon)
            else:
                item = self.tree.insert('', "end", text=entry.path, tags='file', image=self.file_icon)
            #self.tree.set(item, column="#0", value=entry.path)
    def reset(self):
        self.selected_file.set_value(None)
        self.tree.delete(*self.tree.get_children())
    def identify(self):
        real_coords = (self.tree.winfo_pointerx() - self.tree.winfo_rootx(),
                       self.tree.winfo_pointery() - self.tree.winfo_rooty())
        item = self.tree.identify('item', *real_coords)
        return self.tree.item(item)
    def on_tree_select(self, event):
        # item = self.tree.selection()[0]
        item = self.identify()
        path, tags = item['text'], item['tags']

        if 'file' in tags:
            self.selected_file.set_value(path)
            pass
            # os.startfile(path)

    def on_double_click(self, event):
        item = self.identify()

        path, tags = item['text'], item['tags']
        print(path)
        print(tags)
        if 'folder' in tags:
            self.reset()
            self.selected_folder= path
            self.populate_tree(path)
            print('Clicked on Folder')
        elif path == '..':
            p1 = Path(self.selected_folder).parent.absolute()
            self.reset()
            self.selected_folder= str(p1)
            self.populate_tree(p1)
            print('Clicked on ..')

        # print(item)
        # print(path)
        # pass
