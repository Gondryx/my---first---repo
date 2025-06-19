from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTextEdit, QComboBox, QDateEdit, QSpinBox, QGroupBox,
                             QTableWidget, QTableWidgetItem, QMessageBox, QFrame,
                             QLineEdit, QCheckBox, QListWidget, QSplitter, QTabWidget)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QFont
import json

class MarketingStrategyView(QWidget):
    """营销策略界面"""
    
    strategy_created_signal = pyqtSignal(dict)
    strategy_updated_signal = pyqtSignal(dict)
    strategy_deleted_signal = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.strategies = []
        self.current_strategy = None
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("营销策略管理")
        self.setMinimumSize(1200, 800)
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("营销策略管理")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧策略列表
        strategy_list_panel = self.create_strategy_list_panel()
        splitter.addWidget(strategy_list_panel)
        
        # 右侧策略编辑
        strategy_edit_panel = self.create_strategy_edit_panel()
        splitter.addWidget(strategy_edit_panel)
        
        # 设置分割器比例
        splitter.setSizes([300, 900])
        main_layout.addWidget(splitter)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("保存策略")
        self.save_btn.clicked.connect(self.save_strategy)
        
        self.delete_btn = QPushButton("删除策略")
        self.delete_btn.clicked.connect(self.delete_strategy)
        
        self.export_btn = QPushButton("导出策略")
        self.export_btn.clicked.connect(self.export_strategy)
        
        self.back_btn = QPushButton("返回主界面")
        self.back_btn.clicked.connect(self.go_back)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.back_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def create_strategy_list_panel(self):
        """创建策略列表面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setMaximumWidth(300)
        
        layout = QVBoxLayout()
        
        # 策略列表标题
        title_label = QLabel("策略列表")
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # 新建策略按钮
        new_strategy_btn = QPushButton("新建策略")
        new_strategy_btn.clicked.connect(self.create_new_strategy)
        layout.addWidget(new_strategy_btn)
        
        # 策略列表
        self.strategy_list = QListWidget()
        self.strategy_list.itemClicked.connect(self.load_strategy)
        layout.addWidget(self.strategy_list)
        
        panel.setLayout(layout)
        return panel
        
    def create_strategy_edit_panel(self):
        """创建策略编辑面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout()
        
        # 基本信息组
        basic_group = QGroupBox("基本信息")
        basic_layout = QVBoxLayout()
        
        # 策略名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("策略名称:"))
        self.strategy_name = QLineEdit()
        name_layout.addWidget(self.strategy_name)
        basic_layout.addLayout(name_layout)
        
        # 策略类型
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("策略类型:"))
        self.strategy_type = QComboBox()
        self.strategy_type.addItems(["内容营销", "社交媒体营销", "影响者营销", "付费广告", "活动营销"])
        type_layout.addWidget(self.strategy_type)
        basic_layout.addLayout(type_layout)
        
        # 目标平台
        platform_layout = QHBoxLayout()
        platform_layout.addWidget(QLabel("目标平台:"))
        self.target_platform = QComboBox()
        self.target_platform.addItems(["微博", "微信", "抖音", "小红书", "B站", "多平台"])
        platform_layout.addWidget(self.target_platform)
        basic_layout.addLayout(platform_layout)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # 时间设置组
        time_group = QGroupBox("时间设置")
        time_layout = QVBoxLayout()
        
        # 开始日期
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("开始日期:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate())
        start_layout.addWidget(self.start_date)
        time_layout.addLayout(start_layout)
        
        # 结束日期
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("结束日期:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate().addMonths(1))
        end_layout.addWidget(self.end_date)
        time_layout.addLayout(end_layout)
        
        # 持续时间
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("持续时间(天):"))
        self.duration = QSpinBox()
        self.duration.setRange(1, 365)
        self.duration.setValue(30)
        duration_layout.addWidget(self.duration)
        time_layout.addLayout(duration_layout)
        
        time_group.setLayout(time_layout)
        layout.addWidget(time_group)
        
        # 策略内容组
        content_group = QGroupBox("策略内容")
        content_layout = QVBoxLayout()
        
        # 目标受众
        audience_layout = QHBoxLayout()
        audience_layout.addWidget(QLabel("目标受众:"))
        self.target_audience = QLineEdit()
        self.target_audience.setPlaceholderText("例如：18-35岁年轻女性")
        audience_layout.addWidget(self.target_audience)
        content_layout.addLayout(audience_layout)
        
        # 核心信息
        content_layout.addWidget(QLabel("核心信息:"))
        self.core_message = QTextEdit()
        self.core_message.setMaximumHeight(80)
        content_layout.addWidget(self.core_message)
        
        # 策略描述
        content_layout.addWidget(QLabel("策略描述:"))
        self.strategy_description = QTextEdit()
        content_layout.addWidget(self.strategy_description)
        
        content_group.setLayout(content_layout)
        layout.addWidget(content_group)
        
        # 执行计划组
        plan_group = QGroupBox("执行计划")
        plan_layout = QVBoxLayout()
        
        # 关键行动
        plan_layout.addWidget(QLabel("关键行动:"))
        self.key_actions = QTextEdit()
        self.key_actions.setMaximumHeight(100)
        plan_layout.addWidget(self.key_actions)
        
        # 预算设置
        budget_layout = QHBoxLayout()
        budget_layout.addWidget(QLabel("预算(元):"))
        self.budget = QSpinBox()
        self.budget.setRange(0, 1000000)
        self.budget.setValue(10000)
        budget_layout.addWidget(self.budget)
        plan_layout.addLayout(budget_layout)
        
        # 成功指标
        plan_layout.addWidget(QLabel("成功指标:"))
        self.success_metrics = QTextEdit()
        self.success_metrics.setMaximumHeight(80)
        plan_layout.addWidget(self.success_metrics)
        
        plan_group.setLayout(plan_layout)
        layout.addWidget(plan_group)
        
        panel.setLayout(layout)
        return panel
        
    def create_new_strategy(self):
        """创建新策略"""
        self.current_strategy = None
        self.clear_form()
        
        # 添加到列表
        strategy_name = f"新策略 {len(self.strategies) + 1}"
        self.strategy_list.addItem(strategy_name)
        self.strategy_name.setText(strategy_name)
        
    def load_strategy(self, item):
        """加载策略"""
        strategy_name = item.text()
        # 这里应该从数据库或文件加载策略数据
        # 简化版本，创建示例数据
        self.current_strategy = {
            'name': strategy_name,
            'type': '内容营销',
            'platform': '微博',
            'start_date': QDate.currentDate(),
            'end_date': QDate.currentDate().addMonths(1),
            'duration': 30,
            'audience': '18-35岁年轻女性',
            'core_message': '品牌核心价值传递',
            'description': '通过内容营销提升品牌知名度',
            'actions': '1. 内容创作\n2. 发布计划\n3. 互动管理',
            'budget': 10000,
            'metrics': '粉丝增长、互动率、转化率'
        }
        
        self.populate_form()
        
    def populate_form(self):
        """填充表单"""
        if not self.current_strategy:
            return
            
        self.strategy_name.setText(self.current_strategy['name'])
        self.strategy_type.setCurrentText(self.current_strategy['type'])
        self.target_platform.setCurrentText(self.current_strategy['platform'])
        self.start_date.setDate(self.current_strategy['start_date'])
        self.end_date.setDate(self.current_strategy['end_date'])
        self.duration.setValue(self.current_strategy['duration'])
        self.target_audience.setText(self.current_strategy['audience'])
        self.core_message.setPlainText(self.current_strategy['core_message'])
        self.strategy_description.setPlainText(self.current_strategy['description'])
        self.key_actions.setPlainText(self.current_strategy['actions'])
        self.budget.setValue(self.current_strategy['budget'])
        self.success_metrics.setPlainText(self.current_strategy['metrics'])
        
    def clear_form(self):
        """清空表单"""
        self.strategy_name.clear()
        self.strategy_type.setCurrentIndex(0)
        self.target_platform.setCurrentIndex(0)
        self.start_date.setDate(QDate.currentDate())
        self.end_date.setDate(QDate.currentDate().addMonths(1))
        self.duration.setValue(30)
        self.target_audience.clear()
        self.core_message.clear()
        self.strategy_description.clear()
        self.key_actions.clear()
        self.budget.setValue(10000)
        self.success_metrics.clear()
        
    def save_strategy(self):
        """保存策略"""
        if not self.strategy_name.text():
            QMessageBox.warning(self, "警告", "请输入策略名称")
            return
            
        strategy_data = {
            'name': self.strategy_name.text(),
            'type': self.strategy_type.currentText(),
            'platform': self.target_platform.currentText(),
            'start_date': self.start_date.date().toString("yyyy-MM-dd"),
            'end_date': self.end_date.date().toString("yyyy-MM-dd"),
            'duration': self.duration.value(),
            'audience': self.target_audience.text(),
            'core_message': self.core_message.toPlainText(),
            'description': self.strategy_description.toPlainText(),
            'actions': self.key_actions.toPlainText(),
            'budget': self.budget.value(),
            'metrics': self.success_metrics.toPlainText()
        }
        
        if self.current_strategy:
            self.strategy_updated_signal.emit(strategy_data)
        else:
            self.strategy_created_signal.emit(strategy_data)
            
        QMessageBox.information(self, "成功", "策略保存成功")
        
    def delete_strategy(self):
        """删除策略"""
        if not self.current_strategy:
            QMessageBox.warning(self, "警告", "请先选择要删除的策略")
            return
            
        reply = QMessageBox.question(self, "确认删除", 
                                   "确定要删除这个策略吗？",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # 这里应该删除数据库中的策略
            self.strategy_deleted_signal.emit(1)  # 假设策略ID为1
            self.strategy_list.takeItem(self.strategy_list.currentRow())
            self.clear_form()
            QMessageBox.information(self, "成功", "策略删除成功")
            
    def export_strategy(self):
        """导出策略"""
        if not self.current_strategy:
            QMessageBox.warning(self, "警告", "请先选择要导出的策略")
            return
            
        try:
            from PyQt6.QtWidgets import QFileDialog
            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出策略", f"{self.strategy_name.text()}.json", "JSON文件 (*.json)"
            )
            
            if file_path:
                strategy_data = {
                    'name': self.strategy_name.text(),
                    'type': self.strategy_type.currentText(),
                    'platform': self.target_platform.currentText(),
                    'start_date': self.start_date.date().toString("yyyy-MM-dd"),
                    'end_date': self.end_date.date().toString("yyyy-MM-dd"),
                    'duration': self.duration.value(),
                    'audience': self.target_audience.text(),
                    'core_message': self.core_message.toPlainText(),
                    'description': self.strategy_description.toPlainText(),
                    'actions': self.key_actions.toPlainText(),
                    'budget': self.budget.value(),
                    'metrics': self.success_metrics.toPlainText()
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(strategy_data, f, ensure_ascii=False, indent=2)
                    
                QMessageBox.information(self, "成功", f"策略已导出到: {file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
            
    def go_back(self):
        """返回主界面"""
        if hasattr(self.parent(), 'show_main_view'):
            self.parent().show_main_view() 