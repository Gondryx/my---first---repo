#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek AI API 服务模块
提供与DeepSeek AI的集成功能
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepSeekAPI:
    """DeepSeek AI API 客户端"""
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.deepseek.com"):
        """
        初始化DeepSeek API客户端
        
        Args:
            api_key: API密钥
            base_url: API基础URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            })
    
    def set_api_key(self, api_key: str):
        """设置API密钥"""
        self.api_key = api_key
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def analyze_social_media_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析社交媒体数据
        
        Args:
            data: 社交媒体数据
            
        Returns:
            分析结果
        """
        if not self.api_key:
            return {"error": "API密钥未设置"}
        
        try:
            # 构建分析提示
            prompt = self._build_analysis_prompt(data)
            
            # 调用API
            response = self._call_api(prompt)
            
            return self._parse_analysis_response(response)
            
        except Exception as e:
            logger.error(f"分析社交媒体数据时出错: {str(e)}")
            return {"error": f"分析失败: {str(e)}"}
    
    def generate_marketing_strategy(self, analysis_result: Dict[str, Any], 
                                  target_audience: str = None) -> Dict[str, Any]:
        """
        生成营销策略
        
        Args:
            analysis_result: 数据分析结果
            target_audience: 目标受众
            
        Returns:
            营销策略
        """
        if not self.api_key:
            return {"error": "API密钥未设置"}
        
        try:
            # 构建策略生成提示
            prompt = self._build_strategy_prompt(analysis_result, target_audience)
            
            # 调用API
            response = self._call_api(prompt)
            
            return self._parse_strategy_response(response)
            
        except Exception as e:
            logger.error(f"生成营销策略时出错: {str(e)}")
            return {"error": f"策略生成失败: {str(e)}"}
    
    def generate_content_suggestions(self, topic: str, platform: str, 
                                   content_type: str = "post") -> Dict[str, Any]:
        """
        生成内容建议
        
        Args:
            topic: 主题
            platform: 平台
            content_type: 内容类型
            
        Returns:
            内容建议
        """
        if not self.api_key:
            return {"error": "API密钥未设置"}
        
        try:
            # 构建内容生成提示
            prompt = self._build_content_prompt(topic, platform, content_type)
            
            # 调用API
            response = self._call_api(prompt)
            
            return self._parse_content_response(response)
            
        except Exception as e:
            logger.error(f"生成内容建议时出错: {str(e)}")
            return {"error": f"内容生成失败: {str(e)}"}
    
    def generate_marketing_plan(self, analysis_data: str) -> str:
        """
        生成营销方案
        
        Args:
            analysis_data: 分析数据字符串
            
        Returns:
            营销方案内容
        """
        if not self.api_key:
            return "错误：API密钥未设置，请先在设置中配置API密钥。"
        
        try:
            # 构建营销方案生成提示
            prompt = self._build_marketing_plan_prompt(analysis_data)
            
            # 调用API
            response = self._call_api(prompt, model="deepseek-chat")
            
            # 解析响应
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                return self._format_marketing_plan(content)
            else:
                return "错误：API响应格式异常，请检查网络连接和API配置。"
                
        except Exception as e:
            logger.error(f"生成营销方案时出错: {str(e)}")
            return f"生成营销方案失败: {str(e)}"
    
    def predict_trends(self, prompt: str) -> str:
        """
        预测趋势
        
        Args:
            prompt: 预测提示词
            
        Returns:
            趋势预测结果
        """
        if not self.api_key:
            return "错误：API密钥未设置，请先在设置中配置API密钥。"
        
        try:
            # 构建趋势预测提示
            enhanced_prompt = self._build_trend_prediction_prompt(prompt)
            
            # 调用API
            response = self._call_api(enhanced_prompt, model="deepseek-chat")
            
            # 解析响应
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                return self._format_trend_prediction(content)
            else:
                return "错误：API响应格式异常，请检查网络连接和API配置。"
                
        except Exception as e:
            logger.error(f"预测趋势时出错: {str(e)}")
            return f"趋势预测失败: {str(e)}"
    
    def optimize_content(self, content_data: str, platform: str) -> str:
        """
        优化内容
        
        Args:
            content_data: 内容数据
            platform: 平台名称
            
        Returns:
            优化建议
        """
        if not self.api_key:
            return "错误：API密钥未设置，请先在设置中配置API密钥。"
        
        try:
            # 构建内容优化提示
            prompt = self._build_content_optimization_prompt(content_data, platform)
            
            # 调用API
            response = self._call_api(prompt, model="deepseek-chat")
            
            # 解析响应
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                return self._format_content_optimization(content)
            else:
                return "错误：API响应格式异常，请检查网络连接和API配置。"
                
        except Exception as e:
            logger.error(f"优化内容时出错: {str(e)}")
            return f"内容优化失败: {str(e)}"
    
    def _call_api(self, prompt: str, model: str = "deepseek-chat") -> Dict[str, Any]:
        """
        调用DeepSeek API
        
        Args:
            prompt: 提示词
            model: 模型名称
            
        Returns:
            API响应
        """
        # 保证只拼接一次 /v1/chat/completions
        url = f"{self.base_url.rstrip('/')}/v1/chat/completions"
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API调用失败: {str(e)}")
            raise
    
    def _build_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """构建数据分析提示"""
        prompt = f"""
请分析以下社交媒体数据，并提供详细的分析报告：

数据概览：
- 平台：{data.get('platform', '未知')}
- 时间范围：{data.get('time_range', '未知')}
- 数据量：{data.get('data_count', 0)} 条记录

数据内容：
{json.dumps(data.get('content', {}), ensure_ascii=False, indent=2)}

请从以下角度进行分析：
1. 数据趋势分析
2. 用户行为分析
3. 内容效果分析
4. 竞品分析
5. 机会与挑战识别

请提供结构化的分析报告，包含具体的数据洞察和建议。
"""
        return prompt
    
    def _build_strategy_prompt(self, analysis_result: Dict[str, Any], 
                              target_audience: str = None) -> str:
        """构建策略生成提示"""
        audience_info = f"目标受众：{target_audience}" if target_audience else "目标受众：未指定"
        
        prompt = f"""
基于以下数据分析结果，请生成详细的营销策略：

{audience_info}

分析结果：
{json.dumps(analysis_result, ensure_ascii=False, indent=2)}

请提供以下方面的营销策略：
1. 目标市场定位
2. 内容策略
3. 推广策略
4. 用户增长策略
5. 品牌建设策略
6. 效果评估方案

请提供具体可执行的策略建议，包含时间安排和预期效果。
"""
        return prompt
    
    def _build_content_prompt(self, topic: str, platform: str, 
                             content_type: str) -> str:
        """构建内容生成提示"""
        prompt = f"""
请为以下要求生成社交媒体内容建议：

主题：{topic}
平台：{platform}
内容类型：{content_type}

请提供：
1. 内容标题建议
2. 内容正文建议
3. 标签建议
4. 发布时间建议
5. 互动策略建议

请确保内容符合{platform}平台的特点和用户习惯。
"""
        return prompt
    
    def _parse_analysis_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """解析分析响应"""
        try:
            content = response.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # 尝试解析JSON格式的响应
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # 如果不是JSON格式，返回原始内容
                return {
                    "analysis": content,
                    "status": "success"
                }
                
        except Exception as e:
            logger.error(f"解析分析响应失败: {str(e)}")
            return {"error": f"响应解析失败: {str(e)}"}
    
    def _parse_strategy_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """解析策略响应"""
        try:
            content = response.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # 尝试解析JSON格式的响应
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # 如果不是JSON格式，返回原始内容
                return {
                    "strategy": content,
                    "status": "success"
                }
                
        except Exception as e:
            logger.error(f"解析策略响应失败: {str(e)}")
            return {"error": f"响应解析失败: {str(e)}"}
    
    def _parse_content_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """解析内容响应"""
        try:
            content = response.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # 尝试解析JSON格式的响应
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # 如果不是JSON格式，返回原始内容
                return {
                    "content_suggestions": content,
                    "status": "success"
                }
                
        except Exception as e:
            logger.error(f"解析内容响应失败: {str(e)}")
            return {"error": f"响应解析失败: {str(e)}"}
    
    def test_connection(self) -> bool:
        """测试API连接"""
        try:
            if not self.api_key:
                return False
            
            # 发送简单的测试请求
            test_prompt = "请回复'连接测试成功'"
            response = self._call_api(test_prompt)
            
            content = response.get('choices', [{}])[0].get('message', {}).get('content', '')
            return '连接测试成功' in content
            
        except Exception as e:
            logger.error(f"API连接测试失败: {str(e)}")
            return False
    
    def _build_marketing_plan_prompt(self, analysis_data: str) -> str:
        """构建营销方案生成提示"""
        prompt = f"""
你是一位资深的社交媒体营销专家，请基于以下数据分析结果，生成一份详细、可操作的营销方案。

数据分析结果：
{analysis_data}

请生成一份结构化的营销方案，包含以下部分：

## 1. 市场分析
- 目标受众画像
- 市场机会分析
- 竞争环境评估

## 2. 营销目标
- 短期目标（1-3个月）
- 中期目标（3-6个月）
- 长期目标（6-12个月）

## 3. 内容策略
- 内容主题规划
- 内容类型建议
- 发布频率建议
- 最佳发布时间

## 4. 平台策略
- 各平台重点内容
- 平台特色功能利用
- 跨平台协同策略

## 5. 互动策略
- 用户互动方式
- 评论回复策略
- 粉丝增长策略

## 6. 数据分析与优化
- 关键指标监控
- 效果评估方法
- 持续优化建议

## 7. 预算与资源
- 人力投入建议
- 工具推荐
- 预算分配建议

## 8. 风险控制
- 潜在风险识别
- 应对措施
- 应急预案

请确保方案：
- 基于数据分析结果
- 具有可操作性
- 包含具体建议
- 语言简洁明了
- 适合中文社交媒体环境

请直接输出完整的营销方案，不要包含任何解释性文字。
"""
        return prompt
    
    def _build_trend_prediction_prompt(self, user_prompt: str) -> str:
        """构建趋势预测提示"""
        enhanced_prompt = f"""
你是一位资深的社交媒体趋势分析师，请基于你的专业知识和行业经验，对以下趋势预测请求进行分析和预测。

用户请求：{user_prompt}

请提供一份详细的趋势预测报告，包含以下内容：

## 1. 趋势概述
- 主要趋势总结
- 变化驱动因素
- 影响范围评估

## 2. 具体趋势分析
- 内容形式趋势
- 用户行为变化
- 平台功能演进
- 营销方式创新

## 3. 行业影响
- 对品牌营销的影响
- 对内容创作者的影响
- 对用户习惯的影响
- 对平台生态的影响

## 4. 应对策略
- 品牌应对建议
- 内容策略调整
- 技术工具准备
- 团队能力建设

## 5. 机会与挑战
- 新机会识别
- 潜在风险预警
- 竞争优势构建
- 资源投入建议

## 6. 时间节点
- 短期变化（1-3个月）
- 中期趋势（3-6个月）
- 长期展望（6-12个月）

请确保预测：
- 基于行业趋势
- 具有前瞻性
- 包含具体建议
- 语言专业准确
- 适合中国市场

请直接输出完整的趋势预测报告，不要包含任何解释性文字。
"""
        return enhanced_prompt
    
    def _build_content_optimization_prompt(self, content_data: str, platform: str) -> str:
        """构建内容优化提示"""
        prompt = f"""
你是一位资深的社交媒体内容优化专家，请基于以下内容数据和平台特点，提供详细的内容优化建议。

平台：{platform}
内容数据：{content_data}

请提供一份全面的内容优化方案，包含以下部分：

## 1. 内容质量分析
- 内容优势识别
- 改进空间分析
- 质量评分建议

## 2. 标题优化
- 标题吸引力提升
- 关键词优化
- A/B测试建议

## 3. 内容结构优化
- 开头吸引力
- 内容逻辑性
- 结尾引导性

## 4. 视觉元素优化
- 图片/视频建议
- 色彩搭配
- 排版布局

## 5. 互动元素优化
- 互动引导
- 话题标签
- 用户参与

## 6. 平台适配优化
- 平台特色功能
- 算法偏好
- 用户习惯

## 7. 发布策略优化
- 最佳发布时间
- 发布频率
- 内容节奏

## 8. 效果监控
- 关键指标
- 优化方向
- 持续改进

请确保建议：
- 针对性强
- 可操作性强
- 基于平台特点
- 包含具体示例
- 语言简洁明了

请直接输出完整的优化建议，不要包含任何解释性文字。
"""
        return prompt
    
    def _format_marketing_plan(self, content: str) -> str:
        """格式化营销方案"""
        # 清理和格式化内容
        content = content.strip()
        
        # 确保有适当的标题格式
        if not content.startswith('#') and not content.startswith('##'):
            content = f"# 营销方案\n\n{content}"
        
        return content
    
    def _format_trend_prediction(self, content: str) -> str:
        """格式化趋势预测"""
        # 清理和格式化内容
        content = content.strip()
        
        # 确保有适当的标题格式
        if not content.startswith('#') and not content.startswith('##'):
            content = f"# 趋势预测报告\n\n{content}"
        
        return content
    
    def _format_content_optimization(self, content: str) -> str:
        """格式化内容优化建议"""
        # 清理和格式化内容
        content = content.strip()
        
        # 确保有适当的标题格式
        if not content.startswith('#') and not content.startswith('##'):
            content = f"# 内容优化建议\n\n{content}"
        
        return content

    def _build_prompt(self, content, platform, content_type):
        """
        构建AI提示词，内容更丰富，确保长度大于100
        """
        prompt = (
            f"请针对{platform}平台的{content_type}内容，生成一份高质量的社交媒体营销方案。\n"
            f"内容要求：\n"
            f"{content}\n"
            f"请结构化输出，包含以下部分：\n"
            f"1. 目标（明确本次营销的核心目标）\n"
            f"2. 受众分析（描述目标用户画像、兴趣、行为等）\n"
            f"3. 内容策略（内容类型、风格、主题、发布时间建议等）\n"
            f"4. 渠道与推广（平台选择、推广方式、合作建议等）\n"
            f"5. 执行计划（时间表、资源分配、关键节点）\n"
            f"6. 预期效果与评估（KPI、数据监控、优化建议）\n"
            f"请用条理清晰的分点方式详细展开，每一部分都要有具体建议和理由。\n"
            f"示例：\n"
            f"1. 目标：提升品牌曝光度，增加粉丝互动率。\n"
            f"2. 受众分析：目标用户为18-30岁年轻群体，活跃于短视频平台，关注时尚与科技。\n"
            f"3. 内容策略：以趣味短视频为主，结合热点话题，定期发布互动话题。\n"
            f"4. 渠道与推广：主推抖音、小红书，联合KOL进行话题扩散。\n"
            f"5. 执行计划：每周三次内容更新，月度线上活动一次。\n"
            f"6. 预期效果与评估：粉丝增长10%，互动率提升20%，每月复盘优化。"
        )
        return prompt

    def _send_request(self, prompt):
        """
        模拟API请求（测试用）
        """
        # 实际生产环境应实现真实API调用
        return "模拟API响应"


# 创建全局API实例
deepseek_api = DeepSeekAPI() 