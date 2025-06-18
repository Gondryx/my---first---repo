import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Any, Tuple
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class DataAnalyzer:
    """数据分析类，用于社交媒体数据分析"""
    
    def __init__(self):
        self.data = None
        self.analysis_results = {}
        
    def load_data(self, data: pd.DataFrame):
        """加载数据"""
        self.data = data.copy()
        return True
        
    def basic_statistics(self) -> Dict[str, Any]:
        """基础统计分析"""
        if self.data is None:
            return {"error": "数据未加载"}
            
        stats = {}
        
        # 数据基本信息
        stats["数据形状"] = self.data.shape
        stats["列名"] = self.data.columns.tolist()
        stats["数据类型"] = self.data.dtypes.to_dict()
        
        # 缺失值统计
        missing_data = self.data.isnull().sum()
        stats["缺失值统计"] = missing_data[missing_data > 0].to_dict()
        
        # 数值列统计
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            stats["数值列统计"] = self.data[numeric_cols].describe().to_dict()
            
        # 文本列统计
        text_cols = self.data.select_dtypes(include=['object']).columns
        if len(text_cols) > 0:
            text_stats = {}
            for col in text_cols:
                text_stats[col] = {
                    "唯一值数量": self.data[col].nunique(),
                    "最常见值": self.data[col].mode().iloc[0] if not self.data[col].mode().empty else None,
                    "空值数量": self.data[col].isnull().sum()
                }
            stats["文本列统计"] = text_stats
            
        return stats
        
    def time_series_analysis(self, date_column: str) -> Dict[str, Any]:
        """时间序列分析"""
        if self.data is None or date_column not in self.data.columns:
            return {"error": "数据未加载或日期列不存在"}
            
        try:
            # 转换日期列
            self.data[date_column] = pd.to_datetime(self.data[date_column])
            
            # 按日期分组统计
            daily_stats = self.data.groupby(self.data[date_column].dt.date).size()
            
            # 计算趋势
            trend = np.polyfit(range(len(daily_stats)), daily_stats.values, 1)
            
            # 计算移动平均
            moving_avg = daily_stats.rolling(window=7, min_periods=1).mean()
            
            return {
                "每日数据量": daily_stats.to_dict(),
                "趋势斜率": trend[0],
                "移动平均": moving_avg.to_dict(),
                "总天数": len(daily_stats),
                "平均每日数据量": daily_stats.mean(),
                "最高单日数据量": daily_stats.max(),
                "最低单日数据量": daily_stats.min()
            }
        except Exception as e:
            return {"error": f"时间序列分析失败: {str(e)}"}
            
    def engagement_analysis(self, engagement_columns: List[str]) -> Dict[str, Any]:
        """互动分析"""
        if self.data is None:
            return {"error": "数据未加载"}
            
        engagement_stats = {}
        
        for col in engagement_columns:
            if col in self.data.columns:
                col_data = self.data[col].dropna()
                if len(col_data) > 0:
                    engagement_stats[col] = {
                        "平均值": col_data.mean(),
                        "中位数": col_data.median(),
                        "最大值": col_data.max(),
                        "最小值": col_data.min(),
                        "标准差": col_data.std(),
                        "总和": col_data.sum(),
                        "非零数量": (col_data > 0).sum()
                    }
                    
        # 计算互动率
        if len(engagement_columns) >= 2:
            # 假设第一个是点赞，第二个是评论
            if engagement_columns[0] in self.data.columns and engagement_columns[1] in self.data.columns:
                likes = self.data[engagement_columns[0]].fillna(0)
                comments = self.data[engagement_columns[1]].fillna(0)
                engagement_rate = (likes + comments) / likes.max() * 100
                engagement_stats["互动率"] = {
                    "平均互动率": engagement_rate.mean(),
                    "最高互动率": engagement_rate.max(),
                    "互动率分布": engagement_rate.describe().to_dict()
                }
                
        return engagement_stats
        
    def content_analysis(self, text_column: str) -> Dict[str, Any]:
        """内容分析"""
        if self.data is None or text_column not in self.data.columns:
            return {"error": "数据未加载或文本列不存在"}
            
        try:
            text_data = self.data[text_column].dropna()
            
            # 文本长度分析
            text_lengths = text_data.str.len()
            length_stats = {
                "平均长度": text_lengths.mean(),
                "中位数长度": text_lengths.median(),
                "最长文本": text_lengths.max(),
                "最短文本": text_lengths.min(),
                "长度分布": text_lengths.describe().to_dict()
            }
            
            # 关键词分析（简化版本，不使用jieba）
            all_text = " ".join(text_data.astype(str))
            # 使用简单的分词方法
            words = re.findall(r'\b\w+\b', all_text.lower())
            word_freq = Counter(words)
            
            # 过滤停用词和短词
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours', 'theirs'}
            filtered_words = {word: count for word, count in word_freq.items() 
                            if len(word) > 2 and word not in stop_words and not word.isdigit()}
            
            top_keywords = dict(sorted(filtered_words.items(), key=lambda x: x[1], reverse=True)[:20])
            
            return {
                "文本长度统计": length_stats,
                "关键词频率": top_keywords,
                "总文本数量": len(text_data),
                "平均文本长度": text_lengths.mean()
            }
        except Exception as e:
            return {"error": f"内容分析失败: {str(e)}"}
            
    def sentiment_analysis(self, text_column: str) -> Dict[str, Any]:
        """情感分析"""
        if self.data is None or text_column not in self.data.columns:
            return {"error": "数据未加载或文本列不存在"}
            
        try:
            text_data = self.data[text_column].dropna()
            
            sentiments = []
            for text in text_data[:1000]:  # 限制分析数量
                try:
                    blob = TextBlob(str(text))
                    sentiment = blob.sentiment.polarity
                    sentiments.append(sentiment)
                except:
                    sentiments.append(0)
                    
            sentiment_series = pd.Series(sentiments)
            
            # 情感分类
            positive = (sentiment_series > 0.1).sum()
            negative = (sentiment_series < -0.1).sum()
            neutral = ((sentiment_series >= -0.1) & (sentiment_series <= 0.1)).sum()
            
            return {
                "平均情感得分": sentiment_series.mean(),
                "情感分布": {
                    "正面": positive,
                    "负面": negative,
                    "中性": neutral
                },
                "情感得分统计": sentiment_series.describe().to_dict(),
                "分析样本数": len(sentiments)
            }
        except Exception as e:
            return {"error": f"情感分析失败: {str(e)}"}
            
    def generate_charts(self, chart_type: str, **kwargs) -> Dict[str, Any]:
        """生成图表"""
        if self.data is None:
            return {"error": "数据未加载"}
            
        try:
            if chart_type == "engagement_trend":
                return self._create_engagement_trend_chart(**kwargs)
            elif chart_type == "content_distribution":
                return self._create_content_distribution_chart(**kwargs)
            elif chart_type == "sentiment_pie":
                return self._create_sentiment_pie_chart(**kwargs)
            elif chart_type == "wordcloud":
                return self._create_wordcloud_chart(**kwargs)
            else:
                return {"error": f"不支持的图表类型: {chart_type}"}
        except Exception as e:
            return {"error": f"图表生成失败: {str(e)}"}
            
    def _create_engagement_trend_chart(self, date_column: str, engagement_column: str) -> Dict[str, Any]:
        """创建互动趋势图"""
        try:
            # 按日期分组计算平均互动
            daily_engagement = self.data.groupby(
                pd.to_datetime(self.data[date_column]).dt.date
            )[engagement_column].mean()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_engagement.index,
                y=daily_engagement.values,
                mode='lines+markers',
                name='平均互动数'
            ))
            
            fig.update_layout(
                title="互动趋势分析",
                xaxis_title="日期",
                yaxis_title="平均互动数",
                template="plotly_white"
            )
            
            return {
                "chart_type": "engagement_trend",
                "figure": fig,
                "data": daily_engagement.to_dict()
            }
        except Exception as e:
            return {"error": f"互动趋势图生成失败: {str(e)}"}
            
    def _create_content_distribution_chart(self, column: str) -> Dict[str, Any]:
        """创建内容分布图"""
        try:
            value_counts = self.data[column].value_counts().head(10)
            
            fig = go.Figure(data=[
                go.Bar(x=value_counts.values, y=value_counts.index, orientation='h')
            ])
            
            fig.update_layout(
                title=f"{column}分布",
                xaxis_title="数量",
                yaxis_title=column,
                template="plotly_white"
            )
            
            return {
                "chart_type": "content_distribution",
                "figure": fig,
                "data": value_counts.to_dict()
            }
        except Exception as e:
            return {"error": f"内容分布图生成失败: {str(e)}"}
            
    def _create_sentiment_pie_chart(self, text_column: str) -> Dict[str, Any]:
        """创建情感饼图"""
        try:
            sentiment_result = self.sentiment_analysis(text_column)
            if "error" in sentiment_result:
                return sentiment_result
                
            sentiment_dist = sentiment_result["情感分布"]
            
            fig = go.Figure(data=[go.Pie(
                labels=list(sentiment_dist.keys()),
                values=list(sentiment_dist.values()),
                hole=0.3
            )])
            
            fig.update_layout(
                title="情感分布",
                template="plotly_white"
            )
            
            return {
                "chart_type": "sentiment_pie",
                "figure": fig,
                "data": sentiment_dist
            }
        except Exception as e:
            return {"error": f"情感饼图生成失败: {str(e)}"}
            
    def _create_wordcloud_chart(self, text_column: str) -> Dict[str, Any]:
        """创建词云图"""
        try:
            content_result = self.content_analysis(text_column)
            if "error" in content_result:
                return content_result
                
            word_freq = content_result["关键词频率"]
            
            # 生成词云
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                font_path=None  # 使用默认字体
            ).generate_from_frequencies(word_freq)
            
            # 转换为图像数据
            fig = go.Figure()
            fig.add_trace(go.Image(z=wordcloud.to_array()))
            
            fig.update_layout(
                title="关键词词云",
                template="plotly_white"
            )
            
            return {
                "chart_type": "wordcloud",
                "figure": fig,
                "wordcloud": wordcloud,
                "data": word_freq
            }
        except Exception as e:
            return {"error": f"词云图生成失败: {str(e)}"}
            
    def export_analysis_report(self, output_path: str) -> bool:
        """导出分析报告"""
        try:
            report = {
                "基础统计": self.basic_statistics(),
                "分析结果": self.analysis_results
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                import json
                json.dump(report, f, ensure_ascii=False, indent=2)
                
            return True
        except Exception as e:
            print(f"报告导出失败: {str(e)}")
            return False 