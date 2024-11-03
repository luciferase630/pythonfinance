import json
import os

class FinanceData:
    def __init__(self, username):
        # 获取顶级目录路径
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.filename = os.path.join(base_dir, 'data', f'{username}_finance.json')
        self.data = self.load_financial_data()

    def load_financial_data(self):
        """加载财务数据，如果文件不存在则创建一个新的文件"""
        if os.path.exists(self.filename):
            if os.path.getsize(self.filename) == 0:  # 文件为空
                return {}  # 返回空字典
            with open(self.filename, 'r') as f:
                return json.load(f)
        else:
            # 如果文件不存在，创建一个新的文件
            self.save_financial_data({})
            return {}

    def save_financial_data(self, data=None):
        """将财务数据保存到文件"""
        if data is not None:
            self.data = data  # 更新数据
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)

    def add_entry(self, entry):
        """添加一条财务记录"""
        if 'entries' not in self.data:
            self.data['entries'] = []
        self.data['entries'].append(entry)
        self.save_financial_data()

    def get_entries(self):
        """获取所有财务记录"""
        return self.data.get('entries', [])
    def create_file_if_not_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)  # 创建一个空的 JSON 文件

    def load_data(self):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        return data