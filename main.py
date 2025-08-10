from services.auth_service import AuthService

auth_service = AuthService()

# 示例：注册用户
try:
    print(auth_service.register('user1', 'password123'))
except ValueError as e:
    print(e)

# 示例：登录用户
print(auth_service.login('user1', 'password123'))
