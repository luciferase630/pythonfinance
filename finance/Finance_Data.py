import json
import os

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
