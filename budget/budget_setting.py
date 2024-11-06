import json
import os
import sys
import tkinter as tk
from tkinter import messagebox


class BudgetSetting:
    def __init__(self, username, isWindowOpen=True):
        self.username = username

        # 处理打包后环境的路径问题
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.budget_folder = os.path.join(base_dir, "budgetData")  # 预算文件夹路径
        self.budget_file = os.path.join(self.budget_folder, f'{username}_budget.json')  # 用户预算文件路径

        # 确保预算文件夹存在
        os.makedirs(self.budget_folder, exist_ok=True)
        self.data = self.load_budget()  # 加载预算数据

        # 创建用于映射显示值和存储值的字典
        self.category_mapping = {
            "月度": "month",
            "年度": "year"
        }

        # 创建窗口
        if isWindowOpen:
            self.create_window()

    def create_window(self):
        self.top = tk.Toplevel()  # 创建顶层窗口
        self.top.title("设定预算")
        self.top.geometry("400x350")

        # 收入预算输入框
        self.label_income = tk.Label(self.top, text="设定收入预算:")
        self.label_income.pack(pady=5)
        self.entry_income = tk.Entry(self.top)
        self.entry_income.pack(pady=5)

        # 支出预算输入框
        self.label_expense = tk.Label(self.top, text="设定支出预算:")
        self.label_expense.pack(pady=5)
        self.entry_expense = tk.Entry(self.top)
        self.entry_expense.pack(pady=5)

        # 预算类别选择框
        self.label_category = tk.Label(self.top, text="选择预算类别:")
        self.label_category.pack(pady=5)
        self.category_var = tk.StringVar(self.top)
        self.category_var.set("月度")  # 设置默认值为"月度"
        self.category_menu = tk.OptionMenu(self.top, self.category_var, "月度", "年度",
                                           command=self.update_menu_display)
        self.category_menu.pack(pady=5)

        # 提交按钮
        self.submit_button = tk.Button(self.top, text="提交", command=self.submit_budget)
        self.submit_button.pack(pady=10)

        # 返回按钮
        self.back_button = tk.Button(self.top, text="返回", command=self.top.destroy)
        self.back_button.pack(pady=10)

        # 初始化显示
        self.update_menu_display()

    def update_menu_display(self, *args):
        selected = self.category_var.get()
        if selected == "Month":
            self.category_menu['menu'].entryconfig(0, label="月度")
            self.category_menu['menu'].entryconfig(1, label="年度")
        else:
            self.category_menu['menu'].entryconfig(0, label="月度")
            self.category_menu['menu'].entryconfig(1, label="年度")

    def submit_budget(self):
        try:
            income_budget = float(self.entry_income.get())
            expense_budget = float(self.entry_expense.get())
            budget_category_display = self.category_var.get()

            # 将显示的预算类别转换为存储值
            budget_category = self.category_mapping.get(budget_category_display, "month")

            if income_budget < 0 or expense_budget < 0:
                raise ValueError("预算金额必须大于等于零。")

            # 设置预算
            self.set_budget(income_budget, expense_budget, budget_category)
            messagebox.showinfo("信息", "预算已设定！")
            self.top.destroy()  # 关闭窗口
        except ValueError as e:
            messagebox.showerror("错误", f"输入无效: {e}")

    def set_budget(self, income_budget, expense_budget, category):
        """设置预算并保存到文件"""
        budget_data = {
            "income_budget": income_budget,
            "expense_budget": expense_budget,
            "category": category
        }
        self.save_budget(budget_data)

    def save_budget(self, budget_data):
        """保存预算数据到文件"""
        with open(self.budget_file, "w", encoding="utf-8") as json_file:
            json.dump(budget_data, json_file, ensure_ascii=False, indent=4)

    def load_budget(self):
        """加载预算数据"""
        if os.path.exists(self.budget_file):
            if os.path.getsize(self.budget_file) > 0:
                with open(self.budget_file, "r", encoding="utf-8") as json_file:
                    return json.load(json_file)
        # 如果文件不存在，则创建文件
        self.save_budget({"income_budget": 0, "expense_budget": 0, "category": "month"})
        return {}

    def clear_budget(self):
        """清空预算记录"""
        empty_budget_data = {"income_budget": 0, "expense_budget": 0, "category": "month"}
        self.save_budget(empty_budget_data)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    budget_setting = BudgetSetting("user123")
    root.mainloop()
