from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QFrame, QSplitter,
                             QComboBox, QDateEdit, QTextEdit, QLineEdit, QFileDialog,
                             QProgressBar, QGroupBox, QListWidget, QHeaderView,
                             QStackedWidget, QInputDialog, QMenu, QToolBar, QScrollArea)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QAction
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('qtagg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import json
import datetime

class MainView(QMainWindow):
    logout_signal = pyqtSignal()
    import_data_signal = pyqtSignal()
    analyze_data_signal = pyqtSignal()
    generate_plan_signal = pyqtSignal()
    predict_trends_signal = pyqtSignal()
    optimize_content_signal = pyqtSignal()
    export_report_signal = pyqtSignal()
    export_data_signal = pyqtSignal()
    test_api_signal = pyqtSignal()
    save_settings_signal = pyqtSignal()
    change_password_signal = pyqtSignal()
    refresh_data_signal = pyqtSignal()
    exit_signal = pyqtSignal()
    help_signal = pyqtSignal()
    about_signal = pyqtSignal()
    create_plan_signal = pyqtSignal()
    delete_plan_signal = pyqtSignal()
    export_plan_signal = pyqtSignal()
    share_plan_signal = pyqtSignal()
    
    # 新增界面的信号
    show_marketing_strategy_signal = pyqtSignal()
    show_trend_prediction_signal = pyqtSignal()
    show_content_optimization_signal = pyqtSignal()
    show_report_management_signal = pyqtSignal()
    show_system_settings_signal = pyqtSignal()
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.current_user = controller.current_user
        self.initUI()
        
    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle(f'MediaSage - 欢迎：{self.current_user[1]}')
        self.setMinimumSize(1000, 600)
        
        # 创建工具栏
        self.create_tool_bar()
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建标签页控件
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setStyleSheet("QTabBar::tab { height: 30px; }")
        
        # 添加各个标签页（只保留一个系统设置Tab）
        self.create_dashboard_tab()
        self.create_analysis_tab()
        self.create_marketing_tab()
        self.create_trends_tab()
        self.create_content_tab()
        self.create_reports_tab()
        # 只保留一次系统设置Tab
        if not hasattr(self, '_settings_tab_added'):
            self.create_settings_tab()
            self._settings_tab_added = True
        
        main_layout.addWidget(self.tabs)
        
    def create_tool_bar(self):
        """创建精简工具栏（去除设置按钮，增加关于）"""
        toolbar = QToolBar("工具栏")
        self.addToolBar(toolbar)

        # 刷新按钮
        refresh_action = QAction("刷新", self)
        refresh_action.triggered.connect(lambda: self.refresh_data_signal.emit())
        toolbar.addAction(refresh_action)

        # 分隔符
        toolbar.addSeparator()

        # 帮助按钮
        help_action = QAction("帮助", self)
        help_action.triggered.connect(self.show_help_dialog)
        toolbar.addAction(help_action)

        # 关于按钮
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about_dialog)
        toolbar.addAction(about_action)
        
    def create_dashboard_tab(self):
        """创建仪表盘标签页"""
        dashboard_tab = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_tab)
        
        # 创建标题
        title_label = QLabel('数据概览')
        title_font = QFont('Arial', 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dashboard_layout.addWidget(title_label)
        
        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        dashboard_layout.addWidget(line)
        
        # 创建统计卡片布局
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(20)
        
        # 创建统计卡片
        self.create_stat_card("总分析任务", "0", self.stats_layout, "#1E88E5")
        self.create_stat_card("已完成分析", "0", self.stats_layout, "#43A047")
        self.create_stat_card("营销方案", "0", self.stats_layout, "#FB8C00")
        self.create_stat_card("活跃平台", "0", self.stats_layout, "#E53935")
        
        dashboard_layout.addLayout(self.stats_layout)
        
        # 创建图表布局
        charts_layout = QHBoxLayout()
        
        # 创建趋势图表
        trends_frame = QGroupBox("粉丝增长趋势")
        trends_layout = QVBoxLayout(trends_frame)
        self.trends_chart = self.create_chart()
        trends_layout.addWidget(self.trends_chart)
        charts_layout.addWidget(trends_frame)
        
        # 创建平台分布图表
        platform_frame = QGroupBox("平台分布")
        platform_layout = QVBoxLayout(platform_frame)
        self.platform_chart = self.create_chart()
        platform_layout.addWidget(self.platform_chart)
        charts_layout.addWidget(platform_frame)
        
        dashboard_layout.addLayout(charts_layout)
        
        # 添加最近活动表格
        recent_activity_frame = QGroupBox("最近活动")
        recent_activity_layout = QVBoxLayout(recent_activity_frame)
        
        self.recent_activity_table = QTableWidget(5, 4)
        self.recent_activity_table.setHorizontalHeaderLabels(["时间", "活动类型", "详情", "状态"])
        self.recent_activity_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.recent_activity_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        recent_activity_layout.addWidget(self.recent_activity_table)
        dashboard_layout.addWidget(recent_activity_frame)
        
        self.tabs.addTab(dashboard_tab, "数据概览")
        
    def create_analysis_tab(self):
        """创建数据分析标签页"""
        analysis_tab = QWidget()
        analysis_layout = QVBoxLayout(analysis_tab)
        
        # 创建标题
        title_label = QLabel('数据分析')
        title_font = QFont('Arial', 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        analysis_layout.addWidget(title_label)
        
        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        analysis_layout.addWidget(line)
        
        # 创建分析控制区域
        control_frame = QGroupBox("分析设置")
        control_layout = QVBoxLayout(control_frame)
        
        # 分析类型选择
        analysis_type_layout = QHBoxLayout()
        analysis_type_label = QLabel("分析类型:")
        self.analysis_type_combo = QComboBox()
        self.analysis_type_combo.addItems(["粉丝分析", "互动分析", "内容分析", "竞争分析"])
        analysis_type_layout.addWidget(analysis_type_label)
        analysis_type_layout.addWidget(self.analysis_type_combo)
        analysis_type_layout.addStretch()
        
        # 平台选择
        platform_layout = QHBoxLayout()
        platform_label = QLabel("社交媒体平台:")
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(["综合平台", "微博", "微信", "抖音", "小红书", "B站"])
        platform_layout.addWidget(platform_label)
        platform_layout.addWidget(self.platform_combo)
        platform_layout.addStretch()
        
        # 日期范围选择
        date_layout = QHBoxLayout()
        date_label = QLabel("日期范围:")
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        date_range_label = QLabel("至")
        
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(date_range_label)
        date_layout.addWidget(self.end_date)
        date_layout.addStretch()
        
        # 数据来源选择
        data_source_layout = QHBoxLayout()
        data_source_label = QLabel("数据来源:")
        self.data_source_combo = QComboBox()
        self.data_source_combo.addItems(["示例数据", "导入数据"])
        self.data_source_combo.currentIndexChanged.connect(self.update_data_source_options)
        data_source_layout.addWidget(data_source_label)
        data_source_layout.addWidget(self.data_source_combo)
        
        # 数据文件选择
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("请选择数据文件")
        self.file_path_input.setEnabled(False)
        
        self.browse_button = QPushButton("浏览...")
        self.browse_button.setEnabled(False)
        self.browse_button.clicked.connect(self.browse_file)
        
        data_source_layout.addWidget(self.file_path_input)
        data_source_layout.addWidget(self.browse_button)
        
        # 分析按钮
        analyze_button = QPushButton("开始分析")
        analyze_button.setMinimumHeight(40)
        analyze_button.clicked.connect(self.controller.run_analysis)
        
        # 添加所有控制项到布局
        control_layout.addLayout(analysis_type_layout)
        control_layout.addLayout(platform_layout)
        control_layout.addLayout(date_layout)
        control_layout.addLayout(data_source_layout)
        control_layout.addWidget(analyze_button)
        
        analysis_layout.addWidget(control_frame)
        
        # 创建分析结果区域
        results_frame = QGroupBox("分析结果")
        results_layout = QVBoxLayout(results_frame)
        
        # 创建结果标签页
        self.result_tabs = QTabWidget()
        
        # 添加结果标签页
        self.overview_tab = QWidget()
        self.overview_layout = QVBoxLayout(self.overview_tab)
        self.overview_text = QTextEdit()
        self.overview_text.setReadOnly(True)
        self.overview_layout.addWidget(self.overview_text)
        self.result_tabs.addTab(self.overview_tab, "分析概述")
        
        self.charts_tab = QWidget()
        self.charts_layout = QVBoxLayout(self.charts_tab)
        
        # 创建图表显示区域
        self.chart_scroll_area = QScrollArea()
        self.chart_widget = QWidget()
        self.chart_layout = QVBoxLayout(self.chart_widget)
        self.chart_scroll_area.setWidget(self.chart_widget)
        self.chart_scroll_area.setWidgetResizable(True)
        
        # 添加图表说明
        chart_info_label = QLabel("图表分析区域 - 分析完成后将显示可视化图表")
        chart_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_info_label.setStyleSheet("color: #7f8c8d; font-style: italic; padding: 20px;")
        self.chart_layout.addWidget(chart_info_label)
        
        self.charts_layout.addWidget(self.chart_scroll_area)
        self.result_tabs.addTab(self.charts_tab, "图表分析")
        
        self.details_tab = QWidget()
        self.details_layout = QVBoxLayout(self.details_tab)
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_layout.addWidget(self.details_text)
        self.result_tabs.addTab(self.details_tab, "详细数据")
        
        results_layout.addWidget(self.result_tabs)
        
        # 添加进度条
        self.analysis_progress = QProgressBar()
        self.analysis_progress.setRange(0, 100)
        self.analysis_progress.setValue(0)
        results_layout.addWidget(self.analysis_progress)
        
        analysis_layout.addWidget(results_frame)
        
        self.tabs.addTab(analysis_tab, "数据分析")
        
    def create_marketing_tab(self):
        """创建营销方案标签页"""
        marketing_tab = QWidget()
        marketing_layout = QVBoxLayout(marketing_tab)
        
        # 创建标题
        title_label = QLabel('营销方案')
        title_font = QFont('Arial', 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        marketing_layout.addWidget(title_label)
        
        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        marketing_layout.addWidget(line)
        
        # 创建方案列表和内容区域
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧方案列表
        plans_frame = QGroupBox("我的营销方案")
        plans_layout = QVBoxLayout(plans_frame)
        
        self.plans_list = QListWidget()
        self.plans_list.itemClicked.connect(self.load_marketing_plan)
        plans_layout.addWidget(self.plans_list)
        
        # 方案操作按钮
        buttons_layout = QHBoxLayout()
        
        self.new_plan_button = QPushButton("新建方案")
        self.new_plan_button.clicked.connect(lambda: self.create_plan_signal.emit())
        buttons_layout.addWidget(self.new_plan_button)
        
        self.delete_plan_button = QPushButton("删除方案")
        self.delete_plan_button.clicked.connect(lambda: self.delete_plan_signal.emit())
        buttons_layout.addWidget(self.delete_plan_button)
        
        plans_layout.addLayout(buttons_layout)
        
        splitter.addWidget(plans_frame)
        
        # 右侧方案内容
        plan_content_frame = QGroupBox("方案详情")
        plan_content_layout = QVBoxLayout(plan_content_frame)
        
        self.plan_title = QLabel("营销方案标题")
        title_font = QFont('Arial', 16, QFont.Weight.Bold)
        self.plan_title.setFont(title_font)
        plan_content_layout.addWidget(self.plan_title)
        
        self.plan_date = QLabel("创建日期:")
        plan_content_layout.addWidget(self.plan_date)
        
        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        plan_content_layout.addWidget(line)
        
        self.plan_content = QTextEdit()
        self.plan_content.setReadOnly(True)
        plan_content_layout.addWidget(self.plan_content)
        
        # 方案操作按钮
        action_buttons_layout = QHBoxLayout()
        
        self.export_plan_button = QPushButton("导出方案")
        self.export_plan_button.clicked.connect(lambda: self.export_plan_signal.emit())
        action_buttons_layout.addWidget(self.export_plan_button)
        
        self.share_plan_button = QPushButton("分享方案")
        self.share_plan_button.clicked.connect(lambda: self.share_plan_signal.emit())
        action_buttons_layout.addWidget(self.share_plan_button)
        
        plan_content_layout.addLayout(action_buttons_layout)
        
        splitter.addWidget(plan_content_frame)
        
        # 设置分隔器初始大小
        splitter.setSizes([300, 700])
        
        marketing_layout.addWidget(splitter)
        
        self.tabs.addTab(marketing_tab, "营销方案")
        
    def create_trends_tab(self):
        """创建趋势分析标签页"""
        trends_tab = QWidget()
        trends_layout = QVBoxLayout(trends_tab)
        
        # 创建标题
        title_label = QLabel('趋势分析')
        title_font = QFont('Arial', 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        trends_layout.addWidget(title_label)
        
        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        trends_layout.addWidget(line)
        
        # 创建趋势分析控制区域
        control_frame = QGroupBox("趋势分析设置")
        control_layout = QVBoxLayout(control_frame)
        
        # 预测类型选择
        prediction_type_layout = QHBoxLayout()
        prediction_type_label = QLabel("预测类型:")
        self.prediction_type_combo = QComboBox()
        self.prediction_type_combo.addItems(["内容趋势", "用户行为", "市场趋势", "竞争对手"])
        prediction_type_layout.addWidget(prediction_type_label)
        prediction_type_layout.addWidget(self.prediction_type_combo)
        prediction_type_layout.addStretch()
        
        # 时间范围选择
        time_range_layout = QHBoxLayout()
        time_range_label = QLabel("预测时间范围:")
        self.time_range_combo = QComboBox()
        self.time_range_combo.addItems(["1个月", "3个月", "6个月", "1年"])
        time_range_layout.addWidget(time_range_label)
        time_range_layout.addWidget(self.time_range_combo)
        time_range_layout.addStretch()
        
        # 平台选择
        platform_layout = QHBoxLayout()
        platform_label = QLabel("社交媒体平台:")
        self.trend_platform_combo = QComboBox()
        self.trend_platform_combo.addItems(["综合平台", "微博", "微信", "抖音", "小红书", "B站"])
        platform_layout.addWidget(platform_label)
        platform_layout.addWidget(self.trend_platform_combo)
        platform_layout.addStretch()
        
        # 分析按钮
        predict_button = QPushButton("开始预测")
        predict_button.setMinimumHeight(40)
        predict_button.clicked.connect(self.controller.predict_trends)
        
        # 添加所有控制项到布局
        control_layout.addLayout(prediction_type_layout)
        control_layout.addLayout(time_range_layout)
        control_layout.addLayout(platform_layout)
        control_layout.addWidget(predict_button)
        
        trends_layout.addWidget(control_frame)
        
        # 创建趋势预测结果区域
        results_frame = QGroupBox("趋势预测结果")
        results_layout = QVBoxLayout(results_frame)
        
        self.trend_results = QTextEdit()
        self.trend_results.setReadOnly(True)
        results_layout.addWidget(self.trend_results)
        
        trends_layout.addWidget(results_frame)
        
        self.tabs.addTab(trends_tab, "趋势分析")
        
    def create_content_tab(self):
        """创建内容优化标签页"""
        content_tab = QWidget()
        content_layout = QVBoxLayout(content_tab)
        
        # 创建标题
        title_label = QLabel('内容优化')
        title_font = QFont('Arial', 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        content_layout.addWidget(title_label)
        
        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        content_layout.addWidget(line)
        
        # 创建内容优化控制区域
        control_frame = QGroupBox("内容优化设置")
        control_layout = QVBoxLayout(control_frame)
        
        # 平台选择
        platform_layout = QHBoxLayout()
        platform_label = QLabel("发布平台:")
        self.content_platform_combo = QComboBox()
        self.content_platform_combo.addItems(["微博", "微信", "抖音", "小红书", "B站"])
        platform_layout.addWidget(platform_label)
        platform_layout.addWidget(self.content_platform_combo)
        platform_layout.addStretch()
        
        # 内容类型选择
        content_type_layout = QHBoxLayout()
        content_type_label = QLabel("内容类型:")
        self.content_type_combo = QComboBox()
        self.content_type_combo.addItems(["文章", "视频", "图片", "直播", "活动"])
        content_type_layout.addWidget(content_type_label)
        content_type_layout.addWidget(self.content_type_combo)
        content_type_layout.addStretch()
        
        # 原始内容输入
        content_label = QLabel("原始内容:")
        self.original_content = QTextEdit()
        self.original_content.setPlaceholderText("请输入要优化的内容...")
        self.original_content.setMinimumHeight(100)
        
        # 优化按钮
        optimize_button = QPushButton("优化内容")
        optimize_button.setMinimumHeight(40)
        optimize_button.clicked.connect(self.controller.optimize_content)
        
        # 添加所有控制项到布局
        control_layout.addLayout(platform_layout)
        control_layout.addLayout(content_type_layout)
        control_layout.addWidget(content_label)
        control_layout.addWidget(self.original_content)
        control_layout.addWidget(optimize_button)
        
        content_layout.addWidget(control_frame)
        
        # 创建优化结果区域
        results_frame = QGroupBox("优化结果")
        results_layout = QVBoxLayout(results_frame)
        
        # 创建结果标签页
        self.content_result_tabs = QTabWidget()
        
        # 添加结果标签页
        self.optimized_tab = QWidget()
        self.optimized_layout = QVBoxLayout(self.optimized_tab)
        self.optimized_content = QTextEdit()
        self.optimized_content.setReadOnly(True)
        self.optimized_layout.addWidget(self.optimized_content)
        self.content_result_tabs.addTab(self.optimized_tab, "优化内容")
        
        self.suggestions_tab = QWidget()
        self.suggestions_layout = QVBoxLayout(self.suggestions_tab)
        self.suggestions_content = QTextEdit()
        self.suggestions_content.setReadOnly(True)
        self.suggestions_layout.addWidget(self.suggestions_content)
        self.content_result_tabs.addTab(self.suggestions_tab, "优化建议")
        
        results_layout.addWidget(self.content_result_tabs)
        
        content_layout.addWidget(results_frame)
        
        self.tabs.addTab(content_tab, "内容优化")
        
    def create_reports_tab(self):
        """创建报告导出标签页"""
        reports_tab = QWidget()
        reports_layout = QVBoxLayout(reports_tab)
        
        # 创建标题
        title_label = QLabel('报告导出')
        title_font = QFont('Arial', 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        reports_layout.addWidget(title_label)
        
        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        reports_layout.addWidget(line)
        
        # 创建报告类型选择区域
        report_type_frame = QGroupBox("报告类型")
        report_type_layout = QVBoxLayout(report_type_frame)
        
        # 报告类型单选按钮
        self.report_type_layout = QHBoxLayout()
        
        self.analysis_report_radio = QPushButton("数据分析报告")
        self.analysis_report_radio.setCheckable(True)
        self.analysis_report_radio.setChecked(True)
        self.report_type_layout.addWidget(self.analysis_report_radio)
        
        self.marketing_report_radio = QPushButton("营销方案报告")
        self.marketing_report_radio.setCheckable(True)
        self.report_type_layout.addWidget(self.marketing_report_radio)
        
        self.combined_report_radio = QPushButton("综合报告")
        self.combined_report_radio.setCheckable(True)
        self.report_type_layout.addWidget(self.combined_report_radio)
        
        report_type_layout.addLayout(self.report_type_layout)
        
        reports_layout.addWidget(report_type_frame)
        
        # 创建报告选项区域
        report_options_frame = QGroupBox("报告选项")
        report_options_layout = QVBoxLayout(report_options_frame)
        
        # 报告格式选择
        format_layout = QHBoxLayout()
        format_label = QLabel("报告格式:")
        self.report_format_combo = QComboBox()
        self.report_format_combo.addItems(["PDF", "Word", "Excel", "PowerPoint", "HTML"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.report_format_combo)
        format_layout.addStretch()
        
        # 报告内容选择
        content_layout = QHBoxLayout()
        content_label = QLabel("报告内容:")
        
        self.include_charts_check = QPushButton("包含图表")
        self.include_charts_check.setCheckable(True)
        self.include_charts_check.setChecked(True)
        
        self.include_tables_check = QPushButton("包含表格")
        self.include_tables_check.setCheckable(True)
        self.include_tables_check.setChecked(True)
        
        self.include_recommendations_check = QPushButton("包含建议")
        self.include_recommendations_check.setCheckable(True)
        self.include_recommendations_check.setChecked(True)
        
        content_layout.addWidget(content_label)
        content_layout.addWidget(self.include_charts_check)
        content_layout.addWidget(self.include_tables_check)
        content_layout.addWidget(self.include_recommendations_check)
        
        # 报告标题
        title_layout = QHBoxLayout()
        title_label = QLabel("报告标题:")
        self.report_title = QLineEdit()
        self.report_title.setText("社交媒体营销分析报告")
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.report_title)
        
        # 添加所有选项到布局
        report_options_layout.addLayout(format_layout)
        report_options_layout.addLayout(content_layout)
        report_options_layout.addLayout(title_layout)
        
        reports_layout.addWidget(report_options_frame)
        
        # 创建报告预览区域
        preview_frame = QGroupBox("报告预览")
        preview_layout = QVBoxLayout(preview_frame)
        
        self.report_preview = QTextEdit()
        self.report_preview.setReadOnly(True)
        self.report_preview.setPlaceholderText("报告预览将显示在这里...")
        preview_layout.addWidget(self.report_preview)
        
        reports_layout.addWidget(preview_frame)
        
        # 创建导出按钮
        export_button = QPushButton("导出报告")
        export_button.setMinimumHeight(40)
        export_button.clicked.connect(self.controller.export_report)
        reports_layout.addWidget(export_button)
        
        self.tabs.addTab(reports_tab, "报告导出")
        
    def create_settings_tab(self):
        """创建设置标签页（防止重复添加）"""
        if hasattr(self, '_settings_tab_added') and self._settings_tab_added:
            return
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        
        # 创建标题
        title_label = QLabel('系统设置')
        title_font = QFont('Arial', 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        settings_layout.addWidget(title_label)
        
        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        settings_layout.addWidget(line)
        
        # 创建API设置区域
        api_frame = QGroupBox("AI API 设置")
        api_layout = QVBoxLayout(api_frame)
        
        # API密钥
        api_key_layout = QHBoxLayout()
        api_key_label = QLabel("Deepseek API 密钥:")
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setText("sk-dfc4e38245414faf8290bb291db1a35e")  # 设置提供的API密钥
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_input)
        
        # API基础URL
        api_url_layout = QHBoxLayout()
        api_url_label = QLabel("API 基础URL:")
        self.api_url_input = QLineEdit()
        self.api_url_input.setText("https://api.deepseek.com/v1")
        api_url_layout.addWidget(api_url_label)
        api_url_layout.addWidget(self.api_url_input)
        
        # 测试API按钮
        test_api_button = QPushButton("测试API连接")
        test_api_button.setMinimumHeight(40)
        test_api_button.clicked.connect(self.controller.test_api_connection)
        
        # 添加所有API设置到布局
        api_layout.addLayout(api_key_layout)
        api_layout.addLayout(api_url_layout)
        api_layout.addWidget(test_api_button)
        
        settings_layout.addWidget(api_frame)
        
        # 创建用户设置区域
        user_frame = QGroupBox("用户设置")
        user_layout = QVBoxLayout(user_frame)
        
        # 用户名
        username_layout = QHBoxLayout()
        username_label = QLabel("用户名:")
        self.username_display = QLineEdit()
        self.username_display.setText(self.current_user[1])
        self.username_display.setReadOnly(True)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_display)
        
        # 邮箱
        email_layout = QHBoxLayout()
        email_label = QLabel("邮箱:")
        self.email_display = QLineEdit()
        self.email_display.setText(self.current_user[2])
        self.email_display.setReadOnly(True)
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_display)
        
        # 修改密码按钮
        change_password_button = QPushButton("修改密码")
        change_password_button.clicked.connect(lambda: self.change_password_signal.emit())
        settings_layout.addWidget(change_password_button)
        
        # 添加所有用户设置到布局
        user_layout.addLayout(username_layout)
        user_layout.addLayout(email_layout)
        user_layout.addWidget(change_password_button)
        
        settings_layout.addWidget(user_frame)
        
        # 创建保存设置按钮
        save_settings_button = QPushButton("保存设置")
        save_settings_button.clicked.connect(lambda: self.save_settings_signal.emit())
        settings_layout.addWidget(save_settings_button)
        
        self.tabs.addTab(settings_tab, "系统设置")
        self._settings_tab_added = True
        
    def create_stat_card(self, title, value, layout, color):
        """创建统计卡片"""
        card = QWidget()
        card.setStyleSheet(f"background-color: {color}; border-radius: 8px; padding: 15px; color: white;")
        
        card_layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        value_label = QLabel(value)
        value_font = QFont('Arial', 24, QFont.Weight.Bold)
        value_label.setFont(value_font)
        value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        card_layout.addStretch()
        
        layout.addWidget(card, 1)
        
    def create_chart(self):
        """创建图表画布"""
        fig, ax = plt.subplots(figsize=(5, 4))
        canvas = FigureCanvas(fig)
        return canvas
        
    def update_data_source_options(self, index):
        """更新数据来源选项"""
        if index == 1:  # 导入数据
            self.file_path_input.setEnabled(True)
            self.browse_button.setEnabled(True)
        else:  # 示例数据
            self.file_path_input.setEnabled(False)
            self.browse_button.setEnabled(False)
            self.file_path_input.clear()
            
    def browse_file(self):
        """浏览文件选择对话框"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择数据文件", "", "CSV文件 (*.csv);;Excel文件 (*.xlsx);;所有文件 (*)"
        )
        
        if file_path:
            self.file_path_input.setText(file_path)
            
    def load_marketing_plan(self, item):
        """加载营销方案"""
        plan_id = item.data(Qt.ItemDataRole.UserRole)
        self.controller.load_marketing_plan(plan_id)

    def show_help_dialog(self):
        """显示帮助弹窗（标题为'帮助'）"""
        help_text = (
            "本系统为社交媒体营销分析平台，集成AI分析、内容优化、趋势预测等功能。\n"
            "\n"
            "主要功能：\n"
            "- 数据导入与分析\n"
            "- 营销方案管理\n"
            "- 趋势预测与内容优化\n"
            "- 报告导出\n"
            "- 系统个性化设置\n"
            "\n"
            "如需详细操作说明，请查阅用户手册或联系开发者。"
        )
        QMessageBox.information(self, '帮助', help_text)

    def show_about_dialog(self):
        """显示关于弹窗，含开发者信息，年份自动更新"""
        current_year = datetime.datetime.now().year
        about_text = (
            "社交媒体营销分析系统\n"
            "版本：v1.0.0\n"
            "开发者：Gondryisme\n"
            "\n"
            "本系统基于Python 3.9 + PyQt6开发，集成AI分析能力。\n"
            "\n"
            f"© {current_year} Gondryisme 保留所有权利。"
        )
        QMessageBox.information(self, '关于', about_text)