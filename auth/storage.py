import json
import os

class Storage:
    def __init__(self, filename='AccountData/users.json'):
        # 获取项目根目录的绝对路径
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 向上两级目录
        self.filename = os.path.join(base_dir, filename)  # 组合为绝对路径
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)  # 确保目录存在

    def save_user(self, user):
        users = self.load_users()
        users[user.username] = user.password
        with open(self.filename, 'w') as f:
            json.dump(users, f)

    def load_users(self):
        if os.path.exists(self.filename):
            if os.path.getsize(self.filename) == 0:  # 文件为空
                return {}
            with open(self.filename, 'r') as f:
                return json.load(f)
        return {}
