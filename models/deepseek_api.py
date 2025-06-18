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
    
    def _call_api(self, prompt: str, model: str = "deepseek-chat") -> Dict[str, Any]:
        """
        调用DeepSeek API
        
        Args:
            prompt: 提示词
            model: 模型名称
            
        Returns:
            API响应
        """
        url = f"{self.base_url}/v1/chat/completions"
        
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


# 创建全局API实例
deepseek_api = DeepSeekAPI() 