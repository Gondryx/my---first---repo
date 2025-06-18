# 🛠️ 开发指南

## 📋 开发环境设置

### 1. 环境要求
- Python 3.9+
- PyQt6 6.4+
- Git
- IDE推荐：PyCharm、VS Code

### 2. 开发环境搭建
```bash
# 克隆项目
git clone [项目地址]
cd social-media-marketing-system

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install black flake8 pytest
```

## 🏗️ 项目架构

### MVC架构模式
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Views       │    │   Controllers   │    │     Models      │
│   (用户界面)     │◄──►│   (业务逻辑)     │◄──►│   (数据模型)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 目录结构说明
- **views/**: 用户界面层，负责界面展示和用户交互
- **controllers/**: 控制器层，处理业务逻辑和界面交互
- **models/**: 数据模型层，负责数据处理和业务规则

## 📝 代码规范

### 1. 命名规范
```python
# 文件名：使用下划线命名法
data_analyzer.py
main_controller.py

# 类名：使用驼峰命名法
class DataAnalyzer:
class MainController:

# 函数名：使用下划线命名法
def analyze_data():
def generate_report():

# 变量名：使用下划线命名法
user_data = {}
analysis_result = []
```

### 2. 注释规范
```python
class DataAnalyzer:
    """数据分析器类
    
    负责处理社交媒体数据的各种分析功能
    """
    
    def analyze_engagement(self, data):
        """分析互动数据
        
        Args:
            data (DataFrame): 包含互动数据的DataFrame
            
        Returns:
            dict: 分析结果字典
        """
        pass
```

### 3. 错误处理
```python
try:
    result = self.api_call()
except requests.RequestException as e:
    logger.error(f"API调用失败: {e}")
    QMessageBox.warning(self, "错误", "网络连接失败，请检查网络设置")
except Exception as e:
    logger.error(f"未知错误: {e}")
    QMessageBox.critical(self, "错误", "系统发生未知错误")
```

## 🔧 开发流程

### 1. 添加新功能
1. **在models层添加数据模型**
```python
# models/new_feature.py
class NewFeatureModel:
    def __init__(self):
        pass
    
    def process_data(self, data):
        # 数据处理逻辑
        pass
```

2. **在controllers层添加业务逻辑**
```python
# controllers/main_controller.py
def handle_new_feature(self):
    """处理新功能"""
    try:
        model = NewFeatureModel()
        result = model.process_data(self.data)
        self.update_ui(result)
    except Exception as e:
        self.show_error(f"处理失败: {e}")
```

3. **在views层添加用户界面**
```python
# views/main_view.py
def setup_new_feature_ui(self):
    """设置新功能界面"""
    self.new_feature_button = QPushButton("新功能")
    self.new_feature_button.clicked.connect(self.controller.handle_new_feature)
```

### 2. 修改现有功能
1. 先理解现有代码结构
2. 在对应层进行修改
3. 确保向后兼容
4. 更新相关文档

### 3. 测试新功能
```python
# test_new_feature.py
def test_new_feature():
    """测试新功能"""
    model = NewFeatureModel()
    test_data = create_test_data()
    result = model.process_data(test_data)
    assert result is not None
```

## 🧪 测试指南

### 1. 单元测试
```python
import unittest
from models.data_analyzer import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = DataAnalyzer()
    
    def test_analyze_engagement(self):
        """测试互动数据分析"""
        test_data = pd.DataFrame({
            'engagement': [100, 200, 300]
        })
        result = self.analyzer.analyze_engagement(test_data)
        self.assertIsNotNone(result)
        self.assertIn('total_engagement', result)
```

### 2. 集成测试
```python
def test_full_workflow():
    """测试完整工作流程"""
    # 1. 导入数据
    # 2. 分析数据
    # 3. 生成报告
    # 4. 验证结果
    pass
```

### 3. 运行测试
```bash
# 运行所有测试
python -m pytest

# 运行特定测试
python -m pytest test_data_analyzer.py

# 生成测试报告
python -m pytest --html=report.html
```

## 🔍 调试技巧

### 1. 日志调试
```python
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_function():
    logger.debug("开始执行函数")
    # 函数逻辑
    logger.debug("函数执行完成")
```

### 2. PyQt6调试
```python
# 启用Qt调试信息
import os
os.environ['QT_LOGGING_RULES'] = '*.debug=true;qt.*.debug=false'

# 使用QDebug
from PyQt6.QtCore import QDebug
qDebug() << "调试信息"
```

### 3. 断点调试
在IDE中设置断点，或使用pdb：
```python
import pdb

def problematic_function():
    pdb.set_trace()  # 设置断点
    # 代码逻辑
```

## 📦 打包发布

### 1. 使用PyInstaller打包
```bash
# 安装PyInstaller
pip install pyinstaller

# 打包应用
pyinstaller --onefile --windowed main.py

# 打包为目录
pyinstaller --onedir main.py
```

### 2. 创建安装包
```bash
# 使用Inno Setup创建安装程序
# 或使用NSIS等其他工具
```

## 🔄 版本控制

### 1. Git工作流
```bash
# 创建功能分支
git checkout -b feature/new-feature

# 提交更改
git add .
git commit -m "添加新功能: 描述"

# 合并到主分支
git checkout main
git merge feature/new-feature
```

### 2. 提交信息规范
```
feat: 添加新功能
fix: 修复bug
docs: 更新文档
style: 代码格式调整
refactor: 代码重构
test: 添加测试
chore: 构建过程或辅助工具的变动
```

## 🚀 性能优化

### 1. 数据处理优化
```python
# 使用向量化操作
import numpy as np

# 慢的方式
for i in range(len(data)):
    data[i] = data[i] * 2

# 快的方式
data = data * 2
```

### 2. 界面响应优化
```python
# 使用QThread处理耗时操作
from PyQt6.QtCore import QThread, pyqtSignal

class DataProcessThread(QThread):
    finished = pyqtSignal(object)
    
    def run(self):
        # 耗时操作
        result = self.process_data()
        self.finished.emit(result)
```

### 3. 内存优化
```python
# 及时释放大对象
import gc

def process_large_data():
    data = load_large_data()
    result = process(data)
    del data  # 释放内存
    gc.collect()  # 强制垃圾回收
    return result
```

## 📚 学习资源

### 1. PyQt6文档
- [PyQt6官方文档](https://doc.qt.io/qtforpython/)
- [PyQt6教程](https://doc.qt.io/qtforpython/tutorials/)

### 2. 数据处理
- [Pandas文档](https://pandas.pydata.org/docs/)
- [NumPy文档](https://numpy.org/doc/)

### 3. 数据可视化
- [Matplotlib文档](https://matplotlib.org/stable/contents.html)
- [Seaborn文档](https://seaborn.pydata.org/)

## 🤝 贡献指南

### 1. 提交Issue
- 描述问题或建议
- 提供复现步骤
- 附上错误日志

### 2. 提交Pull Request
- 创建功能分支
- 编写测试用例
- 更新相关文档
- 确保代码通过所有测试

### 3. 代码审查
- 检查代码质量
- 验证功能正确性
- 确保文档完整性

---

**注意**: 开发过程中请遵循项目规范，保持代码质量和可维护性。 