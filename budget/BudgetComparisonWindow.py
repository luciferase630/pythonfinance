import tkinter as tk
from tkinter import messagebox
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from finance.Finance_Data import FinanceData
from budget.budget_setting import BudgetSetting
import numpy as np


class BudgetComparisonWindow:
    def __init__(self, master, username: str):
        self.master = master
        self.username = username
        self.top = tk.Toplevel(master)
        self.top.title("收入支出预算对比")
        self.top.geometry("1600x1200")

        # 实例化FinanceData类读取实际数据
        self.finance_data = FinanceData(self.username)
        self.data = self.finance_data.load_data()

        # 实例化BudgetSetting类读取预算数据
        self.budget_setting = BudgetSetting(self.username, isWindowOpen=False)
        self.budget_data = self.budget_setting.load_budget()

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

        self.canvas = None

        # 设置字体为支持中文的字体
        plt.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False

    def calculate_total_income(self, year=None, month=None):
        if year and month:
            filtered_data = [entry for entry in self.data if
                             entry['date'].startswith(f"{year}-{month:02d}") and entry['type'] == '收入']
        elif year:
            filtered_data = [entry for entry in self.data if entry['date'].startswith(year) and entry['type'] == '收入']
        else:
            filtered_data = [entry for entry in self.data if entry['type'] == '收入']

        return sum(entry['amount'] for entry in filtered_data) if filtered_data else 0

    def calculate_total_expense(self, year=None, month=None):
        if year and month:
            filtered_data = [entry for entry in self.data if
                             entry['date'].startswith(f"{year}-{month:02d}") and entry['type'] == '支出']
        elif year:
            filtered_data = [entry for entry in self.data if entry['date'].startswith(year) and entry['type'] == '支出']
        else:
            filtered_data = [entry for entry in self.data if entry['type'] == '支出']

        return sum(entry['amount'] for entry in filtered_data) if filtered_data else 0

    def compare_yearly_budget(self):
        year = self.year_entry.get().strip()
        if not self.is_valid_year(year):
            messagebox.showerror("错误", "请输入有效的年份（四位数字）")
            return

        if not self.check_year_data_exists(year):
            messagebox.showerror("错误", f"文件里不存在{year}年的数据，请重新输入")
            return

        self.income_budget = self.budget_data.get("year", {}).get("income_budget", 0)
        self.expense_budget = self.budget_data.get("year", {}).get("expense_budget", 0)

        self.total_income = self.calculate_total_income(year=year)
        self.total_expense = self.calculate_total_expense(year=year)

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

        try:
            month = int(month)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的月份（1-12）")
            return

        if not self.check_month_data_exists(year, month):
            messagebox.showerror("错误", f"文件里不存在{year}年{month}月的数据，请重新输入")
            return

        self.income_budget = self.budget_data.get("month", {}).get("income_budget", 0)
        self.expense_budget = self.budget_data.get("month", {}).get("expense_budget", 0)

        self.total_income = self.calculate_total_income(year=year, month=month)
        self.total_expense = self.calculate_total_expense(year=year, month=month)

        self.display_comparison(year, month)

    def is_valid_year(self, year):
        return year.isdigit() and len(year) == 4

    def is_valid_month(self, month):
        return month.isdigit() and 1 <= int(month) <= 12

    def check_year_data_exists(self, year):
        return any(entry['date'].startswith(year) for entry in self.data)

    def check_month_data_exists(self, year, month):
        return any(entry['date'].startswith(f"{year}-{month:02d}") for entry in self.data)

    def display_comparison(self, year, month):
        if month:
            messagebox.showinfo("预算对比", f"{year}年{month}月的月度预算对比")
        else:
            messagebox.showinfo("预算对比", f"{year}年的年度预算对比")

        self.clear_previous_plot()
        self.draw_comparison_chart(year, month)

    def draw_comparison_chart(self, year, month):
        outer_radius = 0.7
        inner_radius = 0.55

        fig = Figure(figsize=(6, 6), dpi=100)
        ax = fig.add_subplot(111)

        # 绘制收入预算对比
        income_data = [self.income_budget, self.total_income]
        wedges, _ = ax.pie(income_data,
                           startangle=90, colors=['lightblue', 'green'],
                           radius=outer_radius)

        # 绘制支出预算对比
        expense_data = [self.expense_budget, self.total_expense]
        wedges_expense, _ = ax.pie(expense_data,
                                   startangle=90, colors=['lightcoral', 'red'],
                                   radius=inner_radius)

        # 设置标题
        ax.set_title(f"{year}年{month}月的月度预算对比" if month else f"{year}年的年度预算对比")

        # 在每个扇区旁边添加数值标签（金额和比例）
        for wedge, value, label in zip(wedges, income_data, ["预算收入", "实际收入"]):
            angle = (wedge.theta2 + wedge.theta1) / 2
            x = outer_radius * 1.2 * np.cos(np.radians(angle))
            y = outer_radius * 1.2 * np.sin(np.radians(angle))
            percentage = f"{value / sum(income_data) * 100:.1f}%" if sum(income_data) > 0 else "0%"
            ax.text(x, y, f"{label}: {value:.2f} ({percentage})", ha='center', fontsize=10, color="black")

        for wedge, value, label in zip(wedges_expense, expense_data, ["预算支出", "实际支出"]):
            angle = (wedge.theta2 + wedge.theta1) / 2
            x = inner_radius * 1.2 * np.cos(np.radians(angle))
            y = inner_radius * 1.2 * np.sin(np.radians(angle))
            percentage = f"{value / sum(expense_data) * 100:.1f}%" if sum(expense_data) > 0 else "0%"
            ax.text(x, y, f"{label}: {value:.2f} ({percentage})", ha='center', fontsize=10, color="black")

        # 添加图例
        ax.legend(wedges + wedges_expense,
                  ['预算收入', '实际收入', '预算支出', '实际支出'],
                  loc="upper right", bbox_to_anchor=(1.1, 1), fontsize=10)

        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def clear_previous_plot(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    budget_comparison_window = BudgetComparisonWindow(root, "user123")
    root.mainloop()
