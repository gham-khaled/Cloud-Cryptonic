import os
import boto3
import tkinter as tk
from tkinter import ttk

from observer import Publisher

s3 = boto3.client('s3')


class S3FileExplorerFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.app = master
        self.selected_object = Publisher()
        self.selected_bucket =  Publisher()
        self.configure(bg="white")
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self)
        self.tree.heading("#0", text="AWS S3")
        self.tree.column("#0", stretch=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        self.scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.populate_buckets()

    def populate_buckets(self):
        response = s3.list_buckets()
        buckets = response['Buckets']
        for bucket in buckets:
            self.tree.insert('', 'end', iid=bucket['Name'], text=bucket['Name'], tags=['bucket', 'encrypted'])

    def populate_tree(self, bucket_name):
        self.selected_bucket.set_value(bucket_name)

        s3_objects = s3.list_objects_v2(Bucket=bucket_name)
        self.tree.insert('', 'end', text="..", tags='object')

        if 'Contents' in s3_objects:
            for obj in s3_objects['Contents']:
                self.tree.insert('', 'end', text=obj['Key'], tags=['object', {'encrypted': None}])

    def reset(self):
        self.selected_object.set_value(None)
        self.selected_bucket.set_value(None)
        self.tree.delete(*self.tree.get_children())

    def identify(self):
        real_coords = (self.tree.winfo_pointerx() - self.tree.winfo_rootx(),
                       self.tree.winfo_pointery() - self.tree.winfo_rooty())
        item = self.tree.identify('item', *real_coords)
        return self.tree.item(item)

    def on_double_click(self, event):
        item = self.identify()
        text, tags = item['text'], item['tags']
        if 'bucket' in tags:
            self.reset()
            self.populate_tree(text)
        elif 'object' in tags:
            if text == '..':
                self.reset()
                self.populate_buckets()
            else:
                print(f'Clicked on the Object {text}')

    def on_tree_select(self, event):
        item = self.identify()
        text, tags = item['text'], item['tags']

        print("from Select", item)
        # if 'bucket' in tags:
        #     self.selected_bucket = text
        if 'object' in tags:
            if text == '..':
                self.selected_object.set_value(None)

            else:
                self.selected_object.set_value(text)
