#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成器模块
支持生成多种格式的分析报告和营销方案报告
"""

import os
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import seaborn as sns
from pathlib import Path

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self):
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 设置图表样式
        sns.set_style("whitegrid")
        plt.style.use('seaborn-v0_8')
        
    def generate_analysis_report(self, analysis_data: Dict[str, Any], 
                               df: pd.DataFrame, platform: str,
                               include_charts: bool = True,
                               include_tables: bool = True,
                               include_recommendations: bool = True) -> str:
        """
        生成数据分析报告
        
        Args:
            analysis_data: 分析结果数据
            df: 原始数据DataFrame
            platform: 平台名称
            include_charts: 是否包含图表
            include_tables: 是否包含表格
            include_recommendations: 是否包含建议
            
        Returns:
            报告内容字符串
        """
        report_content = []
        
        # 报告标题
        report_content.append(f"# {platform}平台社交媒体数据分析报告")
        report_content.append("")
        report_content.append(f"**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report_content.append(f"**数据平台**: {platform}")
        report_content.append(f"**数据量**: {len(df)} 条记录")
        report_content.append("")
        
        # 报告概述
        report_content.append("## 📊 报告概述")
        report_content.append("")
        report_content.append("本报告基于社交媒体数据分析，从多个维度深入分析了数据特征、")
        report_content.append("用户行为模式和内容效果表现，为营销策略制定提供数据支撑。")
        report_content.append("")
        
        # 基本统计信息
        if include_tables:
            report_content.append("## 📈 基本统计信息")
            report_content.append("")
            
            # 数据概览表格
            report_content.append("### 数据概览")
            report_content.append("")
            report_content.append("| 指标 | 数值 |")
            report_content.append("|------|------|")
            report_content.append(f"| 总数据量 | {len(df)} 条 |")
            report_content.append(f"| 平均互动量 | {df['engagement'].mean():.0f} |")
            report_content.append(f"| 最高互动量 | {df['engagement'].max():.0f} |")
            report_content.append(f"| 最低互动量 | {df['engagement'].min():.0f} |")
            report_content.append(f"| 互动量标准差 | {df['engagement'].std():.0f} |")
            report_content.append("")
            
            # 平台分布表格
            if 'platform' in df.columns and df['platform'].nunique() > 1:
                platform_stats = df.groupby('platform')['engagement'].agg(['count', 'mean', 'max']).round(0)
                report_content.append("### 平台分布统计")
                report_content.append("")
                report_content.append("| 平台 | 数据量 | 平均互动量 | 最高互动量 |")
                report_content.append("|------|--------|------------|------------|")
                for platform_name, stats in platform_stats.iterrows():
                    report_content.append(f"| {platform_name} | {stats['count']} | {stats['mean']:.0f} | {stats['max']:.0f} |")
                report_content.append("")
            
            # 内容类型分布表格
            if 'content_type' in df.columns:
                content_stats = df.groupby('content_type')['engagement'].agg(['count', 'mean']).round(0)
                report_content.append("### 内容类型分布")
                report_content.append("")
                report_content.append("| 内容类型 | 数据量 | 平均互动量 |")
                report_content.append("|----------|--------|------------|")
                for content_type, stats in content_stats.iterrows():
                    report_content.append(f"| {content_type} | {stats['count']} | {stats['mean']:.0f} |")
                report_content.append("")
        
        # 详细分析结果
        report_content.append("## 🔍 详细分析结果")
        report_content.append("")
        
        # 基本统计
        if 'overview' in analysis_data:
            report_content.append("### 基本统计分析")
            report_content.append("")
            for key, value in analysis_data['overview'].items():
                report_content.append(f"- **{key}**: {value}")
            report_content.append("")
        
        # 增长分析
        if 'growth' in analysis_data:
            report_content.append("### 增长趋势分析")
            report_content.append("")
            for key, value in analysis_data['growth'].items():
                report_content.append(f"- **{key}**: {value}")
            report_content.append("")
        
        # 相关性分析
        if 'correlation' in analysis_data:
            report_content.append("### 相关性分析")
            report_content.append("")
            for key, value in analysis_data['correlation'].items():
                report_content.append(f"- **{key}**: {value}")
            report_content.append("")
        
        # 趋势分析
        if 'trends' in analysis_data:
            report_content.append("### 趋势分析")
            report_content.append("")
            for key, value in analysis_data['trends'].items():
                report_content.append(f"- **{key}**: {value}")
            report_content.append("")
        
        # 图表分析
        if include_charts:
            report_content.append("## 📊 图表分析")
            report_content.append("")
            report_content.append("### 互动量分布")
            report_content.append("")
            report_content.append("![互动量分布](engagement_distribution.png)")
            report_content.append("")
            
            report_content.append("### 平台对比")
            report_content.append("")
            report_content.append("![平台对比](platform_comparison.png)")
            report_content.append("")
            
            report_content.append("### 内容类型效果")
            report_content.append("")
            report_content.append("![内容类型效果](content_type_analysis.png)")
            report_content.append("")
        
        # 关键发现
        report_content.append("## 💡 关键发现")
        report_content.append("")
        
        # 基于数据生成关键发现
        key_findings = self._generate_key_findings(df, analysis_data)
        for i, finding in enumerate(key_findings, 1):
            report_content.append(f"{i}. {finding}")
        report_content.append("")
        
        # 建议和策略
        if include_recommendations:
            report_content.append("## 🎯 建议和策略")
            report_content.append("")
            
            recommendations = self._generate_recommendations(df, analysis_data, platform)
            for category, recs in recommendations.items():
                report_content.append(f"### {category}")
                report_content.append("")
                for rec in recs:
                    report_content.append(f"- {rec}")
                report_content.append("")
        
        # 结论
        report_content.append("## 📝 结论")
        report_content.append("")
        report_content.append("基于以上分析，我们得出以下主要结论：")
        report_content.append("")
        
        conclusions = self._generate_conclusions(df, analysis_data, platform)
        for i, conclusion in enumerate(conclusions, 1):
            report_content.append(f"{i}. {conclusion}")
        report_content.append("")
        
        # 附录
        report_content.append("## 📋 附录")
        report_content.append("")
        report_content.append("### 数据来源")
        report_content.append(f"- 平台: {platform}")
        report_content.append(f"- 数据量: {len(df)} 条")
        report_content.append(f"- 时间范围: {df['date'].min() if 'date' in df.columns else '未知'} 至 {df['date'].max() if 'date' in df.columns else '未知'}")
        report_content.append("")
        
        report_content.append("### 分析方法")
        report_content.append("- 描述性统计分析")
        report_content.append("- 相关性分析")
        report_content.append("- 趋势分析")
        report_content.append("- 对比分析")
        report_content.append("")
        
        return "\n".join(report_content)
    
    def generate_marketing_plan_report(self, plan_data: str, plan_name: str,
                                     analysis_data: Optional[Dict[str, Any]] = None) -> str:
        """
        生成营销方案报告
        
        Args:
            plan_data: 营销方案内容
            plan_name: 方案名称
            analysis_data: 分析数据（可选）
            
        Returns:
            报告内容字符串
        """
        report_content = []
        
        # 报告标题
        report_content.append(f"# {plan_name}")
        report_content.append("")
        report_content.append(f"**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report_content.append(f"**方案类型**: 社交媒体营销方案")
        report_content.append("")
        
        # 方案概述
        report_content.append("## 📋 方案概述")
        report_content.append("")
        report_content.append("本营销方案基于社交媒体数据分析结果，结合行业最佳实践，")
        report_content.append("为品牌在社交媒体平台上的营销活动提供全面的策略指导。")
        report_content.append("")
        
        # 分析基础（如果有分析数据）
        if analysis_data:
            report_content.append("## 📊 分析基础")
            report_content.append("")
            report_content.append("### 数据概览")
            report_content.append("")
            if 'overview' in analysis_data:
                for key, value in analysis_data['overview'].items():
                    report_content.append(f"- **{key}**: {value}")
            report_content.append("")
        
        # 营销方案内容
        report_content.append("## 🎯 营销方案")
        report_content.append("")
        report_content.append(plan_data)
        report_content.append("")
        
        # 执行计划
        report_content.append("## 📅 执行计划")
        report_content.append("")
        report_content.append("### 第一阶段（1-2周）")
        report_content.append("- 团队组建和培训")
        report_content.append("- 内容策略制定")
        report_content.append("- 平台账号准备")
        report_content.append("")
        
        report_content.append("### 第二阶段（3-4周）")
        report_content.append("- 内容制作和发布")
        report_content.append("- 用户互动管理")
        report_content.append("- 数据监控开始")
        report_content.append("")
        
        report_content.append("### 第三阶段（5-8周）")
        report_content.append("- 策略优化调整")
        report_content.append("- 效果评估分析")
        report_content.append("- 下一阶段规划")
        report_content.append("")
        
        # 风险控制
        report_content.append("## ⚠️ 风险控制")
        report_content.append("")
        report_content.append("### 潜在风险")
        report_content.append("- 内容质量不达标")
        report_content.append("- 用户反馈负面")
        report_content.append("- 平台政策变化")
        report_content.append("- 竞品策略调整")
        report_content.append("")
        
        report_content.append("### 应对措施")
        report_content.append("- 建立内容审核机制")
        report_content.append("- 及时响应用户反馈")
        report_content.append("- 关注平台动态")
        report_content.append("- 定期竞品分析")
        report_content.append("")
        
        # 附录
        report_content.append("## 📋 附录")
        report_content.append("")
        report_content.append("### 工具推荐")
        report_content.append("- 内容创作工具")
        report_content.append("- 数据分析工具")
        report_content.append("- 发布管理工具")
        report_content.append("- 监控分析工具")
        report_content.append("")
        
        report_content.append("### 参考资料")
        report_content.append("- 行业最佳实践")
        report_content.append("- 平台官方指南")
        report_content.append("- 成功案例分析")
        report_content.append("")
        
        return "\n".join(report_content)
    
    def generate_combined_report(self, analysis_data: Dict[str, Any], 
                               df: pd.DataFrame, platform: str,
                               plan_data: Optional[str] = None,
                               plan_name: Optional[str] = None) -> str:
        """
        生成综合分析报告
        
        Args:
            analysis_data: 分析结果数据
            df: 原始数据DataFrame
            platform: 平台名称
            plan_data: 营销方案内容（可选）
            plan_name: 方案名称（可选）
            
        Returns:
            报告内容字符串
        """
        report_content = []
        
        # 报告标题
        report_content.append(f"# {platform}平台社交媒体营销综合分析报告")
        report_content.append("")
        report_content.append(f"**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report_content.append(f"**数据平台**: {platform}")
        report_content.append(f"**数据量**: {len(df)} 条记录")
        report_content.append("")
        
        # 执行摘要
        report_content.append("## 📋 执行摘要")
        report_content.append("")
        report_content.append("本报告整合了社交媒体数据分析结果和AI生成的营销方案，")
        report_content.append("为品牌提供全面的营销策略指导。报告包含数据分析、")
        report_content.append("趋势洞察、营销策略和执行建议等核心内容。")
        report_content.append("")
        
        # 数据分析部分
        analysis_report = self.generate_analysis_report(
            analysis_data, df, platform, 
            include_charts=False, include_tables=True, include_recommendations=False
        )
        
        # 提取分析报告的主要内容部分
        analysis_lines = analysis_report.split('\n')
        start_idx = 0
        end_idx = len(analysis_lines)
        
        # 找到详细分析结果部分
        for i, line in enumerate(analysis_lines):
            if "## 🔍 详细分析结果" in line:
                start_idx = i
                break
        
        # 找到结论部分
        for i, line in enumerate(analysis_lines[start_idx:], start_idx):
            if "## 📝 结论" in line:
                end_idx = i
                break
        
        report_content.extend(analysis_lines[start_idx:end_idx])
        report_content.append("")
        
        # 营销方案部分
        if plan_data and plan_name:
            report_content.append("## 🎯 营销方案")
            report_content.append("")
            report_content.append(f"### {plan_name}")
            report_content.append("")
            report_content.append(plan_data)
            report_content.append("")
        
        # 综合建议
        report_content.append("## 💡 综合建议")
        report_content.append("")
        
        combined_recommendations = self._generate_combined_recommendations(
            df, analysis_data, platform, plan_data
        )
        
        for category, recs in combined_recommendations.items():
            report_content.append(f"### {category}")
            report_content.append("")
            for rec in recs:
                report_content.append(f"- {rec}")
            report_content.append("")
        
        # 实施路线图
        report_content.append("## 🗺️ 实施路线图")
        report_content.append("")
        
        roadmap = self._generate_implementation_roadmap(df, analysis_data, platform)
        for phase, tasks in roadmap.items():
            report_content.append(f"### {phase}")
            report_content.append("")
            for task in tasks:
                report_content.append(f"- {task}")
            report_content.append("")
        
        # 成功指标
        report_content.append("## 📊 成功指标")
        report_content.append("")
        report_content.append("### 关键绩效指标(KPI)")
        report_content.append("")
        kpis = self._generate_kpis(df, analysis_data, platform)
        for kpi in kpis:
            report_content.append(f"- {kpi}")
        report_content.append("")
        
        # 附录
        report_content.append("## 📋 附录")
        report_content.append("")
        report_content.append("### 数据详情")
        report_content.append(f"- 数据来源: {platform}")
        report_content.append(f"- 数据量: {len(df)} 条")
        report_content.append(f"- 分析维度: {len(analysis_data)} 个")
        report_content.append("")
        
        return "\n".join(report_content)
    
    def save_report(self, report_content: str, file_path: str, format_type: str = "markdown") -> bool:
        """
        保存报告到文件
        
        Args:
            report_content: 报告内容
            file_path: 文件路径
            format_type: 文件格式
            
        Returns:
            是否保存成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 根据格式保存文件
            if format_type.lower() == "markdown":
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
            elif format_type.lower() == "html":
                html_content = self._convert_to_html(report_content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            elif format_type.lower() == "txt":
                # 移除Markdown标记
                txt_content = self._convert_to_plain_text(report_content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(txt_content)
            else:
                # 默认保存为Markdown
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
            
            return True
            
        except Exception as e:
            print(f"保存报告失败: {str(e)}")
            return False
    
    def _generate_key_findings(self, df: pd.DataFrame, analysis_data: Dict[str, Any]) -> List[str]:
        """生成关键发现"""
        findings = []
        
        # 基于数据生成发现
        avg_engagement = df['engagement'].mean()
        max_engagement = df['engagement'].max()
        
        findings.append(f"平均互动量为 {avg_engagement:.0f}，最高互动量达到 {max_engagement:.0f}")
        
        if 'platform' in df.columns and df['platform'].nunique() > 1:
            best_platform = df.groupby('platform')['engagement'].mean().idxmax()
            findings.append(f"{best_platform}平台表现最佳，互动效果显著")
        
        if 'content_type' in df.columns:
            best_content = df.groupby('content_type')['engagement'].mean().idxmax()
            findings.append(f"{best_content}类型内容最受欢迎，互动率最高")
        
        if 'sentiment' in df.columns:
            sentiment_dist = df['sentiment'].value_counts()
            dominant_sentiment = sentiment_dist.index[0]
            findings.append(f"情感倾向以{dominant_sentiment}为主，占比{sentiment_dist[dominant_sentiment]/sentiment_dist.sum()*100:.1f}%")
        
        return findings
    
    def _generate_recommendations(self, df: pd.DataFrame, analysis_data: Dict[str, Any], platform: str) -> Dict[str, List[str]]:
        """生成建议和策略"""
        recommendations = {
            "内容策略": [],
            "发布策略": [],
            "互动策略": [],
            "平台策略": []
        }
        
        # 内容策略建议
        if 'content_type' in df.columns:
            best_content = df.groupby('content_type')['engagement'].mean().idxmax()
            recommendations["内容策略"].append(f"增加{best_content}类型内容的比重")
        
        # 发布策略建议
        if 'date' in df.columns:
            recommendations["发布策略"].append("分析最佳发布时间，优化发布节奏")
        
        # 互动策略建议
        recommendations["互动策略"].append("建立用户互动机制，及时回复评论")
        recommendations["互动策略"].append("举办线上活动，提升用户参与度")
        
        # 平台策略建议
        recommendations["平台策略"].append(f"深耕{platform}平台，建立品牌影响力")
        recommendations["平台策略"].append("考虑多平台布局，扩大传播范围")
        
        return recommendations
    
    def _generate_conclusions(self, df: pd.DataFrame, analysis_data: Dict[str, Any], platform: str) -> List[str]:
        """生成结论"""
        conclusions = []
        
        conclusions.append(f"数据表明{platform}平台具有较好的营销潜力")
        conclusions.append("用户互动活跃，内容传播效果良好")
        conclusions.append("需要持续优化内容策略，提升用户粘性")
        conclusions.append("建议建立长期的内容营销体系")
        
        return conclusions
    
    def _generate_combined_recommendations(self, df: pd.DataFrame, analysis_data: Dict[str, Any], 
                                         platform: str, plan_data: Optional[str]) -> Dict[str, List[str]]:
        """生成综合建议"""
        recommendations = {
            "数据分析洞察": [],
            "营销策略建议": [],
            "执行要点": [],
            "风险控制": []
        }
        
        # 数据分析洞察
        avg_engagement = df['engagement'].mean()
        recommendations["数据分析洞察"].append(f"平均互动量{avg_engagement:.0f}，表现良好")
        recommendations["数据分析洞察"].append("用户参与度高，内容传播效果好")
        
        # 营销策略建议
        recommendations["营销策略建议"].append("制定差异化内容策略")
        recommendations["营销策略建议"].append("建立用户互动机制")
        recommendations["营销策略建议"].append("优化发布时间和频率")
        
        # 执行要点
        recommendations["执行要点"].append("组建专业内容团队")
        recommendations["执行要点"].append("建立数据监控体系")
        recommendations["执行要点"].append("定期评估和优化策略")
        
        # 风险控制
        recommendations["风险控制"].append("建立内容审核机制")
        recommendations["风险控制"].append("关注用户反馈")
        recommendations["风险控制"].append("监控竞品动态")
        
        return recommendations
    
    def _generate_implementation_roadmap(self, df: pd.DataFrame, analysis_data: Dict[str, Any], platform: str) -> Dict[str, List[str]]:
        """生成实施路线图"""
        roadmap = {
            "第一阶段（1-2周）": [
                "团队组建和培训",
                "内容策略制定",
                "平台账号准备",
                "工具和系统搭建"
            ],
            "第二阶段（3-4周）": [
                "内容制作和发布",
                "用户互动管理",
                "数据监控开始",
                "初步效果评估"
            ],
            "第三阶段（5-8周）": [
                "策略优化调整",
                "效果评估分析",
                "用户反馈收集",
                "下一阶段规划"
            ]
        }
        
        return roadmap
    
    def _generate_kpis(self, df: pd.DataFrame, analysis_data: Dict[str, Any], platform: str) -> List[str]:
        """生成关键绩效指标"""
        kpis = [
            "互动量增长率 ≥ 20%",
            "粉丝增长率 ≥ 15%",
            "内容发布频率 ≥ 每日3条",
            "用户回复率 ≥ 80%",
            "内容质量评分 ≥ 8分"
        ]
        
        return kpis
    
    def _convert_to_html(self, markdown_content: str) -> str:
        """转换为HTML格式"""
        html_content = f"""
<!DOCTYPE html>
<html lang=\"zh-CN\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>社交媒体营销分析报告</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; margin: 40px; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        h3 {{ color: #7f8c8d; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
        blockquote {{ border-left: 4px solid #3498db; margin: 20px 0; padding-left: 20px; }}
    </style>
</head>
<body>
{markdown_content.replace('# ', '<h1>').replace('## ', '<h2>').replace('### ', '<h3>')}
</body>
</html>
        """
        return html_content
    
    def _convert_to_plain_text(self, markdown_content: str) -> str:
        """转换为纯文本格式"""
        # 简单的Markdown到纯文本转换
        text_content = markdown_content
        text_content = text_content.replace('# ', '')
        text_content = text_content.replace('## ', '')
        text_content = text_content.replace('### ', '')
        text_content = text_content.replace('**', '')
        text_content = text_content.replace('*', '')
        text_content = text_content.replace('|', ' ')
        text_content = text_content.replace('- ', '• ')
        
        return text_content 