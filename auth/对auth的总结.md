# auth
## Storage 类的数据结构

### 1. 存储位置
- 用户数据存储在 `data/users.json` 文件中。
- 文件路径为项目根目录下的绝对路径。

### 2. 数据结构
- JSON 格式，包含用户的用户名和密码。结构示例：

```json
{
  "username1": "password1",
  "username2": "password2"
}
```

## AuthSystem 类的数据结构

### 1. 依赖
- 依赖于 `User` 类（从 `auth.user` 模块导入）。
- 使用 `storage` 来保存和加载用户数据。

### 2. 属性
- **`storage`**: 存储用户数据的对象。
- **`users`**: 从存储中加载的用户字典。

### 3. 主要方法
- **`__init__(storage)`**: 初始化时加载用户数据。

- **`register(username, password)`**: 
  - 功能: 注册新用户。
  - 检查用户名是否已存在，若存在抛出 `ValueError`。
  - 创建 `User` 对象并将其保存到存储中。
  - 返回 "注册成功" 的消息。

- **`login(username, password)`**: 
  - 功能: 用户登录。
  - 检查用户名和密码是否匹配。
  - 返回 `True` 表示登录成功，返回 `False` 表示登录失败。

### 4. 示例
```python
storage = Storage()  # 假设已有 Storage 类的实例
auth_system = AuthSystem(storage)

# 注册用户
try:
    print(auth_system.register("new_user", "secure_password"))
except ValueError as e:
    print(e)

# 用户登录
if auth_system.login("new_user", "secure_password"):
    print("登录成功")
else:
    print("登录失败")


