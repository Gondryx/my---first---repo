#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化功能测试脚本 - 不依赖PyQt6
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_core_modules():
    """测试核心模块"""
    print("测试核心模块...")
    
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

def test_data_analysis():
    """测试数据分析功能"""
    print("\n测试数据分析功能...")
    
    try:
        import pandas as pd
        from models.data_analyzer import DataAnalyzer
        
        # 加载示例数据
        sample_data_path = Path("assets/sample_data.csv")
        if not sample_data_path.exists():
            print("✗ 示例数据文件不存在")
            return False
            
        data = pd.read_csv("assets/sample_data.csv")
        print(f"✓ 数据加载成功，共 {len(data)} 行，{len(data.columns)} 列")
        
        # 测试数据分析器
        analyzer = DataAnalyzer()
        analyzer.load_data(data)
        
        # 测试基础统计
        stats = analyzer.basic_statistics()
        if 'error' not in stats:
            print("✓ 基础统计分析成功")
            print(f"  数据形状: {stats['数据形状']}")
        else:
            print(f"✗ 基础统计分析失败: {stats['error']}")
            return False
            
        # 测试互动分析
        engagement_stats = analyzer.engagement_analysis(['点赞数', '评论数'])
        if 'error' not in engagement_stats:
            print("✓ 互动分析成功")
        else:
            print(f"✗ 互动分析失败: {engagement_stats['error']}")
            
        # 测试内容分析
        content_stats = analyzer.content_analysis('内容')
        if 'error' not in content_stats:
            print("✓ 内容分析成功")
        else:
            print(f"✗ 内容分析失败: {content_stats['error']}")
            
        return True
        
    except Exception as e:
        print(f"✗ 数据分析测试失败: {e}")
        return False

def test_ai_service():
    """测试AI服务"""
    print("\n测试AI服务...")
    
    try:
        from models.ai_service import AIService
        
        ai_service = AIService()
        print("✓ AI服务初始化成功")
        
        # 测试API配置
        print(f"✓ API密钥配置: {ai_service.api_key[:10]}...")
        print(f"✓ API地址: {ai_service.base_url}")
        
        return True
        
    except Exception as e:
        print(f"✗ AI服务测试失败: {e}")
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
        print(f"  AI API密钥: {config.AI_CONFIG['api_key'][:10]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ 配置模块测试失败: {e}")
        return False

def test_sample_data():
    """测试示例数据"""
    print("\n测试示例数据...")
    
    try:
        import pandas as pd
        
        data = pd.read_csv("assets/sample_data.csv")
        
        # 检查数据质量
        print(f"✓ 数据行数: {len(data)}")
        print(f"✓ 数据列数: {len(data.columns)}")
        print(f"✓ 列名: {list(data.columns)}")
        
        # 检查数据类型
        print(f"✓ 数据类型:")
        for col, dtype in data.dtypes.items():
            print(f"  {col}: {dtype}")
            
        # 检查缺失值
        missing = data.isnull().sum()
        if missing.sum() == 0:
            print("✓ 无缺失值")
        else:
            print(f"⚠ 缺失值统计: {missing[missing > 0].to_dict()}")
            
        return True
        
    except Exception as e:
        print(f"✗ 示例数据测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("人工智能社交媒体营销分析系统 - 核心功能测试")
    print("=" * 60)
    
    tests = [
        ("核心模块", test_core_modules),
        ("示例数据", test_sample_data),
        ("数据分析", test_data_analysis),
        ("AI服务", test_ai_service),
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
        print("🎉 所有核心功能测试通过！")
        print("\n系统核心功能正常，可以继续开发GUI界面。")
        print("\n下一步建议:")
        print("1. 解决PyQt6安装问题")
        print("2. 运行 'python main.py' 启动完整系统")
        print("3. 或使用 'python run.py' 启动")
    else:
        print("⚠️  部分测试失败，请检查依赖安装。")
        print("\n解决建议:")
        print("1. 运行 'pip install -r requirements.txt' 安装依赖")
        print("2. 检查Python版本是否为3.9+")
        print("3. 确保所有依赖包正确安装")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 