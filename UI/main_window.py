import tkinter as tk
from tkinter import messagebox

from UI.navigation import Navigation
from UI.view_data_window import ViewDataWindow
from auth.auth_system import AuthSystem  # 假设 AuthSystem 存在
from auth.storage import Storage
from budget.budget_setting import BudgetSetting
from finance.Finance_Data import FinanceData

from entry_data_window import EntryDataWindow  # 导入新的 EntryDataWindow 类
from FileSavingModule.SaveFileWindow import SaveFileWindow


class MainWindow:
    def __init__(self, master, username,app):




        self.app = app  # 保存对 FinanceApp 实例的引用
        # 创建导航实例
        self.navigation = Navigation(master)

        self.master = master
        self.master.title("个人财务管理系统")
        self.master.geometry("1000x800")  # 设置窗口大小

        self.username = username
        self.finance_data = FinanceData(self.username)  # 实例化 FinanceData

        # 创建按钮
        self.entry_button = tk.Button(master, text="录入财务数据", command=self.open_entry_data_window)
        self.entry_button.pack(pady=10)

        self.view_button = tk.Button(master, text="查看财务数据", command=self.view_data)
        self.view_button.pack(pady=10)

        self.back_button = tk.Button(master, text="返回上一级", command=self.go_back)
        self.back_button.pack(pady=10)

        # 在 __init__ 方法中添加按钮
        self.budget_button = tk.Button(master, text="设定预算", command=self.set_budget)
        self.budget_button.pack(pady=10)

        # 在 __init__ 方法中添加保存文件按钮
        self.budget_button = tk.Button(master, text="保存文件", command=self.saveFinanceData)
        self.budget_button.pack(pady=10)

        self.budget_button = tk.Button(master, text="清空收支记录", command=self.clearAllRecords)
        self.budget_button.pack(pady=10)

        self.budget_button = tk.Button(master, text="清空预算记录", command=self.clearAllBudgetRecords)
        self.budget_button.pack(pady=10)




        self.exit_button = tk.Button(master, text="关闭系统", command=self.exit_system)
        self.exit_button.pack(pady=10)


    def open_entry_data_window(self):
        """打开录入财务数据窗口"""
        EntryDataWindow(self.master, self.finance_data)

    def view_data(self):  # 添加此方法来调用 ViewDataWindow
        view_window = ViewDataWindow(self.master, self.username)

    def go_back(self):
        # 使用 Navigation 类的 go_back 方法
        self.navigation.go_back(self.return_to_login)
        messagebox.showinfo("信息", "已经是登录界面")

    def return_to_login(self):
        # 清空主界面并返回登录界面
        for widget in self.master.winfo_children():
            widget.destroy()
        self.app.create_login_frame()  # 调用 FinanceApp 中的方法创建登录界面


    def exit_system(self):
        self.master.quit()

    def set_budget(self):
        """打开设定预算的窗口"""
        # 初始化 BudgetSetting
        BudgetSetting(self.username)

    def saveFinanceData(self):
        SaveFileWindow(self.master ,self.username)

    def clearAllRecords(self):
        """清空所有收支记录"""
        confirm = messagebox.askyesno("确认", "确定要清空所有收支记录吗？此操作无法撤销。")
        if confirm:
            self.finance_data.clear_all_entries()  # 调用 FinanceData 的方法清空记录
            messagebox.showinfo("成功", "所有收支记录已清空。")
    def clearAllBudgetRecords(self):
        """清空所有预算记录"""
        confirm = messagebox.askyesno("确认", "确定要清空所有预算记录吗？此操作无法撤销。")
        if confirm:
            # 实例化 BudgetSetting 并调用 clear_budget 方法
            budget_setting = BudgetSetting(self.username, isWindowOpen=False)
            budget_setting.clear_budget()
            messagebox.showinfo("成功", "所有预算记录已清空。")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root, 'user1')  # 替换为当前登录的用户名
    root.mainloop()
