import tkinter as tk
from tkinter import messagebox

class Navigation:
    def __init__(self, master):
        self.master = master

    def go_back(self, callback):
        if messagebox.askyesno("确认", "您确定要返回上一级界面吗？"):
            callback()  # 调用传入的回调函数
