import json
import os
import sys


class Storage:
    def __init__(self, filename='Accountdata/users.json'):
        # 处理打包后的路径问题
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.filename = os.path.join(base_dir, filename)

        # 确保目录存在
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def save_user(self, user):
        users = self.load_users()
        users[user.username] = user.password
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

    def load_users(self):
        if os.path.exists(self.filename):
            if os.path.getsize(self.filename) == 0:  # 文件为空
                return {}
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
