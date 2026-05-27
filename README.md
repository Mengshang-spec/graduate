<<<<<<< HEAD
﻿# 电商购物平台 · 毕业设计

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](./LICENSE)

基于 Django 框架开发的 B2C 电商购物系统。支持商品浏览、购物车、订单管理、支付宝沙箱支付等功能，是本科毕业设计项目。

---

## 项目简介

本项目是一个面向消费者的在线购物平台，采用 Django MTV 架构，前端使用 HTML/CSS/JS + Bootstrap，后端使用 Django 5.0 + MySQL，集成支付宝沙箱支付。

### 核心功能

- **用户系统**：注册、登录、地址管理、会话保持
- **商品模块**：多级分类、商品列表、商品详情（多规格 SKU：颜色/尺码）、商品图片轮播
- **购物车**：添加商品、修改数量、删除商品、全选/反选
- **订单系统**：订单生成、状态流转（待支付 → 已支付 → 已发货 → 已完成）
- **在线支付**：集成支付宝沙箱支付（电脑网站支付）
- **后台管理**：基于 Django Admin 的商品、订单、用户数据管理

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Django 5.0 |
| 数据库 | MySQL 8.0 |
| 前端 | HTML5 + CSS3 + JavaScript + Bootstrap |
| 支付 | 支付宝沙箱 API（电脑网站支付） |
| 缓存 | Django Session + Cookie |
| 验证码 | Pillow 图片验证码 |

---

## 项目结构

```
zust/
├── djangoProject/                # 主项目
│   ├── djangoProject/            # Django 配置
│   │   ├── settings.py           # 数据库、中间件、静态文件配置
│   │   ├── urls.py               # 路由分发
│   │   └── wsgi.py               # WSGI 入口
│   ├── userapp/                  # 用户模块
│   │   ├── models.py             # UserInfo、Address、Area
│   │   ├── views.py              # 登录、注册、地址管理
│   │   └── urls.py
│   ├── goodsapp/                 # 商品模块
│   │   ├── models.py             # Category、Goods、Inventory、Color、Size
│   │   ├── views.py              # 商品列表、详情、搜索
│   │   └── urls.py
│   ├── cartsapp/                 # 购物车模块
│   │   ├── models.py             # CartItem
│   │   ├── views.py              # 购物车 CRUD
│   │   └── urls.py
│   ├── orderapp/                 # 订单模块
│   │   ├── models.py             # Order、OrderItem
│   │   ├── views.py              # 订单生成、支付回调、状态管理
│   │   └── urls.py
│   ├── utils/                    # 工具
│   │   ├── code.py               # 图片验证码生成
│   │   ├── loaddata.py           # 商品数据批量导入
│   │   └── jiukuaijiu.json       # 商品初始化数据
│   ├── templates/                # 公共模板
│   ├── static/                   # 静态资源
│   └── media/                    # 商品图片上传目录
├── djangoProject1/               # 备选版本 1
├── djangoProject2/               # 备选版本 2
└── README.md
```

---

## 数据库设计

### 核心模型 ER 关系

```
Category（分类）  1 ── N   Goods（商品）
Goods（商品）     1 ── N   Inventory（库存）  N ── 1  Color（颜色）
Goods（商品）     1 ── N   Inventory（库存）  N ── 1  Size（尺码）
Goods（商品）     1 ── N   GoodDetail（详情图）
UserInfo（用户）  1 ── N   Address（地址）
UserInfo（用户）  1 ── N   CartItem（购物车项）
UserInfo（用户）  1 ── N   Order（订单）
Order（订单）     1 ── N   OrderItem（订单项）
Address（地址）   1 ── N   Order（订单）
```

### 模型字段

| 模型 | 关键字段 | 说明 |
|------|---------|------|
| `UserInfo` | uname, pwd | 用户信息 |
| `Address` | aname, aphone, addr, isdefault | 收货地址 |
| `Category` | cname | 商品分类 |
| `Goods` | gname, gdesc, price, oldprice | 商品信息 |
| `Inventory` | count, color(FK), size(FK), goods(FK) | SKU 库存管理 |
| `CartItem` | goodsid, colorid, sizeid, count | 购物车项 |
| `Order` | out_trade_num(UUID), order_num, trade_no, status, payway | 订单（含支付宝流水号） |
| `OrderItem` | goodsid, colorid, sizeid, count | 订单商品明细 |

---

## 快速启动

```bash
# 1. 进入项目
cd zust/zust/djangoProject

# 2. 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate

# 3. 安装依赖
pip install django pillow

# 4. 修改 settings.py 中的数据库配置，创建 MySQL 数据库后执行迁移
python manage.py makemigrations
python manage.py migrate

# 5. 导入商品数据
python manage.py shell
>>> exec(open('utils/loaddata.py').read())
>>> test_model()

# 6. 启动
python manage.py runserver
```

访问 http://127.0.0.1:8000

---

## 页面路由

| 页面 | 路由 |
|------|------|
| 首页/商品列表 | `/goods/` |
| 商品详情 | `/goods/detail/?id=1` |
| 购物车 | `/cart/` |
| 订单确认 | `/order/` |
| 订单列表 | `/order/list/` |
| 登录 | `/user/login/` |
| 注册 | `/user/register/` |
| 地址管理 | `/user/address/` |

---

## License

MIT
=======
# zust
毕业设计
第三个和第一个可以进行使用/n
包含全套的数据代码和内容，请勿抄袭
>>>>>>> c2ea86d9fb8dbb38ea3be0db53b941da558261e1
