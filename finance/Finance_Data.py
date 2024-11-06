import csv
import json
import os
import pandas as pd
class FinanceData:
    def __init__(self, username):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.filename = os.path.join(base_dir, 'FinancialData', f'{username}_finance.json')
        self.data = self.load_financial_data()

    def load_financial_data(self):
        if os.path.exists(self.filename):
            if os.path.getsize(self.filename) == 0:  # 文件为空
                return []  # 返回空列表
            with open(self.filename, 'r') as f:
                return json.load(f)
        else:
            self.save_financial_data([])  # 创建一个空的列表
            return []

    def save_financial_data(self, data=None):
        if data is not None:
            self.data = data  # 更新数据
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)

    def add_entry(self, entry):
        if isinstance(self.data, list):  # 确保数据是一个列表
            self.data.append(entry)
        else:
            self.data['entries'] = self.data.get('entries', [])  #加载进来之后是一个字典里面套列表
            self.data['entries'].append(entry)
        self.save_financial_data()

    def get_entries(self):
        return self.data if isinstance(self.data, list) else self.data.get('entries', [])

    def load_data(self):
        return self.get_entries()

    def save_to_csv(self, file_path):
        """将数据保存为 CSV 文件"""
        with open(file_path, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["日期", "类型", "金额", "备注"])  # CSV 标题

            # 遍历数据中的 "entries" 列表
            for entry in self.data.get("entries", []):
                # 每个条目是一个字典，确保正确访问键
                writer.writerow([
                    entry.get("date", ""),
                    entry.get("type", ""),
                    entry.get("amount", ""),
                    entry.get("note", "")
                ])

    def save_to_excel(self, file_path):
        """将数据保存为 Excel 文件"""
        # 将数据转换为 DataFrame
        df = pd.DataFrame(self.get_entries())
        df.to_excel(file_path, index=False, sheet_name="财务数据")

    def save_to_json(self, file_path):
        """将数据保存为 JSON 文件"""
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def clear_all_entries(self):
        """清空所有预算条目"""
        self.data = {"entries": []}  # 将 entries 列表置为空
        self.save_financial_data()  # 保存清空后的数据到文件
