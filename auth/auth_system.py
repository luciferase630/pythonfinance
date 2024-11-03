from auth.user import User


class AuthSystem:
    def __init__(self, storage):
        self.storage = storage
        self.users = self.storage.load_users()

    def register(self, username, password):
        if username in self.users:
            raise ValueError("用户名已存在")
        user = User(username, password)
        self.users[username] = user.password
        self.storage.save_user(user)
        return "注册成功"

    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            return True  # 登录成功
        return False  # 登录失败
