import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

class SocialMediaData:
    def __init__(self):
        # 支持的社交媒体平台
        self.platforms = ["综合平台", "微博", "微信", "抖音", "小红书", "B站"]
        
    def generate_sample_data(self, platform, days=30):
        """生成示例社交媒体数据"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        data = {
            '日期': date_range,
            '粉丝数': np.random.randint(1000, 10000, size=len(date_range)),
            '互动量': np.random.randint(100, 1000, size=len(date_range)),
            '曝光量': np.random.randint(10000, 100000, size=len(date_range)),
            '点击率': np.random.uniform(1, 10, size=len(date_range)).round(2),
            '转化率': np.random.uniform(0.1, 5, size=len(date_range)).round(2)
        }
        
        # 根据平台调整数据特征
        if platform == "微博":
            data['转发量'] = np.random.randint(50, 500, size=len(date_range))
            data['评论量'] = np.random.randint(100, 800, size=len(date_range))
            data['点赞量'] = np.random.randint(200, 1500, size=len(date_range))
            
        elif platform == "微信":
            data['阅读量'] = np.random.randint(1000, 10000, size=len(date_range))
            data['在看量'] = np.random.randint(50, 500, size=len(date_range))
            data['分享量'] = np.random.randint(100, 1000, size=len(date_range))
            
        elif platform == "抖音":
            data['播放量'] = np.random.randint(10000, 1000000, size=len(date_range))
            data['完播率'] = np.random.uniform(20, 80, size=len(date_range)).round(2)
            data['平均播放时长'] = np.random.uniform(5, 60, size=len(date_range)).round(2)
            
        elif platform == "小红书":
            data['收藏量'] = np.random.randint(50, 500, size=len(date_range))
            data['关注量'] = np.random.randint(20, 200, size=len(date_range))
            data['搜索量'] = np.random.randint(100, 1000, size=len(date_range))
            
        elif platform == "B站":
            data['播放量'] = np.random.randint(1000, 100000, size=len(date_range))
            data['弹幕量'] = np.random.randint(50, 5000, size=len(date_range))
            data['投币量'] = np.random.randint(20, 2000, size=len(date_range))
            
        return pd.DataFrame(data)
        
    def analyze_data(self, df, platform):
        """分析社交媒体数据"""
        analysis = {}
        
        # 基本统计
        analysis['基本统计'] = {
            '总天数': len(df),
            '平均粉丝数': df['粉丝数'].mean(),
            '平均互动量': df['互动量'].mean(),
            '平均曝光量': df['曝光量'].mean(),
            '平均点击率': df['点击率'].mean(),
            '平均转化率': df['转化率'].mean()
        }
        
        # 增长分析
        latest_followers = df['粉丝数'].iloc[-1]
        initial_followers = df['粉丝数'].iloc[0]
        followers_growth = latest_followers - initial_followers
        followers_growth_rate = (followers_growth / initial_followers) * 100 if initial_followers > 0 else 0
        
        latest_engagement = df['互动量'].iloc[-1]
        initial_engagement = df['互动量'].iloc[0]
        engagement_growth = latest_engagement - initial_engagement
        engagement_growth_rate = (engagement_growth / initial_engagement) * 100 if initial_engagement > 0 else 0
        
        analysis['增长分析'] = {
            '粉丝增长数': followers_growth,
            '粉丝增长率(%)': round(followers_growth_rate, 2),
            '互动量增长数': engagement_growth,
            '互动量增长率(%)': round(engagement_growth_rate, 2)
        }
        
        # 相关性分析
        if platform == "微博":
            analysis['相关性分析'] = {
                '转发量与互动量相关性': round(df['转发量'].corr(df['互动量']), 2),
                '评论量与互动量相关性': round(df['评论量'].corr(df['互动量']), 2),
                '点赞量与互动量相关性': round(df['点赞量'].corr(df['互动量']), 2)
            }
        elif platform == "微信":
            analysis['相关性分析'] = {
                '阅读量与互动量相关性': round(df['阅读量'].corr(df['互动量']), 2),
                '在看量与互动量相关性': round(df['在看量'].corr(df['互动量']), 2),
                '分享量与互动量相关性': round(df['分享量'].corr(df['互动量']), 2)
            }
        elif platform == "抖音":
            analysis['相关性分析'] = {
                '播放量与互动量相关性': round(df['播放量'].corr(df['互动量']), 2),
                '完播率与互动量相关性': round(df['完播率'].corr(df['互动量']), 2),
                '平均播放时长与互动量相关性': round(df['平均播放时长'].corr(df['互动量']), 2)
            }
        elif platform == "小红书":
            analysis['相关性分析'] = {
                '收藏量与互动量相关性': round(df['收藏量'].corr(df['互动量']), 2),
                '关注量与互动量相关性': round(df['关注量'].corr(df['互动量']), 2),
                '搜索量与互动量相关性': round(df['搜索量'].corr(df['互动量']), 2)
            }
        elif platform == "B站":
            analysis['相关性分析'] = {
                '播放量与互动量相关性': round(df['播放量'].corr(df['互动量']), 2),
                '弹幕量与互动量相关性': round(df['弹幕量'].corr(df['互动量']), 2),
                '投币量与互动量相关性': round(df['投币量'].corr(df['互动量']), 2)
            }
        
        # 趋势分析
        weekly_followers = df['粉丝数'].resample('W-MON', on='日期').mean().reset_index().sort_values('日期')
        weekly_engagement = df['互动量'].resample('W-MON', on='日期').mean().reset_index().sort_values('日期')
        
        analysis['趋势分析'] = {
            '粉丝数每周趋势': weekly_followers.to_dict('records'),
            '互动量每周趋势': weekly_engagement.to_dict('records')
        }
        
        return analysis
        
    def prepare_for_ai(self, analysis, platform):
        """为AI分析准备数据"""
        ai_data = f"平台: {platform}\n\n"
        
        # 添加基本统计
        ai_data += "基本统计:\n"
        for key, value in analysis['基本统计'].items():
            ai_data += f"- {key}: {value}\n"
        
        # 添加增长分析
        ai_data += "\n增长分析:\n"
        for key, value in analysis['增长分析'].items():
            ai_data += f"- {key}: {value}\n"
        
        # 添加相关性分析
        ai_data += "\n相关性分析:\n"
        for key, value in analysis['相关性分析'].items():
            ai_data += f"- {key}: {value}\n"
        
        return ai_data    