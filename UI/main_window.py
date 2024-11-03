import tkinter as tk
from tkinter import messagebox

from UI.view_data_window import ViewDataWindow
from auth.auth_system import AuthSystem  # 假设 AuthSystem 存在
from auth.storage import Storage
from finance.Finance_Data import FinanceData

from entry_data_window import EntryDataWindow  # 导入新的 EntryDataWindow 类

class MainWindow:
    def __init__(self, master, username):
        self.master = master
        self.master.title("个人财务管理系统")
        self.master.geometry("1000x800")  # 设置窗口大小

        self.username = username
        self.finance_data = FinanceData(self.username)  # 实例化 FinanceData

        # 创建按钮
        self.entry_button = tk.Button(master, text="录入财务数据", command=self.open_entry_data_window)
        self.entry_button.pack(pady=10)

        self.view_button = tk.Button(master, text="查看财务数据", command=self.view_data)  # 保留未实现功能
        self.view_button.pack(pady=10)

        self.back_button = tk.Button(master, text="返回上一级", command=self.go_back)
        self.back_button.pack(pady=10)

        self.exit_button = tk.Button(master, text="关闭系统", command=self.exit_system)
        self.exit_button.pack(pady=10)

    def open_entry_data_window(self):
        """打开录入财务数据窗口"""
        EntryDataWindow(self.master, self.finance_data)

    def view_data(self):  # 添加此方法来调用 ViewDataWindow
        view_window = ViewDataWindow(self.master, self.username)

    def go_back(self):
        messagebox.showinfo("信息", "返回上一级功能尚未实现。")

    def exit_system(self):
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root, 'user1')  # 替换为当前登录的用户名
    root.mainloop()
