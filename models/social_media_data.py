import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

class SocialMediaData:
    def __init__(self):
        # 支持的社交媒体平台
        self.platforms = ["综合平台", "微博", "微信", "抖音", "小红书", "B站"]
        
        # 标准字段映射
        self.field_mapping = {
            'date': ['日期', '发布时间', 'date', 'time', '发布时间'],
            'platform': ['平台', 'platform', '社交媒体平台'],
            'content_type': ['内容类型', 'content_type', '类型'],
            'engagement': ['互动量', 'engagement', '互动数据', '点赞数', '评论数', '转发数'],
            'reach': ['触达量', 'reach', '曝光量', '阅读量', '播放量'],
            'conversion': ['转化量', 'conversion', '转化数据'],
            'content': ['内容', 'content', '文本内容', '内容文本'],
            'user_type': ['用户类型', 'user_type', '用户'],
            'sentiment': ['情感倾向', 'sentiment', '情感', '情绪'],
            'followers': ['粉丝数', 'followers', '关注者', '粉丝']
        }
        
    def import_csv_data(self, file_path, encoding='utf-8', separator=',', has_header=True):
        """导入CSV数据文件"""
        try:
            # 读取CSV文件
            if has_header:
                df = pd.read_csv(file_path, encoding=encoding, sep=separator)
            else:
                df = pd.read_csv(file_path, encoding=encoding, sep=separator, header=None)
            print(f"[DEBUG] 初始df.columns: {list(df.columns)}")
            # 验证数据格式
            validation_result = self.validate_data_format(df)
            print(f"[DEBUG] 验证结果: {validation_result}")
            if not validation_result['valid']:
                return validation_result
            # 标准化字段名
            df = self.standardize_columns(df)
            print(f"[DEBUG] 标准化后df.columns: {list(df.columns)}")
            # 数据清洗
            df = self.clean_data(df)
            print(f"[DEBUG] 清洗后df.columns: {list(df.columns)}")
            return {
                'valid': True,
                'data': df,
                'message': f"成功导入 {len(df)} 条数据",
                'columns': list(df.columns),
                'sample': df.head(5).to_dict('records')
            }
        except Exception as e:
            import traceback
            print(f"[ERROR] import_csv_data异常: {str(e)}")
            traceback.print_exc()
            return {
                'valid': False,
                'error': f"导入失败: {str(e)}",
                'message': "请检查文件格式和编码"
            }
    
    def validate_data_format(self, df):
        """验证数据格式"""
        if df.empty:
            return {'valid': False, 'error': '数据文件为空'}
            
        if len(df.columns) < 3:
            return {'valid': False, 'error': '数据列数不足，至少需要3列'}
            
        # 检查是否有必要的字段
        required_fields = ['date', 'platform', 'content']
        found_fields = []
        
        for field in required_fields:
            for col in df.columns:
                if any(keyword in col.lower() for keyword in self.field_mapping.get(field, [field])):
                    found_fields.append(field)
                    break
                    
        if len(found_fields) < 2:
            return {
                'valid': False, 
                'error': f'缺少必要字段，需要包含日期、平台或内容字段。当前字段: {list(df.columns)}'
            }
            
        return {'valid': True, 'found_fields': found_fields}
    
    def standardize_columns(self, df):
        """标准化列名并合并同名数值列"""
        column_mapping = {}
        columns = list(df.columns)
        print(f"[DEBUG] standardize_columns输入: {columns}")
        # 记录每个标准字段对应的原始列
        reverse_map = {k: [] for k in self.field_mapping.keys()}
        for col in columns:
            col_lower = str(col).lower()
            for standard_field, keywords in self.field_mapping.items():
                if any(keyword in col_lower for keyword in keywords):
                    column_mapping[col] = standard_field
                    reverse_map[standard_field].append(col)
                    break
        print(f"[DEBUG] column_mapping: {column_mapping}")
        # 合并数值型字段
        numeric_fields = ['engagement', 'reach', 'conversion', 'followers']
        for field in numeric_fields:
            cols = reverse_map[field]
            if len(cols) > 1:
                # 多列合并求和
                df[field] = df[cols].apply(pd.to_numeric, errors='coerce').sum(axis=1)
                df = df.drop(columns=[c for c in cols if c != field])
            elif len(cols) == 1:
                df = df.rename(columns={cols[0]: field})
        # 其他字段只保留第一个
        for field in self.field_mapping.keys():
            if field not in numeric_fields:
                cols = reverse_map[field]
                if len(cols) > 1:
                    df = df.rename(columns={cols[0]: field})
                    df = df.drop(columns=[c for c in cols[1:]])
                elif len(cols) == 1:
                    df = df.rename(columns={cols[0]: field})
        print(f"[DEBUG] 合并后df.columns: {list(df.columns)}")
        # 添加缺失的标准列
        for field in self.field_mapping.keys():
            if field not in df.columns:
                print(f"[DEBUG] 添加缺失字段: {field}")
                if field == 'date':
                    df[field] = pd.Timestamp.now()
                elif field == 'platform':
                    df[field] = '未知平台'
                elif field == 'content_type':
                    df[field] = '文本'
                elif field == 'engagement':
                    df[field] = 0
                elif field == 'reach':
                    df[field] = 0
                elif field == 'conversion':
                    df[field] = 0
                elif field == 'followers':
                    df[field] = 0
                elif field == 'content':
                    df[field] = ''
                elif field == 'user_type':
                    df[field] = '个人用户'
                elif field == 'sentiment':
                    df[field] = '中性'
        print(f"[DEBUG] 返回前df.columns: {list(df.columns)}")
        return df
    
    def clean_data(self, df):
        """数据清洗"""
        # 处理日期字段
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
            
        # 处理数值字段
        numeric_fields = ['engagement', 'reach', 'conversion', 'followers']
        for field in numeric_fields:
            if field in df.columns:
                df[field] = pd.to_numeric(df[field], errors='coerce').fillna(0)
                
        # 处理文本字段
        text_fields = ['content', 'platform', 'content_type', 'user_type', 'sentiment']
        for field in text_fields:
            if field in df.columns:
                df[field] = df[field].astype(str).fillna('')
                
        return df
    
    def save_imported_data(self, df, user_id, data_name):
        """保存导入的数据"""
        try:
            # 创建数据目录
            data_dir = f"data/user_{user_id}"
            os.makedirs(data_dir, exist_ok=True)
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{data_name}_{timestamp}.csv"
            file_path = os.path.join(data_dir, filename)
            
            # 保存数据
            df.to_csv(file_path, index=False, encoding='utf-8')
            
            return {
                'success': True,
                'file_path': file_path,
                'message': f"数据已保存到: {filename}"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"保存失败: {str(e)}"
            }

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
            '平均粉丝数': df['followers'].mean() if 'followers' in df.columns else 0,
            '平均互动量': df['engagement'].mean() if 'engagement' in df.columns else 0,
            '平均曝光量': df['reach'].mean() if 'reach' in df.columns else 0,
            '平均点击率': df['conversion'].mean() if 'conversion' in df.columns else 0,
            '平均转化率': df['conversion'].mean() if 'conversion' in df.columns else 0
        }
        
        # 增长分析
        if 'followers' in df.columns:
            latest_followers = df['followers'].iloc[-1]
            initial_followers = df['followers'].iloc[0]
            followers_growth = latest_followers - initial_followers
            followers_growth_rate = (followers_growth / initial_followers) * 100 if initial_followers > 0 else 0
        else:
            followers_growth = 0
            followers_growth_rate = 0
        
        if 'engagement' in df.columns:
            latest_engagement = df['engagement'].iloc[-1]
            initial_engagement = df['engagement'].iloc[0]
            engagement_growth = latest_engagement - initial_engagement
            engagement_growth_rate = (engagement_growth / initial_engagement) * 100 if initial_engagement > 0 else 0
        else:
            engagement_growth = 0
            engagement_growth_rate = 0
        
        analysis['增长分析'] = {
            '粉丝增长数': followers_growth,
            '粉丝增长率(%)': round(followers_growth_rate, 2),
            '互动量增长数': engagement_growth,
            '互动量增长率(%)': round(engagement_growth_rate, 2)
        }
        
        # 相关性分析
        if platform == "微博":
            analysis['相关性分析'] = {}
            if '转发量' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['转发量与互动量相关性'] = round(df['转发量'].corr(df['engagement']), 2)
            if '评论量' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['评论量与互动量相关性'] = round(df['评论量'].corr(df['engagement']), 2)
            if '点赞量' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['点赞量与互动量相关性'] = round(df['点赞量'].corr(df['engagement']), 2)
        elif platform == "微信":
            analysis['相关性分析'] = {}
            if '阅读量' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['阅读量与互动量相关性'] = round(df['阅读量'].corr(df['engagement']), 2)
            if '在看量' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['在看量与互动量相关性'] = round(df['在看量'].corr(df['engagement']), 2)
            if '分享量' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['分享量与互动量相关性'] = round(df['分享量'].corr(df['engagement']), 2)
        elif platform == "抖音":
            analysis['相关性分析'] = {}
            if '播放量' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['播放量与互动量相关性'] = round(df['播放量'].corr(df['engagement']), 2)
            if '完播率' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['完播率与互动量相关性'] = round(df['完播率'].corr(df['engagement']), 2)
            if '平均播放时长' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['平均播放时长与互动量相关性'] = round(df['平均播放时长'].corr(df['engagement']), 2)
        elif platform == "小红书":
            analysis['相关性分析'] = {}
            if '收藏量' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['收藏量与互动量相关性'] = round(df['收藏量'].corr(df['engagement']), 2)
            if '关注量' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['关注量与互动量相关性'] = round(df['关注量'].corr(df['engagement']), 2)
            if '搜索量' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['搜索量与互动量相关性'] = round(df['搜索量'].corr(df['engagement']), 2)
        elif platform == "B站":
            analysis['相关性分析'] = {}
            if '播放量' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['播放量与互动量相关性'] = round(df['播放量'].corr(df['engagement']), 2)
            if '弹幕量' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['弹幕量与互动量相关性'] = round(df['弹幕量'].corr(df['engagement']), 2)
            if '投币量' in df.columns and 'engagement' in df.columns:
                analysis['相关性分析']['投币量与互动量相关性'] = round(df['投币量'].corr(df['engagement']), 2)
        else:
            analysis['相关性分析'] = {}
        
        # 趋势分析
        if 'followers' in df.columns and 'date' in df.columns:
            # 确保date列是datetime类型并设置为索引
            df_temp = df.copy()
            df_temp['date'] = pd.to_datetime(df_temp['date'], errors='coerce')
            df_temp = df_temp.dropna(subset=['date'])
            if not df_temp.empty:
                df_temp = df_temp.set_index('date')
                weekly_followers = df_temp['followers'].resample('W-MON').mean().reset_index()
                followers_trend = weekly_followers.to_dict('records')
            else:
                followers_trend = []
        else:
            followers_trend = []
            
        if 'engagement' in df.columns and 'date' in df.columns:
            # 确保date列是datetime类型并设置为索引
            df_temp = df.copy()
            df_temp['date'] = pd.to_datetime(df_temp['date'], errors='coerce')
            df_temp = df_temp.dropna(subset=['date'])
            if not df_temp.empty:
                df_temp = df_temp.set_index('date')
                weekly_engagement = df_temp['engagement'].resample('W-MON').mean().reset_index()
                engagement_trend = weekly_engagement.to_dict('records')
            else:
                engagement_trend = []
        else:
            engagement_trend = []
        
        analysis['趋势分析'] = {
            '粉丝数每周趋势': followers_trend,
            '互动量每周趋势': engagement_trend
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