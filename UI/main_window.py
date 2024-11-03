import tkinter as tk
from tkinter import messagebox

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("个人财务管理系统")
        self.master.geometry("400x300")  # 设置窗口大小

        # 创建按钮
        self.entry_button = tk.Button(master, text="录入财务数据", command=self.entry_data)
        self.entry_button.pack(pady=10)  # 垂直间距

        self.view_button = tk.Button(master, text="查看财务数据", command=self.view_data)
        self.view_button.pack(pady=10)

        self.back_button = tk.Button(master, text="返回上一级", command=self.go_back)
        self.back_button.pack(pady=10)

        self.exit_button = tk.Button(master, text="关闭系统", command=self.exit_system)
        self.exit_button.pack(pady=10)

    def entry_data(self):
        messagebox.showinfo("信息", "录入财务数据功能尚未实现。")

    def view_data(self):
        messagebox.showinfo("信息", "查看财务数据功能尚未实现。")

    def go_back(self):
        messagebox.showinfo("信息", "返回上一级功能尚未实现。")

    def exit_system(self):
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
