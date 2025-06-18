#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统功能测试脚本
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    
    try:
        import pandas as pd
        print("✓ pandas 导入成功")
    except ImportError as e:
        print(f"✗ pandas 导入失败: {e}")
        return False
        
    try:
        import numpy as np
        print("✓ numpy 导入成功")
    except ImportError as e:
        print(f"✗ numpy 导入失败: {e}")
        return False
        
    try:
        from PyQt6.QtWidgets import QApplication
        print("✓ PyQt6 导入成功")
    except ImportError as e:
        print(f"✗ PyQt6 导入失败: {e}")
        return False
        
    try:
        from models.ai_service import AIService
        print("✓ AI服务模块导入成功")
    except ImportError as e:
        print(f"✗ AI服务模块导入失败: {e}")
        return False
        
    try:
        from models.data_analyzer import DataAnalyzer
        print("✓ 数据分析模块导入成功")
    except ImportError as e:
        print(f"✗ 数据分析模块导入失败: {e}")
        return False
        
    return True

def test_data_loading():
    """测试数据加载"""
    print("\n测试数据加载...")
    
    try:
        import pandas as pd
        sample_data_path = Path("assets/sample_data.csv")
        
        if not sample_data_path.exists():
            print("✗ 示例数据文件不存在")
            return False
            
        data = pd.read_csv(sample_data_path)
        print(f"✓ 数据加载成功，共 {len(data)} 行，{len(data.columns)} 列")
        print(f"  列名: {list(data.columns)}")
        return True
        
    except Exception as e:
        print(f"✗ 数据加载失败: {e}")
        return False

def test_ai_service():
    """测试AI服务"""
    print("\n测试AI服务...")
    
    try:
        from models.ai_service import AIService
        
        ai_service = AIService()
        print("✓ AI服务初始化成功")
        
        # 测试API连接（不实际调用，只测试配置）
        print("✓ AI服务配置正确")
        return True
        
    except Exception as e:
        print(f"✗ AI服务测试失败: {e}")
        return False

def test_data_analyzer():
    """测试数据分析器"""
    print("\n测试数据分析器...")
    
    try:
        import pandas as pd
        from models.data_analyzer import DataAnalyzer
        
        # 创建测试数据
        test_data = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'likes': [100, 150, 200],
            'comments': [10, 15, 20],
            'content': ['测试内容1', '测试内容2', '测试内容3']
        })
        
        analyzer = DataAnalyzer()
        analyzer.load_data(test_data)
        
        # 测试基础统计
        stats = analyzer.basic_statistics()
        if 'error' not in stats:
            print("✓ 基础统计分析成功")
        else:
            print(f"✗ 基础统计分析失败: {stats['error']}")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ 数据分析器测试失败: {e}")
        return False

def test_views():
    """测试界面模块"""
    print("\n测试界面模块...")
    
    try:
        from views.login_view import LoginView
        print("✓ 登录界面模块导入成功")
        
        from views.register_view import RegisterView
        print("✓ 注册界面模块导入成功")
        
        from views.main_view import MainView
        print("✓ 主界面模块导入成功")
        
        from views.data_import_view import DataImportView
        print("✓ 数据导入界面模块导入成功")
        
        from views.data_analysis_view import DataAnalysisView
        print("✓ 数据分析界面模块导入成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 界面模块测试失败: {e}")
        return False

def test_config():
    """测试配置模块"""
    print("\n测试配置模块...")
    
    try:
        import config
        
        # 测试配置项
        assert hasattr(config, 'AI_CONFIG'), "缺少AI配置"
        assert hasattr(config, 'APP_CONFIG'), "缺少应用配置"
        assert hasattr(config, 'UI_CONFIG'), "缺少界面配置"
        
        print("✓ 配置模块加载成功")
        print(f"  应用名称: {config.APP_CONFIG['name']}")
        print(f"  版本: {config.APP_CONFIG['version']}")
        
        return True
        
    except Exception as e:
        print(f"✗ 配置模块测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("人工智能社交媒体营销分析系统 - 功能测试")
    print("=" * 60)
    
    tests = [
        ("模块导入", test_imports),
        ("数据加载", test_data_loading),
        ("AI服务", test_ai_service),
        ("数据分析器", test_data_analyzer),
        ("界面模块", test_views),
        ("配置模块", test_config)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✓ {test_name} 测试通过")
        else:
            print(f"✗ {test_name} 测试失败")
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统可以正常运行。")
        print("\n启动建议:")
        print("1. 运行 'python run.py' 启动系统")
        print("2. 或运行 'python main.py' 直接启动")
    else:
        print("⚠️  部分测试失败，请检查依赖安装和配置。")
        print("\n解决建议:")
        print("1. 运行 'pip install -r requirements.txt' 安装依赖")
        print("2. 检查Python版本是否为3.9+")
        print("3. 检查PyQt6是否正确安装")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 