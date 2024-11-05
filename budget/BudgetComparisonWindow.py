import tkinter as tk
from tkinter import messagebox
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from finance.Finance_Data import FinanceData
from budget.budget_setting import BudgetSetting  # 导入BudgetSetting类
import numpy as np  # 添加 numpy 导入



class BudgetComparisonWindow:
    def __init__(self, master, username: str):
        self.master = master
        self.username = username
        self.top = tk.Toplevel(master)
        self.top.title("收入支出预算对比")
        self.top.geometry("1600x1200")  # 窗口大小

        # 实例化FinanceData类读取实际数据
        self.finance_data = FinanceData(self.username)
        self.data = self.finance_data.load_data()

        # 实例化BudgetSetting类读取预算数据
        self.budget_setting = BudgetSetting(self.username, isWindowOpen=False)
        self.budget_data = self.budget_setting.load_budget()

        # 读取预算数据
        self.income_budget = self.budget_data.get("income_budget", 0)
        self.expense_budget = self.budget_data.get("expense_budget", 0)

        # 创建输入框和按钮
        self.year_label = tk.Label(self.top, text="请输入年份:", font=("SimHei", 12))
        self.year_label.pack(pady=5)

        self.year_entry = tk.Entry(self.top, font=("SimHei", 12))
        self.year_entry.pack(pady=5)

        self.month_label = tk.Label(self.top, text="请输入月份(1-12):", font=("SimHei", 12))
        self.month_label.pack(pady=5)

        self.month_entry = tk.Entry(self.top, font=("SimHei", 12))
        self.month_entry.pack(pady=5)

        # 按钮
        self.year_button = tk.Button(self.top, text="年度预算对比", command=self.compare_yearly_budget,
                                     font=("SimHei", 12))
        self.year_button.pack(pady=10)

        self.month_button = tk.Button(self.top, text="月度预算对比", command=self.compare_monthly_budget,
                                      font=("SimHei", 12))
        self.month_button.pack(pady=10)

        # 返回按钮
        self.back_button = tk.Button(self.top, text="返回", command=self.top.destroy, font=("SimHei", 12))
        self.back_button.pack(pady=10)

        # 创建Canvas用于绘图
        self.canvas_frame = tk.Frame(self.top)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = None  # 用于保存画布引用

        # 设置字体为支持中文的字体
        plt.rcParams['font.family'] = 'SimHei'  # 使用SimHei字体（黑体）
        plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    def calculate_total_income(self, year=None, month=None):
        if year and month:
            filtered_data = [entry for entry in self.data if
                             entry['date'].startswith(f"{year}-{month:02d}") and entry['type'] == '收入']
        elif year:
            filtered_data = [entry for entry in self.data if entry['date'].startswith(year) and entry['type'] == '收入']
        else:
            filtered_data = [entry for entry in self.data if entry['type'] == '收入']

        # 如果没有收入数据，返回0
        return sum(entry['amount'] for entry in filtered_data) if filtered_data else 0

    def calculate_total_expense(self, year=None, month=None):
        if year and month:
            filtered_data = [entry for entry in self.data if
                             entry['date'].startswith(f"{year}-{month:02d}") and entry['type'] == '支出']
        elif year:
            filtered_data = [entry for entry in self.data if entry['date'].startswith(year) and entry['type'] == '支出']
        else:
            filtered_data = [entry for entry in self.data if entry['type'] == '支出']

        # 如果没有支出数据，返回0
        return sum(entry['amount'] for entry in filtered_data) if filtered_data else 0

    def compare_yearly_budget(self):
        """对比年度预算"""
        year = self.year_entry.get().strip()
        if not self.is_valid_year(year):
            messagebox.showerror("错误", "请输入有效的年份（四位数字）")
            return

        # 检查输入的年份数据是否存在
        if not self.check_year_data_exists(year):
            messagebox.showerror("错误", f"文件里不存在{year}年的数据，请重新输入")
            return

        # 重新计算年度实际收入和支出
        self.total_income = self.calculate_total_income(year=year)
        self.total_expense = self.calculate_total_expense(year=year)

        # 进行年度预算对比绘图
        self.display_comparison(year, None)

    def compare_monthly_budget(self):
        year = self.year_entry.get().strip()
        month = self.month_entry.get().strip()

        if not self.is_valid_year(year):
            messagebox.showerror("错误", "请输入有效的年份（四位数字）")
            return

        if not self.is_valid_month(month):
            messagebox.showerror("错误", "请输入有效的月份（1-12）")
            return

        # 将月份转换为整数
        try:
            month = int(month)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的月份（1-12）")
            return

        # 检查输入的月份数据是否存在
        if not self.check_month_data_exists(year, month):
            messagebox.showerror("错误", f"文件里不存在{year}年{month}月的数据，请重新输入")
            return

        # 重新计算月度实际收入和支出
        self.total_income = self.calculate_total_income(year=year, month=month)
        self.total_expense = self.calculate_total_expense(year=year, month=month)

        # 进行月度预算对比绘图
        self.display_comparison(year, month)

    def is_valid_year(self, year):
        """检查年份是否合法"""
        return year.isdigit() and len(year) == 4

    def is_valid_month(self, month):
        """检查月份是否合法"""
        return month.isdigit() and 1 <= int(month) <= 12

    def check_year_data_exists(self, year):
        """检查年份数据是否存在"""
        for entry in self.data:
            if entry['date'].startswith(year):
                return True
        return False

    def check_month_data_exists(self, year, month):
        # 将 month 转换为整数以避免字符串格式化问题
        try:
            month = int(month)
        except ValueError:
            return False  # 如果月份不是有效的整数，直接返回 False

        # 确保月份在1到12之间
        if not (1 <= month <= 12):
            return False

        # 检查数据中是否包含该年月
        data_exists = any(entry['date'].startswith(f"{year}-{month:02d}") for entry in self.data)
        return data_exists

    def display_comparison(self, year, month):
        """显示预算对比"""
        if month:
            messagebox.showinfo("月度预算对比", f"进行 {year} 年 {month} 月的预算对比")
        else:
            messagebox.showinfo("年度预算对比", f"进行 {year} 年的年度预算对比")

        # 在这里绘制对比图
        self.clear_previous_plot()  # 清空之前的图形
        self.draw_comparison_chart(year, month)

    def draw_comparison_chart(self, year, month):
        # 设置中心位置和半径
        outer_radius = 0.7  # 控制外圈的半径
        inner_radius = 0.55  # 控制内圈的半径

        # 创建图形
        fig = Figure(figsize=(6, 6), dpi=100)
        ax = fig.add_subplot(111)

        # 绘制预算收入（外圈）和实际收入（内圈）的比例
        wedges, texts, autotexts = ax.pie([self.income_budget, self.total_income], labels=['预算收入', '实际收入'],
                                          autopct='%1.1f%%',
                                          startangle=90, colors=['lightblue', 'green'], radius=outer_radius,
                                          pctdistance=0.85)

        ax.set_title(f"{'月度' if month else '年度'}收入对比 ({year})")

        # 绘制支出部分
        wedges_expense, texts_expense, autotexts_expense = ax.pie([self.expense_budget, self.total_expense],
                                                                  labels=['预算支出', '实际支出'], autopct='%1.1f%%',
                                                                  startangle=90, colors=['lightcoral', 'red'],
                                                                  radius=inner_radius, pctdistance=0.85)

        ax.set_title(f"{'月度' if month else '年度'}支出对比 ({year})")

        # 在每个扇区旁边添加数字和标签（预算/实际金额），避免圆心重叠
        for wedge, value, label in zip(wedges, [self.income_budget, self.total_income], ["预算收入", "实际收入"]):
            angle = (wedge.theta2 + wedge.theta1) / 2  # 计算角度
            x = outer_radius * 1.2 * np.cos(np.radians(angle))  # 计算标签X坐标
            y = outer_radius * 1.2 * np.sin(np.radians(angle))  # 计算标签Y坐标
            ax.text(x, y, f"{label}: {value:.2f}", ha='center', fontsize=12, color="black")

        for wedge, value, label in zip(wedges_expense, [self.expense_budget, self.total_expense],
                                       ["预算支出", "实际支出"]):
            angle = (wedge.theta2 + wedge.theta1) / 2  # 计算角度
            x = inner_radius * 1.2 * np.cos(np.radians(angle))  # 计算标签X坐标
            y = inner_radius * 1.2 * np.sin(np.radians(angle))  # 计算标签Y坐标
            ax.text(x, y, f"{label}: {value:.2f}", ha='center', fontsize=12, color="black")

        # 将图形嵌入到Tkinter窗口
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def clear_previous_plot(self):
        """清除之前的图形，只清除绘图区域"""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None  # 重置画布引用


if __name__ == "__main__":
    # 仅用于测试，实际运行时会在ViewDataWindow中打开
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    budget_comparison_window = BudgetComparisonWindow(root, "user123")  # 假设用户名为user
    root.mainloop()  # 启动主事件循环