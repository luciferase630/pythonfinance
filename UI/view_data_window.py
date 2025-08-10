import tkinter as tk
from tkinter import messagebox

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from services.finance_service import FinanceService
from budget.BudgetComparisonWindow import BudgetComparisonWindow

class ViewDataWindow:
    def __init__(self, master, username: str):
        self.master = master
        self.username = username
        self.top = tk.Toplevel(master)
        self.top.title("查看财务数据")
        self.top.geometry("600x400")  # 窗口大小

        self.finance_service = FinanceService(self.username)
        self.data = self.finance_service.get_entries()
        self.total_income = self.calculate_total_income()
        self.total_expense = self.calculate_total_expense()
        self.total_balance = self.total_income - self.total_expense

        self.label_total = tk.Label(self.top, text=f"总计: {self.total_balance:.2f}", font=("Arial", 16))
        self.label_total.pack(pady=10)

        self.histogram_button = tk.Button(self.top, text="绘制收入支出直方图", command=self.plot_histogram)
        self.histogram_button.pack(pady=5)

        self.pie_chart_button = tk.Button(self.top, text="绘制收入支出扇形图", command=self.plot_pie_chart)
        self.pie_chart_button.pack(pady=5)

        # 在 __init__ 方法中添加 "收入支出预算对比" 按钮
        self.budget_comparison_button = tk.Button(self.top, text="收入支出预算对比",
                                                  command=self.open_budget_comparison_window)
        self.budget_comparison_button.pack(pady=10)


        self.canvas_frame = tk.Frame(self.top)  # 用来存放绘图区域的 Frame
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = None  # 用于保存画布引用

    def calculate_total_income(self):
        return sum(entry['amount'] for entry in self.data if entry['type'] == '收入')

    def calculate_total_expense(self):
        return sum(entry['amount'] for entry in self.data if entry['type'] == '支出')

    def clear_previous_plot(self):
        """清除之前的图形，只清除绘图区域"""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None  # 重置画布引用

    def plot_histogram(self):
        self.clear_previous_plot()  # 清除之前的图形
        plt.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        income_data = [entry['amount'] for entry in self.data if entry['type'] == '收入']
        expense_data = [entry['amount'] for entry in self.data if entry['type'] == '支出']
        labels = ['收入', '支出']

        ax.bar(labels, [sum(income_data), sum(expense_data)], color=['green', 'red'])
        ax.set_ylabel('金额')
        ax.set_title('收入与支出对比')

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def plot_pie_chart(self):
        self.clear_previous_plot()  # 清除之前的图形
        # 加载数据
        entries = self.finance_service.get_entries()

        # 初始化数据
        income_dict = {}
        expense_dict = {}

        # 数据聚合
        for entry in entries:
            amount = entry['amount']
            if entry['type'] == '收入':
                income_dict[entry['note']] = income_dict.get(entry['note'], 0) + amount
            elif entry['type'] == '支出':
                expense_dict[entry['note']] = expense_dict.get(entry['note'], 0) + amount

        # 准备扇形图数据
        income_labels = list(income_dict.keys())
        income_sizes = list(income_dict.values())
        expense_labels = list(expense_dict.keys())
        expense_sizes = list(expense_dict.values())

        # 设置字体
        plt.rcParams['font.family'] = 'SimHei'  # 设置字体为 SimHei
        plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

        # 创建图形
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))  # 两个子图，设置大小

        # 绘制收入扇形图
        ax[0].pie(income_sizes, labels=income_labels, autopct='%1.1f%%', startangle=90)
        ax[0].set_title('收入分布')

        # 绘制支出扇形图
        ax[1].pie(expense_sizes, labels=expense_labels, autopct='%1.1f%%', startangle=90)
        ax[1].set_title('支出分布')

        # 将图形嵌入到 Tkinter 窗口
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas = canvas  # 更新当前画布引用

    # 新函数，用来打开新的窗口
    def open_budget_comparison_window(self):
         bugetwindow = BudgetComparisonWindow(self.top,self.username)  # 调用新窗口的构造函数


if __name__ == "__main__":
    # 测试代码可以放在这里
    pass
