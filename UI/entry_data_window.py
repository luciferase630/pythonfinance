import tkinter as tk
from tkinter import messagebox
from finance.Finance_Data import FinanceData
from datetime import datetime


class EntryDataWindow:
    def __init__(self, master, finance_data: FinanceData):
        self.master = master
        self.finance_data = finance_data
        self.top = tk.Toplevel(master)
        self.top.title("录入财务数据")
        self.top.geometry("400x300")  # 增大窗口大小

        # 收入/支出的选择框
        self.label1 = tk.Label(self.top, text="选择收入或支出:")
        self.label1.pack(pady=5)
        self.entry_type = tk.StringVar(self.top)
        self.entry_type.set("收入")  # 默认值
        self.type_menu = tk.OptionMenu(self.top, self.entry_type, "收入", "支出")
        self.type_menu.pack(pady=5)

        # 金额输入框
        self.label2 = tk.Label(self.top, text="金额:")
        self.label2.pack(pady=5)
        self.entry_amount = tk.Entry(self.top)
        self.entry_amount.pack(pady=5)

        # 日期输入框
        self.label3 = tk.Label(self.top, text="日期 (格式: YYYY-MM-DD):")
        self.label3.pack(pady=5)
        self.entry_date = tk.Entry(self.top)
        self.entry_date.pack(pady=5)

        # 备注输入框
        self.label4 = tk.Label(self.top, text="备注:")
        self.label4.pack(pady=5)
        self.entry_note = tk.Entry(self.top)
        self.entry_note.pack(pady=5)

        # 提交和返回按钮
        self.submit_button = tk.Button(self.top, text="提交", command=self.submit)
        self.submit_button.pack(pady=10)

        self.back_button = tk.Button(self.top, text="返回", command=self.top.destroy)
        self.back_button.pack(pady=10)

    def submit(self):
        entry = {
            "type": self.entry_type.get(),
            "amount": self.entry_amount.get(),
            "date": self.entry_date.get(),
            "note": self.entry_note.get()
        }

        # 金额验证
        try:
            amount = float(entry["amount"])  # 严格限制为浮点数
            if not (amount > 0):
                raise ValueError("金额必须大于零。")
            entry["amount"] = amount  # 更新金额为浮点数
        except ValueError:
            messagebox.showerror("错误", "金额必须是一个大于零的数字，请重新输入。")
            return

        # 日期格式验证
        try:
            datetime.strptime(entry["date"], "%Y-%m-%d")  # 验证日期格式
        except ValueError:
            messagebox.showerror("错误", "日期格式不正确，请使用 YYYY-MM-DD 格式。")
            return

        # 添加财务数据
        self.finance_data.add_entry(entry)
        messagebox.showinfo("信息", "财务数据已提交！")
        self.top.destroy()


if __name__ == "__main__":
    # 测试代码可以放在这里
    pass
