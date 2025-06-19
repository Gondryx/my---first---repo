# 🧠 MediaSage

一个基于PyQt6开发的智能社交媒体营销分析平台，集成DeepSeek AI API，提供数据导入、分析、可视化和营销策略生成功能。

## ✨ 主要功能

- 用户注册、登录与会话管理
- 支持CSV格式数据导入与清洗
- 多维度数据统计、趋势分析与预测
- 交互式数据可视化（柱状图、折线图、饼图等）
- DeepSeek AI智能内容分析与营销策略生成
- 个性化营销方案与报告导出

---

## 🚀 快速上手

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

---

## 📁 项目结构

```
social-media-marketing-system/
├── assets/                # 示例数据与数据库
├── config.py              # 配置文件
├── controllers/           # 控制器（业务逻辑）
├── docs/                  # 文档（仅保留USER_MANUAL.md）
├── logs/                  # 日志
├── main.py                # 主入口
├── models/                # 数据与AI分析模型
├── reports/               # 导出报告
├── requirements.txt       # 依赖
├── run.py                 # 启动脚本
├── scripts/               # 辅助脚本
├── temp/                  # 临时文件
├── tests/                 # 测试
├── views/                 # 界面模块
└── README.md              # 项目说明
```

---

## 📝 开发说明

- 遵循PEP 8代码风格，类名用驼峰，函数名用下划线
- 主要依赖：PyQt6、pandas、matplotlib、scikit-learn、wordcloud、nltk、seaborn、openai
- 代码注释为中文
- 新功能开发流程：
  1. 在models/controllers/views中添加功能代码
  2. 控制器实现业务逻辑
  3. 界面实现用户交互
  4. 更新文档和测试

---

## 📖 用户手册

详见 [docs/USER_MANUAL.md](docs/USER_MANUAL.md)

---

## 🛠️ 常见问题与解决

- 依赖安装失败：
  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
  ```
- PyQt6 DLL加载失败：安装VC++运行库，重装PyQt6
- matplotlib后端错误：系统自动设置，或检查matplotlib版本
- API调用失败：检查网络、API密钥与配额

---

## 📊 项目状态

- MediaSage 已支持数据导入、分析、可视化、AI策略生成等主要功能
- 支持多平台、多内容类型分析
- 代码结构清晰，便于二次开发
- 后续将持续优化界面与AI能力

---

## 📞 技术支持

- 用户手册：docs/USER_MANUAL.md
- GitHub Issues提交问题
- 日志文件：logs/app.log

---

**本项目持续更新，欢迎反馈建议！**
