# -*- coding: utf-8 -*-
"""
系统配置文件
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 数据库配置
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'social_media_analysis',
    'user': 'root',
    'password': '',
    'charset': 'utf8mb4'
}

# AI服务配置
AI_CONFIG = {
    'api_key': 'sk-dfc4e38245414faf8290bb291db1a35e',
    'base_url': 'https://api.deepseek.com/v1/chat/completions',
    'model': 'deepseek-chat',
    'max_tokens': 2000,
    'temperature': 0.7,
    'timeout': 30
}

# 应用配置
APP_CONFIG = {
    'name': '人工智能社交媒体营销分析系统',
    'version': '1.0.0',
    'author': 'AI Development Team',
    'window_title': 'AI社交媒体营销分析系统',
    'window_size': (1200, 800),
    'min_window_size': (800, 600)
}

# 界面配置
UI_CONFIG = {
    'theme': 'fusion',
    'font_family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    'font_size': 13,
    'primary_color': '#0071e3',
    'secondary_color': '#0066cc',
    'background_color': '#f5f5f7',
    'text_color': '#1d1d1f',
    'border_color': '#d2d2d7'
}

# 数据分析配置
ANALYSIS_CONFIG = {
    'max_data_rows': 100000,
    'max_text_length': 10000,
    'sentiment_sample_size': 1000,
    'wordcloud_width': 800,
    'wordcloud_height': 400,
    'chart_dpi': 100
}

# 文件路径配置
PATHS = {
    'data_dir': PROJECT_ROOT / 'data',
    'reports_dir': PROJECT_ROOT / 'reports',
    'logs_dir': PROJECT_ROOT / 'logs',
    'temp_dir': PROJECT_ROOT / 'temp',
    'sample_data': PROJECT_ROOT / 'assets' / 'sample_data.csv',
    'database': PROJECT_ROOT / 'assets' / 'social_media_analysis.db'
}

# 创建必要的目录
for path in PATHS.values():
    if isinstance(path, Path) and not path.exists():
        path.mkdir(parents=True, exist_ok=True)

# 日志配置
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': PATHS['logs_dir'] / 'app.log',
            'mode': 'a',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

# 支持的文件格式
SUPPORTED_FORMATS = {
    'csv': {
        'extensions': ['.csv'],
        'encodings': ['utf-8', 'gbk', 'gb2312', 'latin1'],
        'separators': [',', ';', '\t', '|']
    },
    'excel': {
        'extensions': ['.xlsx', '.xls'],
        'sheets': True
    },
    'json': {
        'extensions': ['.json'],
        'encodings': ['utf-8']
    }
}

# 分析类型配置
ANALYSIS_TYPES = {
    'basic': {
        'name': '基础统计分析',
        'description': '数据概览、缺失值统计、数据类型分析',
        'icon': '📊'
    },
    'time_series': {
        'name': '时间序列分析',
        'description': '数据趋势、移动平均、周期性分析',
        'icon': '📈'
    },
    'engagement': {
        'name': '互动分析',
        'description': '点赞、评论、转发数据分析',
        'icon': '👍'
    },
    'content': {
        'name': '内容分析',
        'description': '文本长度、关键词提取、内容分布',
        'icon': '📝'
    },
    'sentiment': {
        'name': '情感分析',
        'description': '文本情感倾向分析',
        'icon': '😊'
    },
    'ai_analysis': {
        'name': 'AI智能分析',
        'description': '基于AI的综合分析和建议',
        'icon': '🤖'
    }
}

# 策略类型配置
STRATEGY_TYPES = {
    'marketing_strategy': {
        'name': '营销策略生成',
        'description': '根据目标受众、平台、目标生成完整营销方案',
        'icon': '🎯'
    },
    'content_ideas': {
        'name': '内容创意生成',
        'description': '基于主题和目标受众生成内容创意',
        'icon': '💡'
    },
    'competitor_analysis': {
        'name': '竞争对手分析',
        'description': '分析竞争对手优劣势，提供差异化建议',
        'icon': '🔍'
    }
}

# 平台配置
PLATFORMS = [
    '微信', '微博', '抖音', '小红书', 'B站', '知乎', 
    'Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'YouTube'
]

# 内容类型配置
CONTENT_TYPES = [
    '图文', '视频', '短视频', '直播', '音频', '链接', '投票', '问答'
]

# 用户类型配置
USER_TYPES = [
    '个人用户', '企业用户', 'KOL', '媒体', '政府机构', '其他'
]

# 情感倾向配置
SENTIMENT_TYPES = [
    '正面', '负面', '中性'
] 