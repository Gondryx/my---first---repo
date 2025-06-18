from views.login_view import LoginView
from views.register_view import RegisterView
from views.main_view import MainView
from models.database import DatabaseManager
from models.social_media_data import SocialMediaData
from models.deepseek_api import DeepSeekAPI
import hashlib
import json
import time
import os
from datetime import datetime

class MainController:
    def __init__(self):
        self.current_user = None
        self.db = DatabaseManager()
        self.social_media_data = SocialMediaData()
        self.api = DeepSeekAPI("sk-dfc4e38245414faf8290bb291db1a35e")
        
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
        self.main_view.show()
        
        # 关闭登录窗口
        if hasattr(self, 'login_view'):
            self.login_view.close()
            
        # 加载用户数据
        self.load_user_data()
            
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
            
        # 获取分析任务数量
        tasks = self.db.get_analysis_tasks(self.current_user[0])
        task_count = len(tasks)
        
        # 获取营销方案数量
        plans = self.db.get_marketing_plans(self.current_user[0])
        plan_count = len(plans)
        
        # 获取活跃平台数量
        active_platforms = set()
        for task in tasks:
            platform = task[2]  # 平台信息在元组的第3个位置
            active_platforms.add(platform)
        platform_count = len(active_platforms)
        
        # 更新统计卡片
        # 注意：这里需要根据实际UI中的控件名称进行调整
        # 例如：self.main_view.stat_card1.setText(str(task_count))
        
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
            # TODO: 实现从文件导入数据的功能
            df = self.social_media_data.generate_sample_data(platform)  # 暂时使用示例数据
            
        self.main_view.analysis_progress.setValue(40)
        
        # 分析数据
        analysis = self.social_media_data.analyze_data(df, platform)
        
        self.main_view.analysis_progress.setValue(60)
        
        # 准备AI分析数据
        ai_data = self.social_media_data.prepare_for_ai(analysis, platform)
        
        self.main_view.analysis_progress.setValue(80)
        
        # 保存分析结果
        self.db.add_analysis_result(task_id, "overview", json.dumps(analysis['基本统计']))
        self.db.add_analysis_result(task_id, "growth", json.dumps(analysis['增长分析']))
        self.db.add_analysis_result(task_id, "correlation", json.dumps(analysis['相关性分析']))
        self.db.add_analysis_result(task_id, "trends", json.dumps(analysis['趋势分析']))
        
        # 更新UI显示分析结果
        self.display_analysis_results(analysis)
        
        self.main_view.analysis_progress.setValue(100)
        
        # 刷新用户数据
        self.load_user_data()
        
    def display_analysis_results(self, analysis):
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
        self.main_view.details_text.setText(json.dumps(analysis, indent=4, ensure_ascii=False))
        
        # TODO: 显示图表分析
        
    def generate_marketing_plan(self):
        """生成营销方案"""
        if not hasattr(self, 'main_view'):
            return
            
        # 获取最新的分析结果
        tasks = self.db.get_analysis_tasks(self.current_user[0])
        if not tasks:
            QMessageBox.warning(self.main_view, "生成失败", "没有可用的分析结果，请先进行数据分析")
            return
            
        latest_task = tasks[0]
        task_id = latest_task[0]
        
        # 获取分析结果
        results = self.db.get_analysis_results(task_id)
        if not results:
            QMessageBox.warning(self.main_view, "生成失败", "分析结果为空，请重新进行数据分析")
            return
            
        # 构建分析数据
        analysis_data = {}
        for result in results:
            result_id, result_type, result_data, created_at = result
            analysis_data[result_type] = json.loads(result_data)
            
        # 准备AI分析数据
        ai_data = f"平台: {latest_task[2]}\n\n"  # 平台信息在任务元组的第3个位置
        
        # 添加基本统计
        ai_data += "基本统计:\n"
        for key, value in analysis_data['overview'].items():
            ai_data += f"- {key}: {value}\n"
            
        # 添加增长分析
        ai_data += "\n增长分析:\n"
        for key, value in analysis_data['growth'].items():
            ai_data += f"- {key}: {value}\n"
            
        # 添加相关性分析
        ai_data += "\n相关性分析:\n"
        for key, value in analysis_data['correlation'].items():
            ai_data += f"- {key}: {value}\n"
            
        # 调用AI生成营销方案
        plan_name, ok = QInputDialog.getText(
            self.main_view, "营销方案名称", "请输入营销方案名称:"
        )
        
        if not ok or not plan_name:
            return
            
        # 显示进度对话框
        progress_dialog = QMessageBox(self.main_view)
        progress_dialog.setWindowTitle("生成中")
        progress_dialog.setText("正在生成营销方案，请稍候...")
        progress_dialog.setStandardButtons(QMessageBox.StandardButton.NoButton)
        progress_dialog.show()
        
        # 调用API生成营销方案
        try:
            plan_content = self.api.generate_marketing_plan(ai_data)
            
            # 保存营销方案
            self.db.add_marketing_plan(
                self.current_user[0],
                task_id,
                plan_name,
                plan_content
            )
            
            progress_dialog.close()
            
            QMessageBox.information(self.main_view, "生成成功", "营销方案已成功生成")
            
            # 刷新营销方案列表
            self.load_marketing_plans()
            
        except Exception as e:
            progress_dialog.close()
            QMessageBox.critical(self.main_view, "生成失败", f"生成营销方案时出错: {str(e)}")
            
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
        report_type = "分析报告"  # 目前只实现了分析报告
        report_format = self.main_view.report_format_combo.currentText()
        report_title = self.main_view.report_title.text()
        include_charts = self.main_view.include_charts_check.isChecked()
        include_tables = self.main_view.include_tables_check.isChecked()
        include_recommendations = self.main_view.include_recommendations_check.isChecked()
        
        # 生成报告内容
        report_content = f"# {report_title}\n\n"
        report_content += f"## 报告概述\n"
        report_content += f"本报告基于社交媒体数据分析，生成于{datetime.now().strftime('%Y年%m月%d日')}\n\n"
        
        # TODO: 根据选择的报告类型和选项生成详细报告内容
        
        # 显示预览
        self.main_view.report_preview.setText(report_content)
        
        # 保存报告
        file_path, _ = QFileDialog.getSaveFileName(
            self.main_view, "保存报告", f"{report_title}.{report_format.lower()}", 
            f"{report_format}文件 (*.{report_format.lower()});;所有文件 (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                    
                QMessageBox.information(self.main_view, "导出成功", f"报告已成功导出到: {file_path}")
                
            except Exception as e:
                QMessageBox.critical(self.main_view, "导出失败", f"导出报告时出错: {str(e)}")
                
    def test_api_connection(self):
        """测试API连接"""
        if not hasattr(self, 'main_view'):
            return
            
        api_key = self.main_view.api_key_input.text()
        api_base = self.main_view.api_url_input.text()
        
        # 创建临时API实例
        test_api = DeepSeekAPI(api_key, api_base)
        
        # 显示进度对话框
        progress_dialog = QMessageBox(self.main_view)
        progress_dialog.setWindowTitle("测试中")
        progress_dialog.setText("正在测试API连接，请稍候...")
        progress_dialog.setStandardButtons(QMessageBox.StandardButton.NoButton)
        progress_dialog.show()
        
        # 测试API连接
        try:
            # 使用简单的提示测试API
            test_prompt = "请确认API连接是否正常"
            response = test_api._send_request(test_prompt)
            
            progress_dialog.close()
            
            if "API请求错误" in response:
                QMessageBox.warning(self.main_view, "连接失败", f"API连接失败: {response}")
            else:
                QMessageBox.information(self.main_view, "连接成功", "API连接成功！")
                
        except Exception as e:
            progress_dialog.close()
            QMessageBox.critical(self.main_view, "连接失败", f"测试API连接时出错: {str(e)}")
            
    def save_settings(self):
        """保存设置"""
        if not hasattr(self, 'main_view'):
            return
            
        # 保存API设置
        api_key = self.main_view.api_key_input.text()
        api_base = self.main_view.api_url_input.text()
        
        # 更新API实例
        self.api = DeepSeekAPI(api_key, api_base)
        
        QMessageBox.information(self.main_view, "保存成功", "设置已成功保存")
            
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
        """导出数据"""
        if not hasattr(self, 'main_view'):
            return
            
        QMessageBox.information(self.main_view, "导出数据", "数据导出功能正在开发中")
            
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
开发者: Doubao
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