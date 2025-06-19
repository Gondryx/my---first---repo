from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTextEdit, QComboBox, QSpinBox, QGroupBox, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QFrame, QLineEdit, 
                             QCheckBox, QListWidget, QSplitter, QProgressBar, QSlider,
                             QTabWidget, QFormLayout)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QDate
from PyQt6.QtGui import QFont
import json
import os

class SystemSettingsView(QWidget):
    """系统设置界面"""
    
    settings_saved_signal = pyqtSignal(dict)
    settings_reset_signal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = {}
        self.init_ui()
        self.load_default_settings()
        
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("系统设置")
        self.setMinimumSize(1000, 700)
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("系统设置")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 添加各个设置标签页
        self.create_general_settings_tab()
        self.create_ai_settings_tab()
        self.create_data_settings_tab()
        self.create_interface_settings_tab()
        self.create_export_settings_tab()
        self.create_about_tab()
        
        main_layout.addWidget(self.tab_widget)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("保存设置")
        self.save_btn.clicked.connect(self.save_settings)
        
        self.reset_btn = QPushButton("重置设置")
        self.reset_btn.clicked.connect(self.reset_settings)
        
        self.back_btn = QPushButton("返回主界面")
        self.back_btn.clicked.connect(self.go_back)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.reset_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.back_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def create_general_settings_tab(self):
        """创建常规设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 系统信息组
        system_group = QGroupBox("系统信息")
        system_layout = QFormLayout()
        
        self.system_name = QLineEdit("社交媒体营销分析系统")
        self.system_name.setReadOnly(True)
        system_layout.addRow("系统名称:", self.system_name)
        
        self.system_version = QLineEdit("v1.0.0")
        self.system_version.setReadOnly(True)
        system_layout.addRow("系统版本:", self.system_version)
        
        self.python_version = QLineEdit("Python 3.9.13")
        self.python_version.setReadOnly(True)
        system_layout.addRow("Python版本:", self.python_version)
        
        system_group.setLayout(system_layout)
        layout.addWidget(system_group)
        
        # 用户偏好组
        user_group = QGroupBox("用户偏好")
        user_layout = QFormLayout()
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["简体中文", "English", "繁體中文"])
        user_layout.addRow("界面语言:", self.language_combo)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["默认主题", "深色主题", "浅色主题", "蓝色主题"])
        user_layout.addRow("界面主题:", self.theme_combo)
        
        self.auto_save = QCheckBox("自动保存")
        self.auto_save.setChecked(True)
        user_layout.addRow("自动保存:", self.auto_save)
        
        self.auto_backup = QCheckBox("自动备份")
        self.auto_backup.setChecked(True)
        user_layout.addRow("自动备份:", self.auto_backup)
        
        user_group.setLayout(user_layout)
        layout.addWidget(user_group)
        
        # 性能设置组
        performance_group = QGroupBox("性能设置")
        perf_layout = QFormLayout()
        
        self.max_threads = QSpinBox()
        self.max_threads.setRange(1, 16)
        self.max_threads.setValue(4)
        perf_layout.addRow("最大线程数:", self.max_threads)
        
        self.cache_size = QSpinBox()
        self.cache_size.setRange(100, 10000)
        self.cache_size.setValue(1000)
        self.cache_size.setSuffix(" MB")
        perf_layout.addRow("缓存大小:", self.cache_size)
        
        self.auto_refresh = QCheckBox("自动刷新")
        self.auto_refresh.setChecked(False)
        perf_layout.addRow("自动刷新:", self.auto_refresh)
        
        performance_group.setLayout(perf_layout)
        layout.addWidget(performance_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "常规设置")
        
    def create_ai_settings_tab(self):
        """创建AI设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # AI服务配置组
        ai_service_group = QGroupBox("AI服务配置")
        ai_layout = QFormLayout()
        
        self.ai_provider = QComboBox()
        self.ai_provider.addItems(["DeepSeek", "OpenAI", "Claude", "本地模型"])
        ai_layout.addRow("AI提供商:", self.ai_provider)
        
        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key.setPlaceholderText("输入API密钥")
        ai_layout.addRow("API密钥:", self.api_key)
        
        self.api_base_url = QLineEdit("https://api.deepseek.com")
        ai_layout.addRow("API地址:", self.api_base_url)
        
        self.model_name = QComboBox()
        self.model_name.addItems(["deepseek-chat", "deepseek-coder", "gpt-4", "gpt-3.5-turbo"])
        ai_layout.addRow("模型名称:", self.model_name)
        
        ai_service_group.setLayout(ai_layout)
        layout.addWidget(ai_service_group)
        
        # AI参数设置组
        ai_params_group = QGroupBox("AI参数设置")
        params_layout = QFormLayout()
        
        self.max_tokens = QSpinBox()
        self.max_tokens.setRange(100, 8000)
        self.max_tokens.setValue(2000)
        params_layout.addRow("最大令牌数:", self.max_tokens)
        
        self.temperature = QSlider(Qt.Orientation.Horizontal)
        self.temperature.setRange(0, 100)
        self.temperature.setValue(70)
        self.temperature_label = QLabel("0.7")
        self.temperature.valueChanged.connect(
            lambda v: self.temperature_label.setText(f"{v/100:.1f}")
        )
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(self.temperature)
        temp_layout.addWidget(self.temperature_label)
        params_layout.addRow("温度参数:", temp_layout)
        
        self.top_p = QSlider(Qt.Orientation.Horizontal)
        self.top_p.setRange(0, 100)
        self.top_p.setValue(90)
        self.top_p_label = QLabel("0.9")
        self.top_p.valueChanged.connect(
            lambda v: self.top_p_label.setText(f"{v/100:.1f}")
        )
        top_p_layout = QHBoxLayout()
        top_p_layout.addWidget(self.top_p)
        top_p_layout.addWidget(self.top_p_label)
        params_layout.addRow("Top-P参数:", top_p_layout)
        
        ai_params_group.setLayout(params_layout)
        layout.addWidget(ai_params_group)
        
        # AI功能开关组
        ai_features_group = QGroupBox("AI功能开关")
        features_layout = QVBoxLayout()
        
        self.enable_content_optimization = QCheckBox("启用内容优化")
        self.enable_content_optimization.setChecked(True)
        features_layout.addWidget(self.enable_content_optimization)
        
        self.enable_trend_prediction = QCheckBox("启用趋势预测")
        self.enable_trend_prediction.setChecked(True)
        features_layout.addWidget(self.enable_trend_prediction)
        
        self.enable_sentiment_analysis = QCheckBox("启用情感分析")
        self.enable_sentiment_analysis.setChecked(True)
        features_layout.addWidget(self.enable_sentiment_analysis)
        
        self.enable_competitor_analysis = QCheckBox("启用竞争分析")
        self.enable_competitor_analysis.setChecked(False)
        features_layout.addWidget(self.enable_competitor_analysis)
        
        ai_features_group.setLayout(features_layout)
        layout.addWidget(ai_features_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "AI设置")
        
    def create_data_settings_tab(self):
        """创建数据设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 数据源配置组
        data_source_group = QGroupBox("数据源配置")
        source_layout = QFormLayout()
        
        self.default_data_source = QComboBox()
        self.default_data_source.addItems(["CSV文件", "Excel文件", "数据库", "API接口"])
        source_layout.addRow("默认数据源:", self.default_data_source)
        
        self.data_directory = QLineEdit("./data")
        source_layout.addRow("数据目录:", self.data_directory)
        
        self.backup_directory = QLineEdit("./backup")
        source_layout.addRow("备份目录:", self.backup_directory)
        
        data_source_group.setLayout(source_layout)
        layout.addWidget(data_source_group)
        
        # 数据处理设置组
        data_processing_group = QGroupBox("数据处理设置")
        processing_layout = QFormLayout()
        
        self.max_file_size = QSpinBox()
        self.max_file_size.setRange(1, 1000)
        self.max_file_size.setValue(100)
        self.max_file_size.setSuffix(" MB")
        processing_layout.addRow("最大文件大小:", self.max_file_size)
        
        self.auto_clean_data = QCheckBox("自动清理数据")
        self.auto_clean_data.setChecked(True)
        processing_layout.addRow("自动清理:", self.auto_clean_data)
        
        self.data_retention_days = QSpinBox()
        self.data_retention_days.setRange(1, 365)
        self.data_retention_days.setValue(30)
        self.data_retention_days.setSuffix(" 天")
        processing_layout.addRow("数据保留期:", self.data_retention_days)
        
        data_processing_group.setLayout(processing_layout)
        layout.addWidget(data_processing_group)
        
        # 数据安全设置组
        data_security_group = QGroupBox("数据安全设置")
        security_layout = QVBoxLayout()
        
        self.encrypt_data = QCheckBox("加密敏感数据")
        self.encrypt_data.setChecked(True)
        security_layout.addWidget(self.encrypt_data)
        
        self.log_data_access = QCheckBox("记录数据访问")
        self.log_data_access.setChecked(True)
        security_layout.addWidget(self.log_data_access)
        
        self.anonymize_data = QCheckBox("匿名化用户数据")
        self.anonymize_data.setChecked(False)
        security_layout.addWidget(self.anonymize_data)
        
        data_security_group.setLayout(security_layout)
        layout.addWidget(data_security_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "数据设置")
        
    def create_interface_settings_tab(self):
        """创建界面设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 界面布局设置组
        layout_group = QGroupBox("界面布局设置")
        layout_settings = QFormLayout()
        
        self.default_window_size = QComboBox()
        self.default_window_size.addItems(["1024x768", "1280x720", "1920x1080", "自适应"])
        layout_settings.addRow("默认窗口大小:", self.default_window_size)
        
        self.show_toolbar = QCheckBox("显示工具栏")
        self.show_toolbar.setChecked(True)
        layout_settings.addRow("工具栏:", self.show_toolbar)
        
        self.show_statusbar = QCheckBox("显示状态栏")
        self.show_statusbar.setChecked(True)
        layout_settings.addRow("状态栏:", self.show_statusbar)
        
        self.show_sidebar = QCheckBox("显示侧边栏")
        self.show_sidebar.setChecked(True)
        layout_settings.addRow("侧边栏:", self.show_sidebar)
        
        layout_group.setLayout(layout_settings)
        layout.addWidget(layout_group)
        
        # 图表设置组
        chart_group = QGroupBox("图表设置")
        chart_layout = QFormLayout()
        
        self.chart_theme = QComboBox()
        self.chart_theme.addItems(["默认", "深色", "浅色", "蓝色", "绿色"])
        chart_layout.addRow("图表主题:", self.chart_theme)
        
        self.chart_dpi = QSpinBox()
        self.chart_dpi.setRange(72, 300)
        self.chart_dpi.setValue(100)
        chart_layout.addRow("图表DPI:", self.chart_dpi)
        
        self.auto_save_charts = QCheckBox("自动保存图表")
        self.auto_save_charts.setChecked(True)
        chart_layout.addRow("自动保存图表:", self.auto_save_charts)
        
        chart_group.setLayout(chart_layout)
        layout.addWidget(chart_group)
        
        # 通知设置组
        notification_group = QGroupBox("通知设置")
        notification_layout = QVBoxLayout()
        
        self.show_notifications = QCheckBox("显示系统通知")
        self.show_notifications.setChecked(True)
        notification_layout.addWidget(self.show_notifications)
        
        self.sound_notifications = QCheckBox("声音通知")
        self.sound_notifications.setChecked(False)
        notification_layout.addWidget(self.sound_notifications)
        
        self.email_notifications = QCheckBox("邮件通知")
        self.email_notifications.setChecked(False)
        notification_layout.addWidget(self.email_notifications)
        
        notification_group.setLayout(notification_layout)
        layout.addWidget(notification_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "界面设置")
        
    def create_export_settings_tab(self):
        """创建导出设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 导出格式设置组
        export_format_group = QGroupBox("导出格式设置")
        format_layout = QFormLayout()
        
        self.default_export_format = QComboBox()
        self.default_export_format.addItems(["PDF", "Excel", "Word", "HTML", "JSON"])
        format_layout.addRow("默认导出格式:", self.default_export_format)
        
        self.export_directory = QLineEdit("./exports")
        format_layout.addRow("导出目录:", self.export_directory)
        
        self.auto_export = QCheckBox("自动导出")
        self.auto_export.setChecked(False)
        format_layout.addRow("自动导出:", self.auto_export)
        
        export_format_group.setLayout(format_layout)
        layout.addWidget(export_format_group)
        
        # 报告模板设置组
        report_template_group = QGroupBox("报告模板设置")
        template_layout = QFormLayout()
        
        self.report_template = QComboBox()
        self.report_template.addItems(["标准模板", "简洁模板", "详细模板", "自定义模板"])
        template_layout.addRow("报告模板:", self.report_template)
        
        self.include_logo = QCheckBox("包含Logo")
        self.include_logo.setChecked(True)
        template_layout.addRow("包含Logo:", self.include_logo)
        
        self.include_footer = QCheckBox("包含页脚")
        self.include_footer.setChecked(True)
        template_layout.addRow("包含页脚:", self.include_footer)
        
        report_template_group.setLayout(template_layout)
        layout.addWidget(report_template_group)
        
        # 数据导出设置组
        data_export_group = QGroupBox("数据导出设置")
        data_export_layout = QFormLayout()
        
        self.export_encoding = QComboBox()
        self.export_encoding.addItems(["UTF-8", "GBK", "GB2312", "UTF-16"])
        data_export_layout.addRow("导出编码:", self.export_encoding)
        
        self.include_metadata = QCheckBox("包含元数据")
        self.include_metadata.setChecked(True)
        data_export_layout.addRow("包含元数据:", self.include_metadata)
        
        self.compress_export = QCheckBox("压缩导出文件")
        self.compress_export.setChecked(False)
        data_export_layout.addRow("压缩文件:", self.compress_export)
        
        data_export_group.setLayout(data_export_layout)
        layout.addWidget(data_export_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "导出设置")
        
    def create_about_tab(self):
        """创建关于标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 系统信息
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setPlainText("""
社交媒体营销分析系统 v1.0.0

系统简介:
本系统是一个基于Python和PyQt6开发的社交媒体营销分析工具，
集成了DeepSeek AI技术，提供数据分析、趋势预测、内容优化等功能。

主要功能:
• 社交媒体数据分析
• AI驱动的趋势预测
• 智能内容优化
• 营销策略制定
• 报告生成和导出

技术栈:
• Python 3.9.13
• PyQt6 6.4.0
• DeepSeek AI API
• SQLite数据库
• Matplotlib图表库

开发团队:
• 开发者: AI助手
• 技术支持: DeepSeek
• 界面设计: PyQt6

版权信息:
© 2024 社交媒体营销分析系统
保留所有权利

联系方式:
• 邮箱: support@example.com
• 官网: https://example.com
• 文档: https://docs.example.com
        """)
        
        layout.addWidget(about_text)
        self.tab_widget.addTab(tab, "关于系统")
        
    def load_default_settings(self):
        """加载默认设置"""
        self.settings = {
            'language': '简体中文',
            'theme': '默认主题',
            'auto_save': True,
            'auto_backup': True,
            'max_threads': 4,
            'cache_size': 1000,
            'ai_provider': 'DeepSeek',
            'model_name': 'deepseek-chat',
            'max_tokens': 2000,
            'temperature': 0.7,
            'top_p': 0.9,
            'enable_content_optimization': True,
            'enable_trend_prediction': True,
            'enable_sentiment_analysis': True,
            'default_export_format': 'PDF',
            'export_directory': './exports'
        }
        
    def save_settings(self):
        """保存设置"""
        try:
            # 收集所有设置
            settings = {
                'language': self.language_combo.currentText(),
                'theme': self.theme_combo.currentText(),
                'auto_save': self.auto_save.isChecked(),
                'auto_backup': self.auto_backup.isChecked(),
                'max_threads': self.max_threads.value(),
                'cache_size': self.cache_size.value(),
                'ai_provider': self.ai_provider.currentText(),
                'api_key': self.api_key.text(),
                'api_base_url': self.api_base_url.text(),
                'model_name': self.model_name.currentText(),
                'max_tokens': self.max_tokens.value(),
                'temperature': self.temperature.value() / 100,
                'top_p': self.top_p.value() / 100,
                'enable_content_optimization': self.enable_content_optimization.isChecked(),
                'enable_trend_prediction': self.enable_trend_prediction.isChecked(),
                'enable_sentiment_analysis': self.enable_sentiment_analysis.isChecked(),
                'enable_competitor_analysis': self.enable_competitor_analysis.isChecked(),
                'default_data_source': self.default_data_source.currentText(),
                'data_directory': self.data_directory.text(),
                'backup_directory': self.backup_directory.text(),
                'max_file_size': self.max_file_size.value(),
                'auto_clean_data': self.auto_clean_data.isChecked(),
                'data_retention_days': self.data_retention_days.value(),
                'encrypt_data': self.encrypt_data.isChecked(),
                'log_data_access': self.log_data_access.isChecked(),
                'anonymize_data': self.anonymize_data.isChecked(),
                'default_window_size': self.default_window_size.currentText(),
                'show_toolbar': self.show_toolbar.isChecked(),
                'show_statusbar': self.show_statusbar.isChecked(),
                'show_sidebar': self.show_sidebar.isChecked(),
                'chart_theme': self.chart_theme.currentText(),
                'chart_dpi': self.chart_dpi.value(),
                'auto_save_charts': self.auto_save_charts.isChecked(),
                'show_notifications': self.show_notifications.isChecked(),
                'sound_notifications': self.sound_notifications.isChecked(),
                'email_notifications': self.email_notifications.isChecked(),
                'default_export_format': self.default_export_format.currentText(),
                'export_directory': self.export_directory.text(),
                'auto_export': self.auto_export.isChecked(),
                'report_template': self.report_template.currentText(),
                'include_logo': self.include_logo.isChecked(),
                'include_footer': self.include_footer.isChecked(),
                'export_encoding': self.export_encoding.currentText(),
                'include_metadata': self.include_metadata.isChecked(),
                'compress_export': self.compress_export.isChecked()
            }
            
            # 保存到文件
            settings_file = "config/settings.json"
            os.makedirs(os.path.dirname(settings_file), exist_ok=True)
            
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
                
            self.settings = settings
            self.settings_saved_signal.emit(settings)
            
            QMessageBox.information(self, "成功", "设置已保存")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存设置失败: {str(e)}")
            
    def reset_settings(self):
        """重置设置"""
        reply = QMessageBox.question(self, "确认重置", 
                                   "确定要重置所有设置吗？",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.load_default_settings()
            self.settings_reset_signal.emit()
            QMessageBox.information(self, "成功", "设置已重置为默认值")
            
    def go_back(self):
        """返回主界面"""
        if hasattr(self.parent(), 'show_main_view'):
            self.parent().show_main_view() 