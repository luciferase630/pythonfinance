# navigation.py
import tkinter as tk
from tkinter import messagebox

class Navigation:
    def __init__(self, master):
        self.master = master

    def go_back(self):
        if messagebox.askyesno("确认", "您确定要返回上一级界面吗？"):
            self.master.destroy()  # 关闭当前窗口
            # 这里可以添加打开上一级窗口的逻辑，例如:
            # previous_window = PreviousWindow(self.master)
            # previous_window.show()
