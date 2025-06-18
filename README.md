# 🤖 人工智能社交媒体营销分析系统

一个基于PyQt6开发的智能社交媒体营销分析平台，集成DeepSeek AI API，提供数据导入、分析、可视化和营销策略生成功能。

## ✨ 主要功能

### 🔐 用户管理
- 用户注册和登录
- 安全的密码验证
- 用户会话管理

### 📊 数据管理
- 支持CSV格式数据导入
- 社交媒体数据预处理
- 数据质量检查和清洗

### 📈 数据分析
- 多维度数据统计分析
- 趋势分析和预测
- 用户行为分析
- 内容效果评估

### 🎨 数据可视化
- 交互式图表展示
- 多种图表类型（柱状图、折线图、饼图等）
- 实时数据更新
- 图表导出功能

### 🤖 AI智能分析
- 集成DeepSeek AI API
- 智能内容分析
- 营销策略自动生成
- 竞品分析建议

### 📋 营销策略
- 个性化营销方案
- 目标受众分析
- 内容策略建议
- 投放时间优化

## 🚀 快速开始

### 环境要求
- Python 3.9+
- PyQt6 6.4+
- Windows 10/11

### 安装步骤

1. **克隆项目**
```bash
git clone [项目地址]
cd social-media-marketing-system
```

2. **创建虚拟环境**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置API密钥**
编辑 `config.py` 文件，添加你的DeepSeek API密钥：
```python
DEEPSEEK_API_KEY = "your_api_key_here"
```

5. **启动应用**
```bash
python main.py
```

## �� 项目结构

详细的项目结构请查看 [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

## 🛠️ 技术栈

- **前端框架**: PyQt6
- **数据处理**: pandas, numpy
- **数据可视化**: matplotlib, seaborn
- **AI服务**: DeepSeek API
- **数据库**: SQLite
- **HTTP请求**: requests

## 📖 使用指南

### 1. 用户登录
- 首次使用需要注册账号
- 输入用户名和密码登录系统

### 2. 数据导入
- 点击"数据导入"功能
- 选择CSV格式的社交媒体数据文件
- 系统自动验证数据格式和质量

### 3. 数据分析
- 选择要分析的数据集
- 选择分析维度（时间、平台、内容类型等）
- 查看分析结果和可视化图表

### 4. AI分析
- 点击"AI分析"功能
- 输入分析需求或选择预设分析类型
- 获取AI生成的营销建议

### 5. 营销策略
- 基于分析结果生成营销策略
- 查看策略详情和执行建议
- 导出策略报告

## 🔧 配置说明

### 配置文件 (config.py)
```python
# API配置
DEEPSEEK_API_KEY = "your_api_key"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# 数据库配置
DATABASE_PATH = "assets/social_media_analysis.db"

# 界面配置
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
```

### 数据格式要求
CSV文件应包含以下字段：
- `date`: 发布日期
- `platform`: 平台名称
- `content_type`: 内容类型
- `engagement`: 互动数据
- `reach`: 触达数据
- `conversion`: 转化数据

## 🧪 测试

### 测试依赖安装
```bash
python tests/simple_test.py
```

### 测试系统功能
```bash
python tests/test_system.py
```

### 简单功能测试
```bash
python tests/simple_test.py
```

## 🐛 常见问题

### 1. 依赖安装失败
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 2. PyQt6 DLL加载失败
- 确保安装了Visual C++ Redistributable
- 重新安装PyQt6: `pip uninstall PyQt6 && pip install PyQt6`

### 3. matplotlib后端错误
- 系统会自动设置正确的后端
- 如遇问题，检查matplotlib版本兼容性

### 4. API调用失败
- 检查网络连接
- 验证API密钥是否正确
- 确认API配额是否充足

## 📝 开发说明

### 代码规范
- 使用中文注释
- 遵循PEP 8代码风格
- 类名使用驼峰命名法
- 函数名使用下划线命名法

### 添加新功能
1. 在对应模块中添加功能代码
2. 在控制器中添加业务逻辑
3. 在界面中添加用户交互
4. 更新文档和测试

## 📄 许可证

本项目仅供学习和研究使用。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者

---

**注意**: 使用前请确保已正确配置API密钥，并遵守相关服务条款。 