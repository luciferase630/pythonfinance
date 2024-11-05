from auth import user
from auth.storage import Storage
from auth.auth_system import AuthSystem
import tkinter as tk
from tkinter import messagebox
from UI.main_window import MainWindow  # 导入主窗口类


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("个人财务管理系统")
        self.root.geometry("1000x800")  # 设置窗口大小

        # 创建存储和认证系统的实例
        storage = Storage()
        self.auth_system = AuthSystem(storage)

        # 创建登录界面
        self.create_login_frame()

    def create_login_frame(self):
        self.clear_frame()

        tk.Label(self.root, text="欢迎使用个人财务管理系统", font=("Arial", 16)).pack(pady=10)

        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)
        self.username_entry.insert(0, "用户名")

        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack(pady=5)
        self.password_entry.insert(0, "密码")

        login_button = tk.Button(self.root, text="登录", command=self.login)
        login_button.pack(pady=5)

        register_button = tk.Button(self.root, text="注册", command=self.register)
        register_button.pack(pady=5)
#这两行没必要，login就是不需要返回键
        # back_button = tk.Button(self.root, text="返回", command=self.back)
        # back_button.pack(pady=5)

        exit_button = tk.Button(self.root, text="退出程序", command=self.root.quit)
        exit_button.pack(pady=5)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get().strip()  # 去除首尾空格
        password = self.password_entry.get().strip()  # 去除首尾空格
        if self.auth_system.login(username, password):  # 检查登录结果
            messagebox.showinfo("登录", f"欢迎回来, {username}!")
            self.open_main_window(username)  # 登录成功后打开主窗口
        else:
            messagebox.showerror("错误", "用户名或密码错误")  # 登录失败

    def open_main_window(self, username):
        self.clear_frame()  # 清空登录界面
        MainWindow(self.root, username,self)  # 实例化主窗口  做了一些修改，为了实现返回到这一集

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        try:
            result = self.auth_system.register(username, password)
            messagebox.showinfo("注册", result)
        except ValueError as e:
            messagebox.showerror("错误", str(e))

    def back(self):
        messagebox.showinfo("返回", "返回上一个界面")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
