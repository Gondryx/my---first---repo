# 人工智能社交媒体营销分析系统 - 项目结构

## 📁 项目目录结构

```
social-media-marketing-system/
├── 📄 main.py                    # 主程序入口文件
├── 📄 run.py                     # 备用启动文件
├── 📄 config.py                  # 配置文件（API密钥、数据库设置等）
├── 📄 requirements.txt           # Python依赖包列表
├── 📄 README.md                  # 项目说明文档
├── 📄 .gitignore                 # Git忽略文件
│
├── 📁 docs/                      # 文档目录
│   ├── 📄 PROJECT_STRUCTURE.md   # 项目结构说明（本文件）
│   ├── 📄 DEVELOPMENT_GUIDE.md   # 开发指南
│   └── 📄 PROJECT_STATUS.md      # 项目状态报告
│
├── 📁 scripts/                   # 脚本目录
│   ├── 📄 start.bat             # Windows一键启动脚本
│   └── 📄 clean.bat             # 清理脚本
│
├── 📁 tests/                     # 测试目录
│   ├── 📄 simple_test.py        # 核心功能测试（不依赖PyQt6）
│   └── 📄 test_system.py        # 系统集成测试
│
├── 📁 assets/                    # 资源目录
│   ├── 📄 sample_data.csv       # 示例数据文件
│   └── 📄 social_media_analysis.db # SQLite数据库文件
│
├── 📁 models/                    # 数据模型层
│   ├── 📄 __init__.py
│   ├── 📄 database.py           # 数据库操作类
│   ├── 📄 social_media_data.py  # 社交媒体数据模型
│   ├── 📄 data_analyzer.py      # 数据分析器
│   ├── 📄 ai_service.py         # AI服务接口
│   └── 📄 deepseek_api.py       # DeepSeek API集成
│
├── 📁 views/                     # 用户界面层
│   ├── 📄 __init__.py
│   ├── 📄 login_view.py         # 登录界面
│   ├── 📄 register_view.py      # 注册界面
│   ├── 📄 main_view.py          # 主界面
│   ├── 📄 data_import_view.py   # 数据导入界面
│   └── 📄 data_analysis_view.py # 数据分析界面
│
├── 📁 controllers/               # 控制器层
│   ├── 📄 __init__.py
│   └── 📄 main_controller.py    # 主控制器
│
├── 📁 data/                      # 数据存储目录
│   └── 📄 .gitkeep              # 保持目录存在
├── 📁 logs/                      # 日志文件目录
│   └── 📄 .gitkeep              # 保持目录存在
├── 📁 reports/                   # 报告输出目录
│   └── 📄 .gitkeep              # 保持目录存在
└── 📁 temp/                      # 临时文件目录
    └── 📄 .gitkeep              # 保持目录存在
```

## 🔧 核心文件说明

### 主程序文件
- **main.py**: 系统主入口，启动PyQt6应用程序
- **run.py**: 备用启动文件，提供额外的启动选项
- **config.py**: 集中管理所有配置项，包括API密钥、数据库连接等

### 文档目录 (docs/)
- **PROJECT_STRUCTURE.md**: 项目结构详细说明
- **DEVELOPMENT_GUIDE.md**: 开发指南和最佳实践
- **PROJECT_STATUS.md**: 项目开发进度和功能状态

### 脚本目录 (scripts/)
- **start.bat**: Windows一键启动脚本
- **clean.bat**: 清理临时文件和缓存脚本

### 测试目录 (tests/)
- **simple_test.py**: 核心功能测试，不依赖PyQt6
- **test_system.py**: 系统集成测试

### 资源目录 (assets/)
- **sample_data.csv**: 示例社交媒体数据
- **social_media_analysis.db**: SQLite数据库文件

### 数据模型层 (models/)
- **database.py**: 数据库连接和基础操作
- **social_media_data.py**: 社交媒体数据结构定义
- **data_analyzer.py**: 数据分析和统计功能
- **ai_service.py**: AI服务统一接口
- **deepseek_api.py**: DeepSeek API的具体实现

### 用户界面层 (views/)
- **login_view.py**: 用户登录界面
- **register_view.py**: 用户注册界面
- **main_view.py**: 系统主界面，包含所有功能入口
- **data_import_view.py**: 数据导入和管理界面
- **data_analysis_view.py**: 数据分析和可视化界面

### 控制器层 (controllers/)
- **main_controller.py**: 主控制器，处理业务逻辑和界面交互

## 📊 数据文件
- **assets/sample_data.csv**: 示例社交媒体数据
- **assets/social_media_analysis.db**: SQLite数据库文件

## 🧪 测试文件
- **tests/simple_test.py**: 核心功能测试
- **tests/test_system.py**: 系统集成测试

## 🚀 启动方式

### 推荐启动方式
```bash
# 在项目根目录下运行
python main.py
```

### 使用启动脚本
```bash
# Windows用户可以直接双击
scripts/start.bat

# 或命令行运行
scripts/start.bat
```

### 备用启动方式
```bash
# 使用备用启动文件
python run.py
```

## 📋 依赖管理

### 安装依赖
```bash
pip install -r requirements.txt
```

### 主要依赖包
- PyQt6: GUI框架
- pandas: 数据处理
- matplotlib: 数据可视化
- requests: HTTP请求
- sqlite3: 数据库操作
- numpy: 数值计算
- seaborn: 统计图表

## 🔍 调试和测试

### 测试依赖安装
```bash
python tests/simple_test.py
```

### 测试系统功能
```bash
python tests/test_system.py
```

## 📝 开发规范

1. **文件命名**: 使用下划线命名法 (snake_case)
2. **类命名**: 使用驼峰命名法 (CamelCase)
3. **目录结构**: 按功能模块分层组织
4. **注释**: 重要功能需要添加中文注释
5. **错误处理**: 使用try-except进行异常处理

## 🎯 功能模块

### 已实现功能
- ✅ 用户登录注册
- ✅ 数据导入和管理
- ✅ 基础数据分析
- ✅ AI服务集成
- ✅ 数据可视化
- ✅ 营销策略生成

### 待开发功能
- 🔄 高级数据分析
- 🔄 实时数据监控
- 🔄 报告导出
- 🔄 用户权限管理
- 🔄 数据备份恢复

## 🚀 GitHub上传准备

### 已排除的文件和目录
- `__pycache__/`: Python缓存文件
- `.idea/`: PyCharm IDE配置
- `venv/`: Python虚拟环境
- `*.db`: 数据库文件（在assets目录中）
- `logs/*.log`: 日志文件
- `temp/*`: 临时文件
- `reports/*`: 报告文件

### 保持的目录结构
- 使用`.gitkeep`文件保持空目录的存在
- 所有源代码文件都会被上传
- 文档和脚本文件都会被上传
- 示例数据文件会被上传 