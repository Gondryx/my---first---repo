#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人工智能社交媒体营销分析系统启动脚本
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        ('PyQt6', 'PyQt6'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('requests', 'requests'),
        ('openai', 'openai'),
        ('plotly', 'plotly'),
        ('wordcloud', 'wordcloud'),
        ('sklearn', 'scikit-learn'),  # scikit-learn的导入名是sklearn
        ('textblob', 'textblob'),
        ('nltk', 'nltk')
    ]
    
    missing_packages = []
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("缺少以下依赖包:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n请运行以下命令安装依赖:")
        print("python -m pip install -r requirements.txt")
        return False
    
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("人工智能社交媒体营销分析系统")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        input("按回车键退出...")
        return
    
    try:
        # 导入主程序
        from main import main as app_main
        print("启动应用程序...")
        app_main()
    except Exception as e:
        print(f"启动失败: {str(e)}")
        input("按回车键退出...")

if __name__ == "__main__":
    main() 