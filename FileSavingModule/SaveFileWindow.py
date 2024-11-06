import tkinter as tk
from tkinter import messagebox, filedialog
from finance.Finance_Data import FinanceData
import os


class SaveFileWindow:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.finance_data = FinanceData(self.username)  # 实例化 FinanceData

        self.top = tk.Toplevel(master)
        self.top.title("保存文件")
        self.top.geometry("300x200")

        # 文件格式选择
        self.format_var = tk.StringVar(value="csv")
        tk.Label(self.top, text="选择文件格式:").pack(pady=10)
        formats = [("CSV 文件", "csv"), ("Excel 文件", "xlsx")]
        for text, value in formats:
            tk.Radiobutton(self.top, text=text, variable=self.format_var, value=value).pack(anchor=tk.W)

        # 保存按钮
        save_button = tk.Button(self.top, text="保存", command=self.save_file)
        save_button.pack(pady=20)

    def save_file(self):
        # 获取选择的格式
        file_format = self.format_var.get()
        # 创建项目根目录下的userDataFile文件夹路径
        save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "userDataFile")
        os.makedirs(save_dir, exist_ok=True)  # 如果文件夹不存在则创建

        # 根据用户名生成文件路径
        file_path = os.path.join(save_dir, f"{self.username}_data.{file_format}")

        try:
            # 根据选择的格式保存数据
            if file_format == "csv":
                self.finance_data.save_to_csv(file_path)
            elif file_format == "xlsx":
                self.finance_data.save_to_excel(file_path)

            messagebox.showinfo("保存文件", f"文件已成功保存到 {file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"保存文件失败: {e}")
