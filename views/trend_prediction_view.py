from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTextEdit, QComboBox, QDateEdit, QSpinBox, QGroupBox,
                             QTableWidget, QTableWidgetItem, QMessageBox, QFrame,
                             QLineEdit, QCheckBox, QListWidget, QSplitter, QProgressBar, QTabWidget, QProgressDialog)
from PyQt6.QtCore import Qt, QDate, pyqtSignal, QTimer, QThread
from PyQt6.QtGui import QFont
import json
import random
import traceback

try:
    from models.deepseek_api import deepseek_api
except ImportError:
    deepseek_api = None

class TrendPredictionWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    def __init__(self, prompt, timeout=20):
        super().__init__()
        self.prompt = prompt
        self.timeout = timeout
    def run(self):
        try:
            if deepseek_api is None:
                raise Exception("未找到DeepSeek API模块")
            result = deepseek_api.predict_trends(self.prompt)
            self.finished.emit(result)
        except Exception as e:
            tb = traceback.format_exc()
            self.error.emit(f"{str(e)}\n{tb}")

class TrendPredictionView(QWidget):
    """趋势预测界面"""
    
    prediction_started_signal = pyqtSignal(dict)
    prediction_completed_signal = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.predictions = []
        self.current_prediction = None
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("趋势预测分析")
        self.setMinimumSize(1200, 800)
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("趋势预测分析")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧预测设置
        prediction_settings_panel = self.create_prediction_settings_panel()
        splitter.addWidget(prediction_settings_panel)
        
        # 右侧预测结果
        prediction_results_panel = self.create_prediction_results_panel()
        splitter.addWidget(prediction_results_panel)
        
        # 设置分割器比例
        splitter.setSizes([400, 800])
        main_layout.addWidget(splitter)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.start_prediction_btn = QPushButton("开始预测")
        self.start_prediction_btn.clicked.connect(self.start_prediction)
        
        self.save_prediction_btn = QPushButton("保存预测")
        self.save_prediction_btn.clicked.connect(self.save_prediction)
        
        self.export_prediction_btn = QPushButton("导出预测")
        self.export_prediction_btn.clicked.connect(self.export_prediction)
        
        self.back_btn = QPushButton("返回主界面")
        self.back_btn.clicked.connect(self.go_back)
        
        button_layout.addWidget(self.start_prediction_btn)
        button_layout.addWidget(self.save_prediction_btn)
        button_layout.addWidget(self.export_prediction_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.back_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def create_prediction_settings_panel(self):
        """创建预测设置面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setMaximumWidth(400)
        
        layout = QVBoxLayout()
        
        # 预测类型组
        prediction_type_group = QGroupBox("预测类型")
        prediction_type_layout = QVBoxLayout()
        
        self.prediction_type_combo = QComboBox()
        self.prediction_type_combo.addItems([
            "内容趋势预测",
            "用户行为预测", 
            "市场趋势预测",
            "竞争对手分析",
            "平台发展趋势",
            "热点话题预测"
        ])
        prediction_type_layout.addWidget(self.prediction_type_combo)
        
        prediction_type_group.setLayout(prediction_type_layout)
        layout.addWidget(prediction_type_group)
        
        # 平台选择组
        platform_group = QGroupBox("目标平台")
        platform_layout = QVBoxLayout()
        
        self.platform_combo = QComboBox()
        self.platform_combo.addItems([
            "微博", "微信", "抖音", "小红书", "B站", "知乎", "多平台"
        ])
        platform_layout.addWidget(self.platform_combo)
        
        platform_group.setLayout(platform_layout)
        layout.addWidget(platform_group)
        
        # 时间范围组
        time_range_group = QGroupBox("预测时间范围")
        time_layout = QVBoxLayout()
        
        # 预测周期
        period_layout = QHBoxLayout()
        period_layout.addWidget(QLabel("预测周期:"))
        self.prediction_period = QComboBox()
        self.prediction_period.addItems(["1周", "1个月", "3个月", "6个月", "1年"])
        period_layout.addWidget(self.prediction_period)
        time_layout.addLayout(period_layout)
        
        # 历史数据范围
        history_layout = QHBoxLayout()
        history_layout.addWidget(QLabel("历史数据:"))
        self.history_period = QComboBox()
        self.history_period.addItems(["1个月", "3个月", "6个月", "1年", "2年"])
        history_layout.addWidget(self.history_period)
        time_layout.addLayout(history_layout)
        
        time_range_group.setLayout(time_layout)
        layout.addWidget(time_range_group)
        
        # 预测参数组
        parameters_group = QGroupBox("预测参数")
        params_layout = QVBoxLayout()
        
        # 置信度
        confidence_layout = QHBoxLayout()
        confidence_layout.addWidget(QLabel("置信度(%):"))
        self.confidence_level = QSpinBox()
        self.confidence_level.setRange(50, 99)
        self.confidence_level.setValue(85)
        confidence_layout.addWidget(self.confidence_level)
        params_layout.addLayout(confidence_layout)
        
        # 数据点数量
        data_points_layout = QHBoxLayout()
        data_points_layout.addWidget(QLabel("数据点:"))
        self.data_points = QSpinBox()
        self.data_points.setRange(10, 1000)
        self.data_points.setValue(100)
        data_points_layout.addWidget(self.data_points)
        params_layout.addLayout(data_points_layout)
        
        parameters_group.setLayout(params_layout)
        layout.addWidget(parameters_group)
        
        # 关键词组
        keywords_group = QGroupBox("关键词设置")
        keywords_layout = QVBoxLayout()
        
        self.keywords_input = QTextEdit()
        self.keywords_input.setMaximumHeight(80)
        self.keywords_input.setPlaceholderText("输入相关关键词，每行一个")
        keywords_layout.addWidget(self.keywords_input)
        
        keywords_group.setLayout(keywords_layout)
        layout.addWidget(keywords_group)
        
        # 高级选项组
        advanced_group = QGroupBox("高级选项")
        advanced_layout = QVBoxLayout()
        
        self.include_sentiment = QCheckBox("包含情感分析")
        self.include_sentiment.setChecked(True)
        advanced_layout.addWidget(self.include_sentiment)
        
        self.include_competitor = QCheckBox("包含竞争对手分析")
        self.include_competitor.setChecked(True)
        advanced_layout.addWidget(self.include_competitor)
        
        self.include_seasonal = QCheckBox("包含季节性分析")
        self.include_seasonal.setChecked(False)
        advanced_layout.addWidget(self.include_seasonal)
        
        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)
        
        panel.setLayout(layout)
        return panel
        
    def create_prediction_results_panel(self):
        """创建预测结果面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout()
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 预测概览标签页
        self.overview_tab = QWidget()
        overview_layout = QVBoxLayout(self.overview_tab)
        
        self.overview_text = QTextEdit()
        self.overview_text.setReadOnly(True)
        self.overview_text.setPlaceholderText("预测完成后将显示结果概览...")
        overview_layout.addWidget(self.overview_text)
        
        self.tab_widget.addTab(self.overview_tab, "预测概览")
        
        # 趋势图表标签页
        self.trends_tab = QWidget()
        trends_layout = QVBoxLayout(self.trends_tab)
        
        self.trends_text = QTextEdit()
        self.trends_text.setReadOnly(True)
        self.trends_text.setPlaceholderText("预测完成后将显示趋势图表...")
        trends_layout.addWidget(self.trends_text)
        
        self.tab_widget.addTab(self.trends_tab, "趋势图表")
        
        # 详细数据标签页
        self.details_tab = QWidget()
        details_layout = QVBoxLayout(self.details_tab)
        
        self.details_table = QTableWidget()
        self.details_table.setColumnCount(5)
        self.details_table.setHorizontalHeaderLabels(["时间", "预测值", "置信区间", "趋势", "说明"])
        details_layout.addWidget(self.details_table)
        
        self.tab_widget.addTab(self.details_tab, "详细数据")
        
        # 建议标签页
        self.recommendations_tab = QWidget()
        recommendations_layout = QVBoxLayout(self.recommendations_tab)
        
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setReadOnly(True)
        self.recommendations_text.setPlaceholderText("预测完成后将显示行动建议...")
        recommendations_layout.addWidget(self.recommendations_text)
        
        self.tab_widget.addTab(self.recommendations_tab, "行动建议")
        
        layout.addWidget(self.tab_widget)
        
        panel.setLayout(layout)
        return panel
        
    def start_prediction(self):
        """开始预测"""
        prediction_params = {
            'type': self.prediction_type_combo.currentText(),
            'platform': self.platform_combo.currentText(),
            'period': self.prediction_period.currentText(),
            'history': self.history_period.currentText(),
            'confidence': self.confidence_level.value(),
            'data_points': self.data_points.value(),
            'keywords': self.keywords_input.toPlainText().split('\n'),
            'include_sentiment': self.include_sentiment.isChecked(),
            'include_competitor': self.include_competitor.isChecked(),
            'include_seasonal': self.include_seasonal.isChecked()
        }
        prompt = f"""
预测类别: {prediction_params['type']}
目标平台: {prediction_params['platform']}
预测周期: {prediction_params['period']}
历史数据: {prediction_params['history']}
置信度: {prediction_params['confidence']}%
数据点: {prediction_params['data_points']}
关键词: {', '.join([k for k in prediction_params['keywords'] if k.strip()])}
包含情感分析: {'是' if prediction_params['include_sentiment'] else '否'}
包含竞争对手分析: {'是' if prediction_params['include_competitor'] else '否'}
包含季节性分析: {'是' if prediction_params['include_seasonal'] else '否'}
"""
        self.start_prediction_btn.setEnabled(False)
        # 显示QProgressDialog
        self.progress_dialog = QProgressDialog("正在进行趋势预测，请稍候...", "取消", 0, 100, self)
        self.progress_dialog.setWindowTitle("趋势预测进度")
        self.progress_dialog.setWindowModality(Qt.WindowModality.NonModal)
        self.progress_dialog.setValue(0)
        self.progress_dialog.canceled.connect(self.cancel_prediction)
        self.progress_dialog.show()
        self._prediction_canceled = False
        # 启动异步线程
        self.worker = TrendPredictionWorker(prompt, timeout=20)
        self.worker.finished.connect(self.on_prediction_finished)
        self.worker.error.connect(self.on_prediction_error)
        self.worker.start()
        # 启动进度条动画
        self.simulation_timer = QTimer()
        self.simulation_timer.timeout.connect(self.update_progress)
        self.simulation_timer.start(100)
        
    def update_progress(self):
        """更新进度条"""
        if hasattr(self, '_prediction_canceled') and self._prediction_canceled:
            self.simulation_timer.stop()
            if hasattr(self, 'progress_dialog'):
                self.progress_dialog.close()
            self.start_prediction_btn.setEnabled(True)
            return
        current_value = self.progress_dialog.value() if hasattr(self, 'progress_dialog') else 0
        if current_value < 100:
            if hasattr(self, 'progress_dialog'):
                self.progress_dialog.setValue(current_value + 5)
        else:
            self.simulation_timer.stop()
            if hasattr(self, 'progress_dialog'):
                self.progress_dialog.close()
            self.generate_prediction_results()
            
    def generate_prediction_results(self):
        """生成预测结果（模拟）"""
        prediction_type = self.prediction_type_combo.currentText()
        platform = self.platform_combo.currentText()
        
        # 生成模拟结果
        overview = f"""
预测类型: {prediction_type}
目标平台: {platform}
预测周期: {self.prediction_period.currentText()}
置信度: {self.confidence_level.value()}%

预测结果概览:
- 总体趋势: 上升趋势
- 关键时间点: 未来2-3周可能出现峰值
- 影响因素: 节假日、热点事件、用户行为变化
- 风险等级: 中等
        """
        
        trends = f"""
趋势分析图表:
1. 用户活跃度趋势 - 预计增长15-20%
2. 内容互动率趋势 - 预计增长8-12%
3. 话题热度趋势 - 预计增长25-30%
4. 竞争对手表现 - 相对稳定

图表数据已生成，包含时间序列分析和预测曲线。
        """
        
        # 生成详细数据表格
        self.details_table.setRowCount(10)
        for i in range(10):
            week = i + 1
            predicted_value = random.randint(80, 120)
            confidence_lower = predicted_value - random.randint(5, 15)
            confidence_upper = predicted_value + random.randint(5, 15)
            trend = random.choice(["上升", "下降", "稳定"])
            description = f"第{week}周预测数据"
            
            self.details_table.setItem(i, 0, QTableWidgetItem(f"第{week}周"))
            self.details_table.setItem(i, 1, QTableWidgetItem(str(predicted_value)))
            self.details_table.setItem(i, 2, QTableWidgetItem(f"{confidence_lower}-{confidence_upper}"))
            self.details_table.setItem(i, 3, QTableWidgetItem(trend))
            self.details_table.setItem(i, 4, QTableWidgetItem(description))
            
        recommendations = f"""
基于预测结果的行动建议:

1. 内容策略调整
   - 增加视频内容比例，预计视频内容互动率更高
   - 优化发布时间，建议在用户活跃高峰期发布
   - 加强话题标签使用，提高内容发现率

2. 用户互动优化
   - 增加回复频率，提高用户粘性
   - 开展互动活动，提升用户参与度
   - 优化内容质量，提高转发分享率

3. 竞争策略
   - 关注竞争对手动态，及时调整策略
   - 寻找差异化定位，避免同质化竞争
   - 加强品牌建设，提升用户认知度

4. 风险控制
   - 建立舆情监控机制
   - 准备应急预案
   - 定期评估预测准确性
        """
        
        # 更新界面
        self.overview_text.setPlainText(overview)
        self.trends_text.setPlainText(trends)
        self.recommendations_text.setPlainText(recommendations)
        
        # 切换到概览标签页
        self.tab_widget.setCurrentIndex(0)
        
        # 保存预测结果
        self.current_prediction = {
            'type': prediction_type,
            'platform': platform,
            'overview': overview,
            'trends': trends,
            'recommendations': recommendations,
            'timestamp': QDate.currentDate().toString("yyyy-MM-dd")
        }
        
        QMessageBox.information(self, "预测完成", "趋势预测分析已完成！")
        
    def save_prediction(self):
        """保存预测结果"""
        if not self.current_prediction:
            QMessageBox.warning(self, "警告", "没有可保存的预测结果")
            return
            
        try:
            # 这里应该保存到数据库
            self.predictions.append(self.current_prediction)
            QMessageBox.information(self, "成功", "预测结果已保存")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
            
    def export_prediction(self):
        """导出预测结果"""
        if not self.current_prediction:
            QMessageBox.warning(self, "警告", "没有可导出的预测结果")
            return
            
        try:
            from PyQt6.QtWidgets import QFileDialog
            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出预测结果", f"趋势预测_{self.current_prediction['timestamp']}.json", 
                "JSON文件 (*.json)"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.current_prediction, f, ensure_ascii=False, indent=2)
                    
                QMessageBox.information(self, "成功", f"预测结果已导出到: {file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
            
    def go_back(self):
        """返回主界面"""
        if hasattr(self.parent(), 'show_main_view'):
            self.parent().show_main_view()

    def on_prediction_finished(self, result):
        self.simulation_timer.stop()
        self.start_prediction_btn.setEnabled(True)
        # 展示AI预测结果
        self.overview_text.setPlainText(result)
        self.tab_widget.setCurrentIndex(0)
        QMessageBox.information(self, "预测完成", "趋势预测分析已完成！")

    def on_prediction_error(self, msg):
        self.simulation_timer.stop()
        self.start_prediction_btn.setEnabled(True)
        QMessageBox.critical(self, "预测失败", f"趋势预测过程中出现错误：\n{msg}\n请检查网络、API密钥或稍后重试。")

    def cancel_prediction(self):
        """取消预测流程"""
        self._prediction_canceled = True
        if hasattr(self, 'simulation_timer'):
            self.simulation_timer.stop()
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.close()
        self.start_prediction_btn.setEnabled(True) 