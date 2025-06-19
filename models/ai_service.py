import requests
import json
import pandas as pd
from typing import Dict, List, Any, Optional
import logging

class AIService:
    """AI服务类，用于处理DeepSeek API调用"""
    
    def __init__(self, api_key: str = "sk-dfc4e38245414faf8290bb291db1a35e"):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    def analyze_social_media_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """分析社交媒体数据"""
        try:
            # 准备数据摘要
            data_summary = self._prepare_data_summary(data)
            
            prompt = f"""
            请分析以下社交媒体数据并提供营销建议：
            
            数据摘要：
            {data_summary}
            
            请提供以下分析：
            1. 数据趋势分析
            2. 用户行为洞察
            3. 内容表现评估
            4. 营销策略建议
            5. 优化建议
            
            请用中文回答，格式要清晰易读。
            """
            
            response = self._call_api(prompt)
            return {
                "success": True,
                "analysis": response,
                "data_summary": data_summary
            }
        except Exception as e:
            logging.error(f"AI分析失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_marketing_strategy(self, target_audience: str, platform: str, goals: str) -> Dict[str, Any]:
        """生成营销策略"""
        try:
            prompt = f"""
            请为以下营销需求制定详细的策略方案：
            
            目标受众：{target_audience}
            平台：{platform}
            营销目标：{goals}
            
            请提供：
            1. 目标受众分析
            2. 内容策略
            3. 发布计划
            4. 互动策略
            5. 效果评估指标
            6. 预算分配建议
            
            请用中文回答，格式要清晰易读。
            """
            
            response = self._call_api(prompt)
            return {
                "success": True,
                "strategy": response
            }
        except Exception as e:
            logging.error(f"策略生成失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_competitor(self, competitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """竞争对手分析"""
        try:
            prompt = f"""
            请分析以下竞争对手数据：
            
            竞争对手信息：
            {json.dumps(competitor_data, ensure_ascii=False, indent=2)}
            
            请提供：
            1. 竞争对手优势分析
            2. 市场定位分析
            3. 内容策略分析
            4. 差异化建议
            5. 机会点识别
            
            请用中文回答，格式要清晰易读。
            """
            
            response = self._call_api(prompt)
            return {
                "success": True,
                "analysis": response
            }
        except Exception as e:
            logging.error(f"竞争对手分析失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_content_ideas(self, topic: str, platform: str, target_audience: str) -> Dict[str, Any]:
        """生成内容创意"""
        try:
            prompt = f"""
            请为以下需求生成内容创意：
            
            主题：{topic}
            平台：{platform}
            目标受众：{target_audience}
            
            请提供：
            1. 10个内容创意标题
            2. 每个创意的核心要点
            3. 内容形式建议
            4. 发布时机建议
            5. 预期效果评估
            
            请用中文回答，格式要清晰易读。
            """
            
            response = self._call_api(prompt)
            return {
                "success": True,
                "ideas": response
            }
        except Exception as e:
            logging.error(f"内容创意生成失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def sentiment_analysis(self, text_data: List[str]) -> Dict[str, Any]:
        """情感分析"""
        try:
            # 将文本数据合并
            combined_text = "\n".join(text_data[:10])  # 限制前10条
            
            prompt = f"""
            请对以下社交媒体文本进行情感分析：
            
            文本内容：
            {combined_text}
            
            请提供：
            1. 整体情感倾向（正面/负面/中性）
            2. 情感强度评分（1-10）
            3. 主要情感关键词
            4. 情感变化趋势
            5. 改进建议
            
            请用中文回答，格式要清晰易读。
            """
            
            response = self._call_api(prompt)
            return {
                "success": True,
                "sentiment": response
            }
        except Exception as e:
            logging.error(f"情感分析失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _call_api(self, prompt: str) -> str:
        """调用DeepSeek API"""
        try:
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"API调用失败: {response.status_code} - {response.text}")
                
        except Exception as e:
            logging.error(f"API调用异常: {str(e)}")
            raise e
    
    def _prepare_data_summary(self, data: pd.DataFrame) -> str:
        """准备数据摘要"""
        try:
            summary = []
            summary.append(f"数据总行数: {len(data)}")
            summary.append(f"数据列数: {len(data.columns)}")
            summary.append(f"列名: {', '.join(data.columns.tolist())}")
            
            # 数值列统计
            numeric_cols = data.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                summary.append(f"数值列: {', '.join(numeric_cols.tolist())}")
                for col in numeric_cols[:3]:  # 只显示前3个数值列
                    summary.append(f"{col} - 平均值: {data[col].mean():.2f}, 最大值: {data[col].max():.2f}")
            
            # 文本列统计
            text_cols = data.select_dtypes(include=['object']).columns
            if len(text_cols) > 0:
                summary.append(f"文本列: {', '.join(text_cols.tolist())}")
                for col in text_cols[:2]:  # 只显示前2个文本列
                    unique_count = data[col].nunique()
                    summary.append(f"{col} - 唯一值数量: {unique_count}")
            
            return "\n".join(summary)
        except Exception as e:
            return f"数据摘要生成失败: {str(e)}" 