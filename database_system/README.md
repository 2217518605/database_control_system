# 数据库实例管理系统

企业内部数据库实例的管理后台，Django + DRF 实现

## 环境

- Python 3.11 / Django 5.2
- MySQL 8.0
- Redis（Celery 用）

## 跑起来

先建库，字符集要 utf8mb4：

```sql
CREATE DATABASE database_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

装依赖、配环境变量：

```bash
pip install -r requirements.txt
cp .env.example .env
```

`.env` 里的 FERNET_KEY 用这行生成后填进去：

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

然后：

```bash
python manage.py migrate
python manage.py runserver
```

后台在 http://127.0.0.1:8000/admin/

> Windows 上 mysqlclient 装不上的话，换 PyMySQL，在项目入口调一下 `install_as_MySQLdb()`。

## 目录

```
database_system/
├── database_system/    # settings、urls
├── common/             # BaseModel
└── assets/             # 业务代码
```
