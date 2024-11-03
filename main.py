from auth.storage import Storage
from auth.auth_system import AuthSystem

storage = Storage()
auth_system = AuthSystem(storage)

# 示例：注册用户
try:
    print(auth_system.register('user1', 'password123'))
except ValueError as e:
    print(e)

# 示例：登录用户
print(auth_system.login('user1', 'password123'))
