import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from finance.Finance_Data import FinanceData

class ViewDataWindow:
    def __init__(self, master, username: str):
        self.master = master
        self.username = username
        self.top = tk.Toplevel(master)
        self.top.title("查看财务数据")
        self.top.geometry("600x400")  # 窗口大小

        self.finance_data = FinanceData(self.username)  # 实例化 FinanceData
        self.data = self.finance_data.load_data()  # 加载数据
        self.total_income = self.calculate_total_income()
        self.total_expense = self.calculate_total_expense()
        self.total_balance = self.total_income - self.total_expense

        self.label_total = tk.Label(self.top, text=f"总计: {self.total_balance:.2f}", font=("Arial", 16))
        self.label_total.pack(pady=10)

        self.plot_data()  # 绘制图形

        self.back_button = tk.Button(self.top, text="返回", command=self.top.destroy)
        self.back_button.pack(pady=10)

    def calculate_total_income(self):
        return sum(entry['amount'] for entry in self.data if entry['type'] == '收入')

    def calculate_total_expense(self):
        return sum(entry['amount'] for entry in self.data if entry['type'] == '支出')

    def plot_data(self):
        # 设置字体为 SimHei（黑体），可以根据需要更改为其他支持中文的字体
        plt.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

        # 准备数据
        income_data = [entry['amount'] for entry in self.data if entry['type'] == '收入']
        expense_data = [entry['amount'] for entry in self.data if entry['type'] == '支出']
        labels = ['收入', '支出']

        # 绘制直方图
        fig, ax = plt.subplots()
        ax.bar(labels, [sum(income_data), sum(expense_data)], color=['green', 'red'])
        ax.set_ylabel('金额')
        ax.set_title('收入与支出对比')

        # 显示图形
        plt.show()
if __name__ == "__main__":
    # 测试代码可以放在这里
    pass
