from views.login_view import LoginView
from views.register_view import RegisterView
from views.main_view import MainView
from views.data_import_view import DataImportView
from views.data_analysis_view import DataAnalysisView
from views.marketing_strategy_view import MarketingStrategyView
from views.trend_prediction_view import TrendPredictionView
from views.content_optimization_view import ContentOptimizationView
from views.report_management_view import ReportManagementView
from views.system_settings_view import SystemSettingsView
from models.database import DatabaseManager
from models.social_media_data import SocialMediaData
from models.deepseek_api import DeepSeekAPI
from models.report_generator import ReportGenerator
import hashlib
import json
import time
import os
from datetime import datetime
import sys
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QFileDialog, 
                             QInputDialog, QProgressDialog, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QPushButton, QTextEdit, QTabWidget,
                             QScrollArea, QFrame, QSplitter, QGroupBox, QGridLayout,
                             QTableWidgetItem)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QIcon
from models.data_analyzer import DataAnalyzer
import matplotlib.pyplot as plt
import numpy as np

def convert_pandas_types(obj):
    """将pandas数据类型转换为JSON可序列化的类型"""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (pd.Timestamp, pd.DatetimeTZDtype)):
        return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif pd.isna(obj) if not isinstance(obj, (list, dict, np.ndarray)) else False:
        return None
    elif isinstance(obj, dict):
        return {key: convert_pandas_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_pandas_types(item) for item in obj]
    else:
        return obj

class MainController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.current_user = None
        self.db = DatabaseManager()
        self.social_media_data = SocialMediaData()
        self.api = DeepSeekAPI("sk-dfc4e38245414faf8290bb291db1a35e")
        self.data_analyzer = DataAnalyzer()
        
        # 设置应用程序样式
        self.app.setStyle('Fusion')
        
        # 显示登录界面
        self.show_login_view()
        
    def show_login_view(self):
        """显示登录界面"""
        self.login_view = LoginView(self)
        self.login_view.show()
        # 如果有打开的主窗口或注册窗口，则关闭它们
        if hasattr(self, 'main_view'):
            self.main_view.close()
        if hasattr(self, 'register_view'):
            self.register_view.close()
            
    def show_register_view(self):
        """显示注册界面"""
        self.register_view = RegisterView(self)
        self.register_view.show()
        
        # 如果有打开的登录窗口或主窗口，则关闭它们
        if hasattr(self, 'login_view'):
            self.login_view.close()
        if hasattr(self, 'main_view'):
            self.main_view.close()
            
    def show_main_view(self):
        """显示主界面"""
        self.main_view = MainView(self)
        
        # 连接信号
        self.main_view.logout_signal.connect(self.logout)
        self.main_view.import_data_signal.connect(self.show_data_import_view)
        self.main_view.analyze_data_signal.connect(self.run_analysis)
        self.main_view.generate_plan_signal.connect(self.generate_marketing_plan)
        self.main_view.predict_trends_signal.connect(self.predict_trends)
        self.main_view.optimize_content_signal.connect(self.optimize_content)
        self.main_view.export_report_signal.connect(self.export_report)
        self.main_view.test_api_signal.connect(self.test_api_connection)
        self.main_view.save_settings_signal.connect(self.save_settings)
        self.main_view.change_password_signal.connect(self.change_password)
        self.main_view.export_data_signal.connect(self.export_data)
        self.main_view.refresh_data_signal.connect(self.refresh_data)
        self.main_view.exit_signal.connect(self.exit_application)
        self.main_view.help_signal.connect(self.show_help)
        self.main_view.about_signal.connect(self.show_about)
        self.main_view.create_plan_signal.connect(self.create_new_plan)
        self.main_view.delete_plan_signal.connect(self.delete_marketing_plan)
        self.main_view.export_plan_signal.connect(self.export_marketing_plan)
        self.main_view.share_plan_signal.connect(self.share_marketing_plan)
        
        # 连接新界面的信号
        self.main_view.show_marketing_strategy_signal.connect(self.show_marketing_strategy_view)
        self.main_view.show_trend_prediction_signal.connect(self.show_trend_prediction_view)
        self.main_view.show_content_optimization_signal.connect(self.show_content_optimization_view)
        self.main_view.show_report_management_signal.connect(self.show_report_management_view)
        self.main_view.show_system_settings_signal.connect(self.show_system_settings_view)
            
        # 加载用户数据
        self.load_user_data()
            
        self.main_view.show()
        
    def show_marketing_strategy_view(self):
        """显示营销策略界面"""
        self.marketing_strategy_view = MarketingStrategyView(self.main_view)
        
        # 连接信号
        self.marketing_strategy_view.strategy_created_signal.connect(self.create_strategy)
        self.marketing_strategy_view.strategy_updated_signal.connect(self.update_strategy)
        self.marketing_strategy_view.strategy_deleted_signal.connect(self.delete_strategy)
        
        self.marketing_strategy_view.show()
        
    def show_trend_prediction_view(self):
        """显示趋势预测界面"""
        self.trend_prediction_view = TrendPredictionView(self.main_view)
        
        # 连接信号
        self.trend_prediction_view.prediction_started_signal.connect(self.start_prediction)
        self.trend_prediction_view.prediction_completed_signal.connect(self.complete_prediction)
        
        self.trend_prediction_view.show()
        
    def show_content_optimization_view(self):
        """显示内容优化界面"""
        self.content_optimization_view = ContentOptimizationView(self.main_view)
        
        # 连接信号
        self.content_optimization_view.optimization_started_signal.connect(self.start_optimization)
        self.content_optimization_view.optimization_completed_signal.connect(self.complete_optimization)
        
        self.content_optimization_view.show()
        
    def show_report_management_view(self):
        """显示报告管理界面"""
        self.report_management_view = ReportManagementView(self.main_view)
        
        # 连接信号
        self.report_management_view.report_generated_signal.connect(self.generate_report)
        self.report_management_view.report_exported_signal.connect(self.export_report_file)
        
        self.report_management_view.show()
        
    def show_system_settings_view(self):
        """显示系统设置界面"""
        self.system_settings_view = SystemSettingsView(self.main_view)
        
        # 连接信号
        self.system_settings_view.settings_saved_signal.connect(self.save_system_settings)
        self.system_settings_view.settings_reset_signal.connect(self.reset_system_settings)
        
        self.system_settings_view.show()
            
    def login(self, username, password):
        """处理登录逻辑"""
        # 对密码进行哈希处理
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        # 从数据库获取用户
        user = self.db.get_user(username, hashed_password)
        if user:
            self.current_user = user
            return True, "登录成功"
        else:
            return False, "用户名或密码错误"
            
    def register(self, username, email, password):
        """处理注册逻辑"""
        # 对密码进行哈希处理
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # 检查用户名是否已存在
        existing_user = self.db.get_user(username)
        if existing_user:
            return False, "用户名已存在"
            
        # 添加新用户
        user_id = self.db.add_user(username, hashed_password, email)
        
        if user_id:
            return True, "注册成功"
        else:
            return False, "注册失败，请重试"
            
    def logout(self):
        """用户登出"""
        self.current_user = None
        self.show_login_view()
        self.main_view.close()
            
    def load_user_data(self):
        """加载用户数据"""
        # 加载分析任务
        self.load_analysis_tasks()
        
        # 加载营销方案
        self.load_marketing_plans()
        
        # 更新仪表盘统计数据
        self.update_dashboard_stats()
        
    def load_analysis_tasks(self):
        """加载分析任务"""
        if not hasattr(self, 'main_view'):
            return
            
        tasks = self.db.get_analysis_tasks(self.current_user[0])
        
        # TODO: 在UI中显示分析任务
        
    def load_marketing_plans(self):
        """加载营销方案"""
        if not hasattr(self, 'main_view'):
            return
            
        plans = self.db.get_marketing_plans(self.current_user[0])
        
        # 清空现有列表
        self.main_view.plans_list.clear()
        
        # 添加营销方案到列表
        for plan in plans:
            plan_id, plan_name, created_at, task_name = plan
            item_text = f"{plan_name}"
            if task_name:
                item_text += f" (来自分析: {task_name})"
                
            item = self.main_view.plans_list.addItem(item_text)
            current_item = self.main_view.plans_list.item(self.main_view.plans_list.count() - 1)
            current_item.setData(self.main_view.plans_list.ItemDataRole.UserRole, plan_id)
            
    def update_dashboard_stats(self):
        """更新仪表盘统计数据"""
        if not hasattr(self, 'main_view'):
            return
            
        try:
        # 获取分析任务数量
            analysis_tasks = self.db.get_analysis_tasks(self.current_user[0])
            total_analysis = len(analysis_tasks) if analysis_tasks else 0
            
            # 获取已完成的分析任务数量
            completed_analysis = len([task for task in analysis_tasks if task[4] == 'completed']) if analysis_tasks else 0
        
        # 获取营销方案数量
            marketing_plans = self.db.get_marketing_plans(self.current_user[0])
            total_plans = len(marketing_plans) if marketing_plans else 0
            
            # 获取活跃平台数量（基于数据导入记录）
            data_imports = self.db.get_data_imports(self.current_user[0])
            active_platforms = len(set([imp[2] for imp in data_imports if imp])) if data_imports else 0
        
        # 更新统计卡片
            self.update_stat_card("总分析任务", str(total_analysis))
            self.update_stat_card("已完成分析", str(completed_analysis))
            self.update_stat_card("营销方案", str(total_plans))
            self.update_stat_card("活跃平台", str(active_platforms))
            
            # 更新最近活动表格
            self.update_recent_activity_table()
            
            # 更新图表
            self.update_dashboard_charts()
            
        except Exception as e:
            print(f"更新仪表盘统计失败: {e}")
    
    def update_stat_card(self, title, value):
        """更新统计卡片"""
        if not hasattr(self, 'main_view'):
            return
            
        # 查找对应的统计卡片并更新
        for i in range(self.main_view.stats_layout.count()):
            widget = self.main_view.stats_layout.itemAt(i).widget()
            if hasattr(widget, 'title_label') and widget.title_label.text() == title:
                if hasattr(widget, 'value_label'):
                    widget.value_label.setText(value)
                break
    
    def update_recent_activity_table(self):
        """更新最近活动表格"""
        if not hasattr(self, 'main_view'):
            return
            
        try:
            # 获取最近的活动记录
            recent_activities = []
            
            # 获取最近的分析任务
            analysis_tasks = self.db.get_analysis_tasks(self.current_user[0])
            if analysis_tasks:
                for task in analysis_tasks[:3]:  # 最多显示3个
                    recent_activities.append({
                        'time': task[5],  # created_at
                        'type': '数据分析',
                        'detail': f"分析任务: {task[1]}",  # task_name
                        'status': task[4]  # status
                    })
            
            # 获取最近的营销方案
            marketing_plans = self.db.get_marketing_plans(self.current_user[0])
            if marketing_plans:
                for plan in marketing_plans[:2]:  # 最多显示2个
                    recent_activities.append({
                        'time': plan[3],  # created_at
                        'type': '营销方案',
                        'detail': f"方案: {plan[0]}",  # plan_name
                        'status': '已完成'
                    })
            
            # 按时间排序
            recent_activities.sort(key=lambda x: x['time'], reverse=True)
            
            # 更新表格
            table = self.main_view.recent_activity_table
            table.setRowCount(min(len(recent_activities), 5))
            
            for i, activity in enumerate(recent_activities[:5]):
                table.setItem(i, 0, QTableWidgetItem(activity['time']))
                table.setItem(i, 1, QTableWidgetItem(activity['type']))
                table.setItem(i, 2, QTableWidgetItem(activity['detail']))
                table.setItem(i, 3, QTableWidgetItem(activity['status']))
                
        except Exception as e:
            print(f"更新最近活动表格失败: {e}")
    
    def update_dashboard_charts(self):
        """更新仪表盘图表"""
        if not hasattr(self, 'main_view'):
            return
            
        try:
            # 获取数据导入记录
            data_imports = self.db.get_data_imports(self.current_user[0])
            
            if not data_imports:
                # 如果没有数据，显示空图表
                self.create_empty_dashboard_charts()
                return
            
            # 创建趋势图表
            self.create_trends_chart(data_imports)
            
            # 创建平台分布图表
            self.create_platform_chart(data_imports)
            
        except Exception as e:
            print(f"更新仪表盘图表失败: {e}")
    
    def create_empty_dashboard_charts(self):
        """创建空的仪表盘图表"""
        if not hasattr(self, 'main_view'):
            return
            
        # 创建空的趋势图表
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, '暂无数据', ha='center', va='center', transform=ax.transAxes, fontsize=14)
        ax.set_title('粉丝增长趋势')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # 清除旧图表并添加新图表
        if hasattr(self.main_view, 'trends_chart'):
            self.main_view.trends_chart.figure.clear()
            self.main_view.trends_chart.figure = fig
            self.main_view.trends_chart.draw()
        
        # 创建空的平台分布图表
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.text(0.5, 0.5, '暂无数据', ha='center', va='center', transform=ax2.transAxes, fontsize=14)
        ax2.set_title('平台分布')
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.axis('off')
        
        # 清除旧图表并添加新图表
        if hasattr(self.main_view, 'platform_chart'):
            self.main_view.platform_chart.figure.clear()
            self.main_view.platform_chart.figure = fig2
            self.main_view.platform_chart.draw()
    
    def create_trends_chart(self, data_imports):
        """创建趋势图表"""
        if not hasattr(self, 'main_view'):
            return
            
        try:
            # 按时间分组统计数据量
            import_dates = [imp[4] for imp in data_imports if imp[4]]  # created_at
            date_counts = {}
            
            for date in import_dates:
                date_str = date.split(' ')[0]  # 只取日期部分
                date_counts[date_str] = date_counts.get(date_str, 0) + 1
            
            if not date_counts:
                self.create_empty_dashboard_charts()
                return
            
            # 创建趋势图表
            fig, ax = plt.subplots(figsize=(6, 4))
            
            dates = list(date_counts.keys())
            counts = list(date_counts.values())
            
            ax.plot(dates, counts, marker='o', linewidth=2, markersize=6)
            ax.set_title('数据导入趋势')
            ax.set_xlabel('日期')
            ax.set_ylabel('导入次数')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3)
            
            # 清除旧图表并添加新图表
            if hasattr(self.main_view, 'trends_chart'):
                self.main_view.trends_chart.figure.clear()
                self.main_view.trends_chart.figure = fig
                self.main_view.trends_chart.draw()
                
        except Exception as e:
            print(f"创建趋势图表失败: {e}")
    
    def create_platform_chart(self, data_imports):
        """创建平台分布图表"""
        if not hasattr(self, 'main_view'):
            return
            
        try:
            # 统计各平台数据量
            platform_counts = {}
            
            for imp in data_imports:
                platform = imp[2] if imp[2] else '未知平台'  # platform
                platform_counts[platform] = platform_counts.get(platform, 0) + 1
            
            if not platform_counts:
                self.create_empty_dashboard_charts()
                return
            
            # 创建平台分布图表
            fig, ax = plt.subplots(figsize=(6, 4))
            
            platforms = list(platform_counts.keys())
            counts = list(platform_counts.values())
            
            # 使用饼图显示平台分布
            colors = plt.cm.Set3(np.linspace(0, 1, len(platforms)))
            wedges, texts, autotexts = ax.pie(counts, labels=platforms, autopct='%1.1f%%', 
                                             colors=colors, startangle=90)
            ax.set_title('平台数据分布')
            
            # 清除旧图表并添加新图表
            if hasattr(self.main_view, 'platform_chart'):
                self.main_view.platform_chart.figure.clear()
                self.main_view.platform_chart.figure = fig
                self.main_view.platform_chart.draw()
                
        except Exception as e:
            print(f"创建平台分布图表失败: {e}")
        
    def run_analysis(self):
        """运行数据分析"""
        if not hasattr(self, 'main_view'):
            return
            
        # 获取UI中的分析参数
        analysis_type = self.main_view.analysis_type_combo.currentText()
        platform = self.main_view.platform_combo.currentText()
        start_date = self.main_view.start_date.date().toString("yyyy-MM-dd")
        end_date = self.main_view.end_date.date().toString("yyyy-MM-dd")
        data_source = self.main_view.data_source_combo.currentText()
        file_path = self.main_view.file_path_input.text()
        
        # 显示进度条
        self.main_view.analysis_progress.setValue(0)
        
        # 创建分析任务
        task_name = f"{analysis_type} - {platform} - {start_date}至{end_date}"
        task_id = self.db.add_analysis_task(
            self.current_user[0], 
            task_name, 
            platform, 
            analysis_type,
            file_path if data_source == "导入数据" else "示例数据"
        )
        
        # 模拟分析进度
        self.main_view.analysis_progress.setValue(20)
        
        # 获取数据
        if data_source == "示例数据":
            # 生成示例数据
            df = self.social_media_data.generate_sample_data(platform)
        else:
            # 从文件导入数据
            if not file_path:
                QMessageBox.warning(self.main_view, "导入失败", "请选择数据文件")
                return
                
            # 导入CSV数据
            import_result = self.social_media_data.import_csv_data(
                file_path=file_path,
                encoding='utf-8',
                separator=',',
                has_header=True
            )
            
            if not import_result['valid']:
                QMessageBox.critical(self.main_view, "导入失败", import_result['error'])
                return
                
            df = import_result['data']
            
            # 保存导入的数据
            save_result = self.social_media_data.save_imported_data(
                df, 
                self.current_user[0], 
                f"{platform}_imported_data"
            )
            
            # 添加数据导入记录到数据库
            self.db.add_data_import(
                user_id=self.current_user[0],
                import_name=f"{platform}_imported_data",
                file_path=file_path,
                data_count=len(df),
                platform=platform
            )
            
            if save_result['success']:
                QMessageBox.information(self.main_view, "导入成功", 
                    f"{import_result['message']}\n{save_result['message']}")
            else:
                QMessageBox.warning(self.main_view, "保存警告", 
                    f"{import_result['message']}\n但保存失败: {save_result['error']}")
            
        self.main_view.analysis_progress.setValue(40)
        
        # 分析数据
        analysis = self.social_media_data.analyze_data(df, platform)
        
        self.main_view.analysis_progress.setValue(60)
        
        # 准备AI分析数据
        ai_data = self.social_media_data.prepare_for_ai(analysis, platform)
        
        self.main_view.analysis_progress.setValue(80)
        
        # 保存分析结果
        self.db.add_analysis_result(task_id, "overview", json.dumps(convert_pandas_types(analysis['基本统计'])))
        self.db.add_analysis_result(task_id, "growth", json.dumps(convert_pandas_types(analysis['增长分析'])))
        self.db.add_analysis_result(task_id, "correlation", json.dumps(convert_pandas_types(analysis['相关性分析'])))
        self.db.add_analysis_result(task_id, "trends", json.dumps(convert_pandas_types(analysis['趋势分析'])))
        
        # 更新UI显示分析结果
        self.display_analysis_results(analysis, df, platform)
        
        self.main_view.analysis_progress.setValue(100)
        
        # 刷新用户数据
        self.load_user_data()
        
    def display_analysis_results(self, analysis, df, platform):
        """显示分析结果"""
        if not hasattr(self, 'main_view'):
            return
            
        # 显示分析概述
        overview_text = "社交媒体数据分析概述\n\n"
        overview_text += "基本统计:\n"
        for key, value in analysis['基本统计'].items():
            overview_text += f"- {key}: {value}\n"
            
        overview_text += "\n增长分析:\n"
        for key, value in analysis['增长分析'].items():
            overview_text += f"- {key}: {value}\n"
            
        overview_text += "\n相关性分析:\n"
        for key, value in analysis['相关性分析'].items():
            overview_text += f"- {key}: {value}\n"
            
        self.main_view.overview_text.setText(overview_text)
        
        # 显示详细数据
        self.main_view.details_text.setText(json.dumps(convert_pandas_types(analysis), indent=4, ensure_ascii=False))
        
        # 创建并显示图表
        self.create_and_display_charts(df, platform)
        
    def create_and_display_charts(self, df, platform):
        """创建并显示图表"""
        if not hasattr(self, 'main_view'):
            return
            
        # 清除现有的图表
        if hasattr(self.main_view, 'chart_layout'):
            # 清除现有图表
            while self.main_view.chart_layout.count():
                child = self.main_view.chart_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        else:
            # 创建图表布局
            self.main_view.chart_layout = QVBoxLayout()
            self.main_view.chart_scroll_area = QScrollArea()
            self.main_view.chart_widget = QWidget()
            self.main_view.chart_widget.setLayout(self.main_view.chart_layout)
            self.main_view.chart_scroll_area.setWidget(self.main_view.chart_widget)
            self.main_view.chart_scroll_area.setWidgetResizable(True)
            
            # 将图表区域添加到主界面
            if hasattr(self.main_view, 'analysis_tab_layout'):
                self.main_view.analysis_tab_layout.addWidget(self.main_view.chart_scroll_area)
        
        try:
            # 创建综合仪表板
            dashboard_fig = self.data_analyzer.create_summary_dashboard(df, platform)
            dashboard_canvas = self.data_analyzer.get_chart_canvas(dashboard_fig)
            
            # 创建标题标签
            dashboard_label = QLabel("综合数据分析仪表板")
            dashboard_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            dashboard_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dashboard_label.setStyleSheet("color: #2c3e50; margin: 10px;")
            
            self.main_view.chart_layout.addWidget(dashboard_label)
            self.main_view.chart_layout.addWidget(dashboard_canvas)
            
            # 创建互动量趋势图
            trend_fig = self.data_analyzer.create_engagement_trend_chart(df, platform)
            trend_canvas = self.data_analyzer.get_chart_canvas(trend_fig)
            
            trend_label = QLabel("互动量趋势分析")
            trend_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            trend_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            trend_label.setStyleSheet("color: #34495e; margin: 10px;")
            
            self.main_view.chart_layout.addWidget(trend_label)
            self.main_view.chart_layout.addWidget(trend_canvas)
            
            # 创建平台对比图
            if df['platform'].nunique() > 1:
                comparison_fig = self.data_analyzer.create_platform_comparison_chart(df)
                comparison_canvas = self.data_analyzer.get_chart_canvas(comparison_fig)
                
                comparison_label = QLabel("平台对比分析")
                comparison_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
                comparison_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                comparison_label.setStyleSheet("color: #34495e; margin: 10px;")
                
                self.main_view.chart_layout.addWidget(comparison_label)
                self.main_view.chart_layout.addWidget(comparison_canvas)
            
            # 创建情感分析图
            sentiment_fig = self.data_analyzer.create_sentiment_analysis_chart(df)
            sentiment_canvas = self.data_analyzer.get_chart_canvas(sentiment_fig)
            
            sentiment_label = QLabel("情感分析")
            sentiment_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            sentiment_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            sentiment_label.setStyleSheet("color: #34495e; margin: 10px;")
            
            self.main_view.chart_layout.addWidget(sentiment_label)
            self.main_view.chart_layout.addWidget(sentiment_canvas)
            
            # 创建内容类型分析图
            content_fig = self.data_analyzer.create_content_type_analysis_chart(df)
            content_canvas = self.data_analyzer.get_chart_canvas(content_fig)
            
            content_label = QLabel("内容类型分析")
            content_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            content_label.setStyleSheet("color: #34495e; margin: 10px;")
            
            self.main_view.chart_layout.addWidget(content_label)
            self.main_view.chart_layout.addWidget(content_canvas)
            
            # 创建相关性热力图
            correlation_fig = self.data_analyzer.create_correlation_heatmap(df)
            if correlation_fig:
                correlation_canvas = self.data_analyzer.get_chart_canvas(correlation_fig)
                
                correlation_label = QLabel("数值字段相关性分析")
                correlation_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
                correlation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                correlation_label.setStyleSheet("color: #34495e; margin: 10px;")
                
                self.main_view.chart_layout.addWidget(correlation_label)
                self.main_view.chart_layout.addWidget(correlation_canvas)
            
            # 添加保存图表按钮
            save_charts_button = QPushButton("保存所有图表")
            save_charts_button.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #229954;
                }
            """)
            save_charts_button.clicked.connect(lambda: self.save_all_charts(df, platform))
            
            self.main_view.chart_layout.addWidget(save_charts_button)
            
            # 添加弹性空间
            spacer = QWidget()
            spacer.setSizePolicy(QWidget.SizePolicy.Expanding, QWidget.SizePolicy.Expanding)
            self.main_view.chart_layout.addWidget(spacer)
            
        except Exception as e:
            error_label = QLabel(f"图表生成失败: {str(e)}")
            error_label.setStyleSheet("color: red; padding: 10px;")
            self.main_view.chart_layout.addWidget(error_label)
            
    def save_all_charts(self, df, platform):
        """保存所有图表"""
        try:
            # 选择保存目录
            save_dir = QFileDialog.getExistingDirectory(
                self.main_view, 
                "选择保存目录",
                "reports"
            )
            
            if not save_dir:
                return
                
            # 生成时间戳
            timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
            
            # 保存各种图表
            charts_to_save = [
                ("综合仪表板", self.data_analyzer.create_summary_dashboard(df, platform)),
                ("互动量趋势", self.data_analyzer.create_engagement_trend_chart(df, platform)),
                ("平台对比", self.data_analyzer.create_platform_comparison_chart(df)),
                ("情感分析", self.data_analyzer.create_sentiment_analysis_chart(df)),
                ("内容类型分析", self.data_analyzer.create_content_type_analysis_chart(df))
            ]
            
            # 添加相关性热力图
            correlation_fig = self.data_analyzer.create_correlation_heatmap(df)
            if correlation_fig:
                charts_to_save.append(("相关性热力图", correlation_fig))
            
            saved_count = 0
            for chart_name, fig in charts_to_save:
                file_path = f"{save_dir}/{platform}_{chart_name}_{timestamp}.png"
                if self.data_analyzer.save_chart(fig, file_path):
                    saved_count += 1
                plt.close(fig)  # 关闭图表释放内存
            
            QMessageBox.information(
                self.main_view, 
                "保存成功", 
                f"成功保存 {saved_count} 个图表到 {save_dir}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self.main_view, 
                "保存失败", 
                f"保存图表时出错: {str(e)}"
            )
        
    def generate_marketing_plan(self):
        """生成营销方案"""
        if not hasattr(self, 'main_view'):
            return
            
        # 检查API配置
        if not self.api.api_key:
            QMessageBox.warning(self.main_view, "配置错误", 
                "请先在设置中配置DeepSeek API密钥")
            return
            
        # 获取最新的分析结果
        tasks = self.db.get_analysis_tasks(self.current_user[0])
        if not tasks:
            QMessageBox.warning(self.main_view, "生成失败", 
                "没有可用的分析结果，请先进行数据分析")
            return
            
        latest_task = tasks[0]
        task_id = latest_task[0]
        platform = latest_task[2]
        data_name = latest_task[3]
        
        # 获取分析结果
        results = self.db.get_analysis_results(task_id)
        if not results:
            QMessageBox.warning(self.main_view, "生成失败", 
                "分析结果为空，请重新进行数据分析")
            return
            
        # 构建分析数据
        analysis_data = {}
        for result in results:
            result_id, result_type, result_data, created_at = result
            analysis_data[result_type] = json.loads(result_data)
            
        # 准备AI分析数据
        ai_data = f"平台: {platform}\n"
        ai_data += f"数据名称: {data_name}\n"
        ai_data += f"分析时间: {latest_task[4]}\n\n"
        
        # 添加基本统计
        if 'overview' in analysis_data:
            ai_data += "基本统计:\n"
            for key, value in analysis_data['overview'].items():
                ai_data += f"- {key}: {value}\n"
            ai_data += "\n"
        # 添加增长分析
        if 'growth' in analysis_data:
            ai_data += "增长分析:\n"
            for key, value in analysis_data['growth'].items():
                ai_data += f"- {key}: {value}\n"
            ai_data += "\n"
        # 添加相关性分析
        if 'correlation' in analysis_data:
            ai_data += "相关性分析:\n"
            for key, value in analysis_data['correlation'].items():
                ai_data += f"- {key}: {value}\n"
            ai_data += "\n"
            
        # 获取方案名称
        plan_name, ok = QInputDialog.getText(
            self.main_view, "营销方案名称", 
            f"请输入营销方案名称:\n(基于 {platform} 平台数据分析)",
            text=f"{platform}营销方案_{pd.Timestamp.now().strftime('%Y%m%d')}"
        )
        
        if not ok or not plan_name:
            return
            
        # 创建进度对话框
        progress_dialog = QMessageBox(self.main_view)
        progress_dialog.setWindowTitle("生成营销方案")
        progress_dialog.setText(f"正在基于 {platform} 平台数据分析生成营销方案...\n请稍候，这可能需要几分钟时间。")
        progress_dialog.setStandardButtons(QMessageBox.StandardButton.NoButton)
        progress_dialog.setIcon(QMessageBox.Icon.Information)
        
        # 设置对话框样式
        progress_dialog.setStyleSheet("""
            QMessageBox {
                background-color: #f8f9fa;
                border: 2px solid #0071e3;
                border-radius: 10px;
                padding: 20px;
            }
            QMessageBox QLabel {
                color: #2c3e50;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        
        progress_dialog.show()
        
        # 强制处理事件
        self.main_view.app.processEvents()
        
        # 调用API生成营销方案
        try:
            # 显示生成进度
            progress_dialog.setText("正在分析数据特征...")
            self.main_view.app.processEvents()
            
            # 调用API
            plan_content = self.api.generate_marketing_plan(ai_data)
            
            # 检查API响应
            if plan_content.startswith("错误："):
                progress_dialog.close()
                QMessageBox.critical(self.main_view, "生成失败", plan_content)
                return
            
            # 保存营销方案
            progress_dialog.setText("正在保存营销方案...")
            self.main_view.app.processEvents()
            
            plan_id = self.db.add_marketing_plan(
                self.current_user[0],
                task_id,
                plan_name,
                plan_content
            )
            
            progress_dialog.close()
            
            # 显示成功消息
            success_dialog = QMessageBox(self.main_view)
            success_dialog.setWindowTitle("生成成功")
            success_dialog.setText(f"营销方案 '{plan_name}' 已成功生成！")
            success_dialog.setInformativeText("方案已保存到您的营销方案列表中，您可以查看、编辑或导出该方案。")
            success_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
            success_dialog.setIcon(QMessageBox.Icon.Information)
            
            # 设置成功对话框样式
            success_dialog.setStyleSheet("""
                QMessageBox {
                    background-color: #d4edda;
                    border: 2px solid #28a745;
                    border-radius: 10px;
                    padding: 20px;
                }
                QMessageBox QLabel {
                    color: #155724;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 10px;
                }
            """)
            
            success_dialog.exec()
            
            # 刷新营销方案列表
            self.load_marketing_plans()
            
            # 自动切换到营销方案标签页并显示新生成的方案
            self.main_view.tabs.setCurrentIndex(2)  # 假设营销方案是第3个标签页
            if plan_id:
                # 找到并选中新生成的方案
                for i in range(self.main_view.plans_list.count()):
                    item = self.main_view.plans_list.item(i)
                    if plan_name in item.text():
                        self.main_view.plans_list.setCurrentItem(item)
                        self.load_marketing_plan(plan_id)
                        break
            
        except Exception as e:
            progress_dialog.close()
            
            # 显示详细错误信息
            error_dialog = QMessageBox(self.main_view)
            error_dialog.setWindowTitle("生成失败")
            error_dialog.setText("生成营销方案时出现错误")
            error_dialog.setInformativeText(f"错误详情: {str(e)}")
            error_dialog.setDetailedText(f"""
可能的解决方案:
1. 检查网络连接是否正常
2. 确认API密钥是否有效
3. 检查API配额是否充足
4. 尝试重新进行数据分析
5. 联系技术支持团队
            """)
            error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_dialog.setIcon(QMessageBox.Icon.Critical)
            
            # 设置错误对话框样式
            error_dialog.setStyleSheet("""
                QMessageBox {
                    background-color: #f8d7da;
                    border: 2px solid #dc3545;
                    border-radius: 10px;
                    padding: 20px;
                }
                QMessageBox QLabel {
                    color: #721c24;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 10px;
                }
            """)
            
            error_dialog.exec()
            
    def load_marketing_plan(self, plan_id):
        """加载营销方案"""
        if not hasattr(self, 'main_view'):
            return
            
        plan = self.db.get_marketing_plan(plan_id)
        if not plan:
            QMessageBox.warning(self.main_view, "加载失败", "营销方案不存在")
            return
            
        plan_name, plan_data, created_at = plan
        
        # 显示方案信息
        self.main_view.plan_title.setText(plan_name)
        self.main_view.plan_date.setText(f"创建日期: {created_at}")
        self.main_view.plan_content.setText(plan_data)
            
    def predict_trends(self):
        """预测趋势"""
        if not hasattr(self, 'main_view'):
            return
            
        # 获取UI中的参数
        prediction_type = self.main_view.prediction_type_combo.currentText()
        time_range = self.main_view.time_range_combo.currentText()
        platform = self.main_view.trend_platform_combo.currentText()
        
        # 构建提示信息
        prompt = f"""
        预测{time_range}内社交媒体{platform}平台的{prediction_type}趋势。
        请提供详细的分析和预测，包括但不限于：
        1. 主要趋势和变化
        2. 受众行为和偏好变化
        3. 内容类型和格式趋势
        4. 营销策略和方法的有效性变化
        5. 竞争格局和机会点
        
        请以结构化的方式呈现，语言简洁明了，可操作性强。
        """
        
        # 显示进度对话框
        progress_dialog = QMessageBox(self.main_view)
        progress_dialog.setWindowTitle("预测中")
        progress_dialog.setText(f"正在预测{time_range}内{platform}平台的{prediction_type}趋势，请稍候...")
        progress_dialog.setStandardButtons(QMessageBox.StandardButton.NoButton)
        progress_dialog.show()
        
        # 调用API预测趋势
        try:
            trend_prediction = self.api.predict_trends(prompt)
            
            progress_dialog.close()
            
            # 显示预测结果
            self.main_view.trend_results.setText(trend_prediction)
            
        except Exception as e:
            progress_dialog.close()
            QMessageBox.critical(self.main_view, "预测失败", f"预测趋势时出错: {str(e)}")
            
    def optimize_content(self):
        """优化内容"""
        if not hasattr(self, 'main_view'):
            return
            
        # 获取UI中的参数
        platform = self.main_view.content_platform_combo.currentText()
        content_type = self.main_view.content_type_combo.currentText()
        original_content = self.main_view.original_content.toPlainText()
        
        if not original_content:
            QMessageBox.warning(self.main_view, "优化失败", "请输入要优化的内容")
            return
            
        # 构建提示信息
        prompt = f"""
        请优化以下{content_type}内容，使其更适合在{platform}平台上传播：
        
        原始内容:
        {original_content}
        
        请提供:
        1. 优化后的内容文本
        2. 建议的发布时间
        3. 推荐使用的标签(hashtag)
        4. 建议的视觉元素
        5. 预期的互动率提升
        
        请以结构化的方式呈现，语言简洁明了，可操作性强。
        """
        
        # 显示进度对话框
        progress_dialog = QMessageBox(self.main_view)
        progress_dialog.setWindowTitle("优化中")
        progress_dialog.setText(f"正在优化{content_type}内容，请稍候...")
        progress_dialog.setStandardButtons(QMessageBox.StandardButton.NoButton)
        progress_dialog.show()
        
        # 调用API优化内容
        try:
            optimized_content = self.api.optimize_content(prompt, platform)
            
            progress_dialog.close()
            
            # 解析优化结果
            try:
                # 假设API返回的是结构化文本，尝试解析
                sections = optimized_content.split('\n\n')
                
                optimized_text = ""
                suggestions = ""
                
                for section in sections:
                    if section.startswith("1."):
                        optimized_text += section[3:].strip() + "\n\n"
                    elif section.startswith("2.") or section.startswith("3.") or section.startswith("4.") or section.startswith("5."):
                        suggestions += section + "\n\n"
                
                # 显示优化结果
                self.main_view.optimized_content.setText(optimized_text)
                self.main_view.suggestions_content.setText(suggestions)
                
            except:
                # 如果解析失败，直接显示全部内容
                self.main_view.optimized_content.setText(optimized_content)
                self.main_view.suggestions_content.setText("无法解析详细建议，请查看优化后的内容。")
                
        except Exception as e:
            progress_dialog.close()
            QMessageBox.critical(self.main_view, "优化失败", f"优化内容时出错: {str(e)}")
            
    def export_report(self):
        """导出报告"""
        if not hasattr(self, 'main_view'):
            return
            
        # 获取UI中的参数
        report_type = "分析报告"  # 根据选择的报告类型确定
        if self.main_view.marketing_report_radio.isChecked():
            report_type = "营销方案报告"
        elif self.main_view.combined_report_radio.isChecked():
            report_type = "综合报告"
            
        report_format = self.main_view.report_format_combo.currentText()
        report_title = self.main_view.report_title.text()
        include_charts = self.main_view.include_charts_check.isChecked()
        include_tables = self.main_view.include_tables_check.isChecked()
        include_recommendations = self.main_view.include_recommendations_check.isChecked()
        
        # 检查是否有数据可以生成报告
        if not hasattr(self, 'current_data') or self.current_data is None:
            QMessageBox.warning(self.main_view, "导出失败", "没有可用的分析数据，请先进行数据分析")
            return
        
        # 创建报告生成器
        report_generator = ReportGenerator()
        
        # 生成报告内容
        try:
            if report_type == "分析报告":
                report_content = report_generator.generate_analysis_report(
                    self.current_analysis_data, 
                    self.current_data, 
                    self.current_platform,
                    include_charts=include_charts,
                    include_tables=include_tables,
                    include_recommendations=include_recommendations
                )
            elif report_type == "营销方案报告":
                # 获取最新的营销方案
                latest_plan = self.db.get_latest_marketing_plan(self.current_user[0])
                if not latest_plan:
                    QMessageBox.warning(self.main_view, "导出失败", "没有可用的营销方案，请先生成营销方案")
                    return
                
                plan_name, plan_data, created_at = latest_plan
                report_content = report_generator.generate_marketing_plan_report(
                    plan_data, plan_name, self.current_analysis_data
                )
            else:  # 综合报告
                # 获取最新的营销方案
                latest_plan = self.db.get_latest_marketing_plan(self.current_user[0])
                plan_name = "综合营销方案"
                plan_data = ""
                if latest_plan:
                    plan_name, plan_data, created_at = latest_plan
                
                report_content = report_generator.generate_combined_report(
                    self.current_analysis_data,
                    self.current_data,
                    self.current_platform,
                    plan_data=plan_data,
                    plan_name=plan_name
                )
        
            # 显示预览
            self.main_view.report_preview.setText(report_content)

            # 保存报告
            file_path, _ = QFileDialog.getSaveFileName(
                self.main_view, "保存报告", f"{report_title}.{report_format.lower()}",
                f"{report_format}文件 (*.{report_format.lower()});;所有文件 (*)"
            )

            if file_path:
                # 根据格式确定保存类型
                save_format = "markdown"
                if report_format.lower() in ["html", "htm"]:
                    save_format = "html"
                elif report_format.lower() == "txt":
                    save_format = "txt"

                success = report_generator.save_report(report_content, file_path, save_format)

                if success:
                    QMessageBox.information(self.main_view, "导出成功", f"报告已成功导出到: {file_path}")
                else:
                    QMessageBox.critical(self.main_view, "导出失败", "保存报告文件时出错")
                
        except Exception as e:
            QMessageBox.critical(self.main_view, "导出失败", f"生成报告时出错: {str(e)}")
            
    def test_api_connection(self):
        """测试API连接（异步，防卡死）"""
        if not hasattr(self, 'main_view'):
            return
            
        api_key = self.main_view.api_key_input.text()
        api_base = self.main_view.api_url_input.text()
        
        # 显示进度对话框
        progress_dialog = QMessageBox(self.main_view)
        progress_dialog.setWindowTitle("测试中")
        progress_dialog.setText("正在测试API连接，请稍候...")
        progress_dialog.setStandardButtons(QMessageBox.StandardButton.NoButton)
        progress_dialog.setModal(True)
        progress_dialog.show()
        
        # 启动子线程测试API
        self.api_test_thread = ApiTestThread(api_key, api_base)
        self.api_test_thread.result_signal.connect(
            lambda ok, msg: self._on_api_test_result(progress_dialog, ok, msg)
        )
        self.api_test_thread.start()

    def _on_api_test_result(self, progress_dialog, ok, msg):
        progress_dialog.done(0)
        progress_dialog.close()
        if ok:
            QMessageBox.information(self.main_view, "连接成功", "API连接成功！")
        else:
            QMessageBox.critical(self.main_view, "连接失败", f"API连接失败: {msg}")
            
    def save_settings(self):
        """保存设置"""
        if not hasattr(self, 'main_view'):
            return
            
        try:
            # 获取设置值
            api_key = self.main_view.api_key_input.text()
            api_base = self.main_view.api_url_input.text()
            
            # 验证API密钥格式
            if not api_key.startswith('sk-'):
                QMessageBox.warning(self.main_view, "设置失败", "API密钥格式不正确，应以'sk-'开头")
                return
            
            # 验证API基础URL格式
            if not api_base.startswith(('http://', 'https://')):
                QMessageBox.warning(self.main_view, "设置失败", "API基础URL格式不正确")
                return
            
            # 保存到数据库
            success = self.db.save_user_settings(
                self.current_user[0], 
                api_key=api_key,
                api_base=api_base
            )
            
            if success:
                # 更新当前API实例
                self.api = DeepSeekAPI(api_key, api_base)
                QMessageBox.information(self.main_view, "保存成功", "设置已成功保存")
            else:
                QMessageBox.critical(self.main_view, "保存失败", "保存设置时出错")
                
        except Exception as e:
            QMessageBox.critical(self.main_view, "保存失败", f"保存设置时出错: {str(e)}")
            
    def change_password(self):
        """修改密码"""
        if not hasattr(self, 'main_view'):
            return
            
        # 创建密码修改对话框
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
        
        dialog = QDialog(self.main_view)
        dialog.setWindowTitle("修改密码")
        dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout(dialog)
        
        # 旧密码
        old_password_label = QLabel("当前密码:")
        old_password_input = QLineEdit()
        old_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(old_password_label)
        layout.addWidget(old_password_input)
        
        # 新密码
        new_password_label = QLabel("新密码:")
        new_password_input = QLineEdit()
        new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(new_password_label)
        layout.addWidget(new_password_input)
        
        # 确认新密码
        confirm_password_label = QLabel("确认新密码:")
        confirm_password_input = QLineEdit()
        confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(confirm_password_label)
        layout.addWidget(confirm_password_input)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("保存")
        save_button.clicked.connect(lambda: self._save_new_password(
            dialog, old_password_input.text(), 
            new_password_input.text(), 
            confirm_password_input.text()
        ))
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(dialog.close)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        dialog.show()
            
    def _save_new_password(self, dialog, old_password, new_password, confirm_password):
        """保存新密码"""
        if not old_password or not new_password or not confirm_password:
            QMessageBox.warning(dialog, "修改失败", "所有字段都不能为空")
            return
            
        if new_password != confirm_password:
            QMessageBox.warning(dialog, "修改失败", "两次输入的新密码不一致")
            return
            
        # 验证旧密码
        hashed_old_password = hashlib.sha256(old_password.encode()).hexdigest()
        user = self.db.get_user(self.current_user[1], hashed_old_password)
        
        if not user:
            QMessageBox.warning(dialog, "修改失败", "当前密码不正确")
            return
            
        # 更新密码
        hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()
        
        # 这里需要实现数据库更新密码的方法
        # 例如：self.db.update_password(self.current_user[0], hashed_new_password)
        
        QMessageBox.information(dialog, "修改成功", "密码已成功修改")
        dialog.close()
            
    def export_data(self):
        """导出分析结果数据"""
        if not hasattr(self, 'main_view'):
            return
            
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        import pandas as pd
        from datetime import datetime
        import os
        
        try:
            # 获取用户的分析任务和结果
            user_id = self.current_user[0]
            analysis_tasks = self.db.get_analysis_tasks(user_id)
            
            if not analysis_tasks:
                QMessageBox.information(self.main_view, "导出数据", "暂无分析数据可导出。")
                return
            
            # 选择导出格式
            format_dialog = QFileDialog()
            format_dialog.setWindowTitle("选择导出格式")
            format_dialog.setNameFilter("Excel文件 (*.xlsx);;CSV文件 (*.csv);;PDF报告 (*.pdf)")
            format_dialog.setDefaultSuffix("xlsx")
            
            if format_dialog.exec() != QFileDialog.DialogCode.Accepted:
                return
                
            selected_filter = format_dialog.selectedNameFilter()
            file_path = format_dialog.selectedFiles()[0]
            
            # 准备导出数据
            export_data = []
            
            for task in analysis_tasks:
                task_id, task_name, platform, analysis_type, created_at = task
                
                # 获取该任务的分析结果
                results = self.db.get_analysis_results(task_id)
                
                for result in results:
                    result_id, result_type, result_data, result_created_at = result
                    
                    # 解析结果数据
                    try:
                        result_dict = json.loads(result_data)
                    except:
                        result_dict = {"raw_data": result_data}
                    
                    # 添加到导出数据
                    export_data.append({
                        "任务名称": task_name,
                        "平台": platform,
                        "分析类型": analysis_type,
                        "结果类型": result_type,
                        "创建时间": created_at,
                        "结果时间": result_created_at,
                        "结果数据": str(result_dict)
                    })
            
            # 创建DataFrame
            df = pd.DataFrame(export_data)
            
            # 根据选择的格式导出
            if "Excel" in selected_filter:
                self._export_to_excel(df, file_path)
            elif "CSV" in selected_filter:
                self._export_to_csv(df, file_path)
            elif "PDF" in selected_filter:
                self._export_to_pdf(df, file_path)
                
            QMessageBox.information(self.main_view, "导出成功", f"数据已成功导出到: {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self.main_view, "导出失败", f"导出数据时出错: {str(e)}")
            
    def _export_to_excel(self, df, file_path):
        """导出到Excel"""
        try:
            df.to_excel(file_path, index=False, engine='openpyxl')
        except ImportError:
            QMessageBox.warning(self.main_view, "Excel导出", 
                              "Excel导出需要安装openpyxl库。\n正在使用CSV格式导出...")
            self._export_to_csv(df, file_path.replace('.xlsx', '.csv'))
        except Exception as e:
            raise Exception(f"Excel生成失败: {str(e)}")
            
    def _export_to_csv(self, df, file_path):
        """导出到CSV"""
        try:
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
        except Exception as e:
            raise Exception(f"CSV生成失败: {str(e)}")
            
    def _export_to_pdf(self, df, file_path):
        """导出到PDF"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
            from reportlab.lib import colors
            
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            story = []
            
            # 创建表格数据
            table_data = [df.columns.tolist()] + df.values.tolist()
            
            # 创建表格
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)
            
            # 生成PDF
            doc.build(story)
            
        except ImportError:
            # 如果没有reportlab，使用简单的文本格式
            QMessageBox.warning(self.main_view, "PDF导出", 
                              "PDF导出需要安装reportlab库。\n正在使用文本格式导出...")
            self._export_to_csv(df, file_path.replace('.pdf', '.txt'))
        except Exception as e:
            raise Exception(f"PDF生成失败: {str(e)}")
            
    def import_data(self):
        """导入数据"""
        if not hasattr(self, 'main_view'):
            return
            
        QMessageBox.information(self.main_view, "导入数据", "数据导入功能正在开发中")
            
    def refresh_data(self):
        """刷新数据"""
        if not hasattr(self, 'main_view'):
            return
            
        # 刷新用户数据
        self.load_user_data()
            
    def exit_application(self):
        """退出应用程序"""
        if hasattr(self, 'main_view'):
            self.main_view.close()
        elif hasattr(self, 'login_view'):
            self.login_view.close()
        elif hasattr(self, 'register_view'):
            self.register_view.close()
            
    def show_help(self):
        """显示帮助信息"""
        if not hasattr(self, 'main_view'):
            return
            
        from PyQt6.QtWidgets import QMessageBox
        
        help_text = """
社交媒体营销分析系统使用说明

1. 登录与注册
   - 首次使用需要注册账号
   - 使用注册的用户名和密码登录系统

2. 数据分析
   - 选择分析类型、社交媒体平台和日期范围
   - 可以使用示例数据或导入自己的数据
   - 点击"开始分析"按钮进行数据分析

3. 营销方案
   - 基于数据分析结果生成营销方案
   - 可以查看、编辑和导出营销方案
   - 营销方案包含目标受众、内容策略等信息

4. 趋势分析
   - 预测社交媒体平台的发展趋势
   - 选择预测类型和时间范围
   - 系统会提供详细的趋势分析和建议

5. 内容优化
   - 输入要发布的内容
   - 选择发布平台和内容类型
   - 系统会提供优化建议和修改后的内容

6. 报告导出
   - 生成各种类型的分析报告
   - 支持多种格式导出
   - 可以自定义报告内容和格式
        """
        
        QMessageBox.information(self.main_view, "使用说明", help_text)
            
    def show_about(self):
        """显示关于信息"""
        if not hasattr(self, 'main_view'):
            return
            
        from PyQt6.QtWidgets import QMessageBox
        
        about_text = """
社交媒体营销分析系统

版本: 1.0.0
开发者: Gondrysime
日期: 2025年6月

社交媒体营销分析系统是一个集成了人工智能的营销分析工具，
可以帮助企业和营销人员分析社交媒体数据，制定精准的营销策略。

系统特点:
- 多平台数据分析
- 人工智能辅助营销决策
- 趋势预测和内容优化
- 专业报告生成和导出
- 用户友好的界面设计
        """
        
        QMessageBox.information(self.main_view, "关于", about_text)    

    def create_new_plan(self):
        """新建营销方案（待开发）"""
        if hasattr(self, 'main_view'):
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self.main_view, "提示", "新建营销方案功能待开发！")
    
    def delete_marketing_plan(self):
        """删除营销方案（待开发）"""
        if hasattr(self, 'main_view'):
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self.main_view, "提示", "删除营销方案功能待开发！")
    
    def export_marketing_plan(self):
        """导出营销方案（待开发）"""
        if hasattr(self, 'main_view'):
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self.main_view, "提示", "导出营销方案功能待开发！")
    
    def share_marketing_plan(self):
        """分享营销方案"""
        QMessageBox.information(self.main_view, "分享", "营销方案分享功能开发中...")
        
    # 新增界面的处理方法
    def create_strategy(self, strategy_data):
        """创建营销策略"""
        try:
            # 这里应该保存策略到数据库
            QMessageBox.information(self.marketing_strategy_view, "成功", "营销策略创建成功")
        except Exception as e:
            QMessageBox.critical(self.marketing_strategy_view, "错误", f"创建策略失败: {str(e)}")
            
    def update_strategy(self, strategy_data):
        """更新营销策略"""
        try:
            # 这里应该更新数据库中的策略
            QMessageBox.information(self.marketing_strategy_view, "成功", "营销策略更新成功")
        except Exception as e:
            QMessageBox.critical(self.marketing_strategy_view, "错误", f"更新策略失败: {str(e)}")
            
    def delete_strategy(self, strategy_id):
        """删除营销策略"""
        try:
            # 这里应该从数据库删除策略
            QMessageBox.information(self.marketing_strategy_view, "成功", "营销策略删除成功")
        except Exception as e:
            QMessageBox.critical(self.marketing_strategy_view, "错误", f"删除策略失败: {str(e)}")
            
    def start_prediction(self, prediction_params):
        """开始趋势预测"""
        try:
            # 这里应该调用AI服务进行预测
            QMessageBox.information(self.trend_prediction_view, "开始预测", "趋势预测已开始...")
        except Exception as e:
            QMessageBox.critical(self.trend_prediction_view, "错误", f"预测失败: {str(e)}")
            
    def complete_prediction(self, prediction_result):
        """完成趋势预测"""
        try:
            # 这里应该处理预测结果
            QMessageBox.information(self.trend_prediction_view, "预测完成", "趋势预测已完成")
        except Exception as e:
            QMessageBox.critical(self.trend_prediction_view, "错误", f"处理预测结果失败: {str(e)}")
            
    def start_optimization(self, optimization_params):
        """开始内容优化"""
        try:
            # 这里应该调用AI服务进行内容优化
            QMessageBox.information(self.content_optimization_view, "开始优化", "内容优化已开始...")
        except Exception as e:
            QMessageBox.critical(self.content_optimization_view, "错误", f"优化失败: {str(e)}")
            
    def complete_optimization(self, optimization_result):
        """完成内容优化"""
        try:
            # 这里应该处理优化结果
            QMessageBox.information(self.content_optimization_view, "优化完成", "内容优化已完成")
        except Exception as e:
            QMessageBox.critical(self.content_optimization_view, "错误", f"处理优化结果失败: {str(e)}")
            
    def generate_report(self, report_params):
        """生成报告"""
        try:
            # 这里应该生成报告
            QMessageBox.information(self.report_management_view, "报告生成", "报告生成中...")
        except Exception as e:
            QMessageBox.critical(self.report_management_view, "错误", f"生成报告失败: {str(e)}")
            
    def export_report_file(self, file_path):
        """导出报告文件"""
        try:
            # 这里应该导出报告文件
            QMessageBox.information(self.report_management_view, "导出成功", f"报告已导出到: {file_path}")
        except Exception as e:
            QMessageBox.critical(self.report_management_view, "错误", f"导出报告失败: {str(e)}")
            
    def save_system_settings(self, settings):
        """保存系统设置"""
        try:
            # 这里应该保存系统设置
            QMessageBox.information(self.system_settings_view, "设置保存", "系统设置已保存")
        except Exception as e:
            QMessageBox.critical(self.system_settings_view, "错误", f"保存设置失败: {str(e)}")
            
    def reset_system_settings(self):
        """重置系统设置"""
        try:
            # 这里应该重置系统设置
            QMessageBox.information(self.system_settings_view, "设置重置", "系统设置已重置")
        except Exception as e:
            QMessageBox.critical(self.system_settings_view, "错误", f"重置设置失败: {str(e)}")

    def show_data_import_view(self):
        """显示数据导入界面"""
        self.data_import_view = DataImportView(self.main_view)
        self.data_import_view.show()


class ApiTestThread(QThread):
    result_signal = pyqtSignal(bool, str)

    def __init__(self, api_key, api_base):
        super().__init__()
        self.api_key = api_key
        self.api_base = api_base

    def run(self):
        try:
            from models.deepseek_api import DeepSeekAPI
            api = DeepSeekAPI(self.api_key, self.api_base)
            ok = api.test_connection()
            self.result_signal.emit(ok, "" if ok else "API连接失败")
        except Exception as e:
            self.result_signal.emit(False, str(e))    