#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动创建GitHub Issues脚本
"""

import requests
import json
import os
from typing import Dict, List

class GitHubIssuesCreator:
    def __init__(self, token: str, repo: str):
        """
        初始化GitHub Issues创建器
        
        Args:
            token: GitHub个人访问令牌
            repo: 仓库名称 (格式: owner/repo)
        """
        self.token = token
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
    
    def create_issue(self, title: str, body: str, labels: List[str] = None) -> Dict:
        """
        创建单个Issue
        
        Args:
            title: Issue标题
            body: Issue内容
            labels: 标签列表
            
        Returns:
            创建的Issue信息
        """
        url = f"{self.base_url}/repos/{self.repo}/issues"
        data = {
            "title": title,
            "body": body
        }
        
        if labels:
            data["labels"] = labels
            
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 201:
            print(f"✅ 成功创建Issue: {title}")
            return response.json()
        else:
            print(f"❌ 创建Issue失败: {title}")
            print(f"错误信息: {response.text}")
            return None
    
    def create_all_issues(self):
        """创建所有预定义的Issues"""
        
        issues_data = [
            {
                "title": "🚀 高级数据分析功能",
                "body": """## 功能描述
实现更高级的数据分析功能，提升系统的分析能力。

## 功能需求
- [ ] 情感分析功能
- [ ] 关键词提取和分析
- [ ] 用户画像分析
- [ ] 竞品分析功能
- [ ] 趋势预测算法

## 技术实现
- 集成NLTK或spaCy进行文本分析
- 使用机器学习模型进行情感分析
- 实现关键词提取算法
- 添加数据可视化图表

## 优先级
高

## 预计工时
2-3周""",
                "labels": ["enhancement", "data-analysis", "priority-high"]
            },
            {
                "title": "📊 实时数据监控",
                "body": """## 功能描述
实现实时数据监控功能，支持动态数据更新和异常检测。

## 功能需求
- [ ] 实时数据更新机制
- [ ] 数据监控面板
- [ ] 异常检测算法
- [ ] 预警机制
- [ ] 数据流处理

## 技术实现
- 使用WebSocket或轮询机制
- 实现数据流处理管道
- 添加异常检测算法
- 创建实时监控界面

## 优先级
中

## 预计工时
3-4周""",
                "labels": ["enhancement", "real-time", "monitoring"]
            },
            {
                "title": "📄 报告导出功能",
                "body": """## 功能描述
实现多种格式的报告导出功能，支持PDF、Excel等格式。

## 功能需求
- [ ] PDF报告生成
- [ ] Excel报告导出
- [ ] 自定义报告模板
- [ ] 报告定时发送
- [ ] 报告预览功能

## 技术实现
- 使用reportlab或weasyprint生成PDF
- 使用openpyxl或xlsxwriter生成Excel
- 实现模板引擎
- 添加邮件发送功能

## 优先级
中

## 预计工时
2周""",
                "labels": ["enhancement", "export", "reports"]
            },
            {
                "title": "🔐 用户权限管理",
                "body": """## 功能描述
实现完整的用户权限管理系统，支持角色管理和数据访问控制。

## 功能需求
- [ ] 用户角色管理
- [ ] 权限控制机制
- [ ] 数据访问控制
- [ ] 操作日志记录
- [ ] 用户组管理

## 技术实现
- 设计权限模型
- 实现RBAC权限系统
- 添加操作审计日志
- 创建权限管理界面

## 优先级
中

## 预计工时
2-3周""",
                "labels": ["enhancement", "security", "user-management"]
            },
            {
                "title": "🔄 数据同步功能",
                "body": """## 功能描述
实现多平台数据同步功能，支持自动数据更新和备份恢复。

## 功能需求
- [ ] 多平台数据同步
- [ ] 自动数据更新
- [ ] 数据备份恢复
- [ ] 数据版本管理
- [ ] 同步状态监控

## 技术实现
- 实现数据同步API
- 添加定时任务调度
- 实现数据备份机制
- 创建同步监控界面

## 优先级
低

## 预计工时
3-4周""",
                "labels": ["enhancement", "data-sync", "integration"]
            },
            {
                "title": "🐛 大数据量处理性能优化",
                "body": """## 问题描述
当处理大量数据时，系统响应速度较慢，需要优化性能。

## 问题表现
- 数据导入速度慢
- 分析过程卡顿
- 内存占用过高
- 界面响应延迟

## 解决方案
- [ ] 实现数据分页处理
- [ ] 优化数据库查询
- [ ] 添加数据缓存机制
- [ ] 实现异步处理
- [ ] 优化内存使用

## 优先级
高

## 预计工时
1-2周""",
                "labels": ["bug", "performance", "priority-high"]
            },
            {
                "title": "⚡ 界面响应速度优化",
                "body": """## 问题描述
某些界面操作响应较慢，影响用户体验。

## 问题表现
- 界面切换延迟
- 图表加载缓慢
- 按钮响应延迟
- 滚动卡顿

## 解决方案
- [ ] 优化界面渲染
- [ ] 实现懒加载
- [ ] 添加加载动画
- [ ] 优化事件处理
- [ ] 使用多线程处理

## 优先级
中

## 预计工时
1周""",
                "labels": ["bug", "ui", "performance"]
            },
            {
                "title": "💬 错误提示信息完善",
                "body": """## 问题描述
部分错误提示信息不够清晰，用户难以理解问题原因。

## 问题表现
- 错误信息过于技术化
- 缺少解决方案提示
- 错误位置不明确
- 缺少用户指导

## 解决方案
- [ ] 优化错误信息文案
- [ ] 添加解决方案提示
- [ ] 实现错误定位功能
- [ ] 创建错误处理指南
- [ ] 添加用户帮助文档

## 优先级
中

## 预计工时
1周""",
                "labels": ["bug", "user-experience", "documentation"]
            },
            {
                "title": "🧪 兼容性测试",
                "body": """## 问题描述
需要在不同操作系统和Python版本上进行兼容性测试。

## 测试范围
- [ ] Windows 10/11
- [ ] macOS
- [ ] Linux (Ubuntu/CentOS)
- [ ] Python 3.9/3.10/3.11
- [ ] 不同分辨率屏幕

## 测试内容
- [ ] 安装部署测试
- [ ] 功能运行测试
- [ ] 性能对比测试
- [ ] 界面显示测试
- [ ] 错误处理测试

## 优先级
中

## 预计工时
1周""",
                "labels": ["bug", "testing", "compatibility"]
            },
            {
                "title": "📚 文档完善",
                "body": """## 功能描述
需要完善用户手册、API文档和部署文档。

## 文档需求
- [ ] 用户使用手册
- [ ] API接口文档
- [ ] 部署安装指南
- [ ] 故障排除指南
- [ ] 开发者文档

## 内容要求
- [ ] 详细的操作步骤
- [ ] 截图和示例
- [ ] 常见问题解答
- [ ] 视频教程
- [ ] 多语言支持

## 优先级
低

## 预计工时
2周""",
                "labels": ["documentation", "user-guide"]
            }
        ]
        
        print("🚀 开始创建GitHub Issues...")
        print(f"📁 目标仓库: {self.repo}")
        print("=" * 50)
        
        created_count = 0
        failed_count = 0
        
        for i, issue_data in enumerate(issues_data, 1):
            print(f"\n📝 创建Issue {i}/{len(issues_data)}: {issue_data['title']}")
            
            result = self.create_issue(
                title=issue_data['title'],
                body=issue_data['body'],
                labels=issue_data['labels']
            )
            
            if result:
                created_count += 1
            else:
                failed_count += 1
        
        print("\n" + "=" * 50)
        print(f"✅ 创建成功: {created_count} 个")
        print(f"❌ 创建失败: {failed_count} 个")
        print(f"📊 总计: {len(issues_data)} 个")
        
        if created_count > 0:
            print(f"\n🎉 Issues创建完成！")
            print(f"🔗 查看Issues: https://github.com/{self.repo}/issues")

def main():
    """主函数"""
    print("🤖 GitHub Issues 自动创建工具")
    print("=" * 40)
    
    # 获取GitHub Token
    token = input("请输入GitHub个人访问令牌 (Personal Access Token): ").strip()
    if not token:
        print("❌ 请输入有效的GitHub Token")
        return
    
    # 获取仓库信息
    repo = input("请输入仓库名称 (格式: owner/repo): ").strip()
    if not repo or '/' not in repo:
        print("❌ 请输入正确的仓库名称格式，例如: Gondryx/my---first---repo")
        return
    
    # 创建Issues
    creator = GitHubIssuesCreator(token, repo)
    creator.create_all_issues()

if __name__ == "__main__":
    main() 