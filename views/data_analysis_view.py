from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QComboBox, QTabWidget,
                             QTableWidget, QTableWidgetItem, QProgressBar,
                             QMessageBox, QGroupBox, QGridLayout, QSplitter,
                             QScrollArea, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
import pandas as pd
import json
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.data_analyzer import DataAnalyzer
from models.ai_service import AIService

class AnalysisWorker(QThread):
    """分析工作线程"""
    progress_updated = pyqtSignal(int)
    analysis_completed = pyqtSignal(dict)
    
    def __init__(self, data, analysis_type, **kwargs):
        super().__init__()
        self.data = data
        self.analysis_type = analysis_type
        self.kwargs = kwargs
        
    def run(self):
        """运行分析"""
        try:
            analyzer = DataAnalyzer()
            analyzer.load_data(self.data)
            
            if self.analysis_type == "basic":
                result = analyzer.basic_statistics()
            elif self.analysis_type == "time_series":
                result = analyzer.time_series_analysis(self.kwargs.get('date_column'))
            elif self.analysis_type == "engagement":
                result = analyzer.engagement_analysis(self.kwargs.get('engagement_columns', []))
            elif self.analysis_type == "content":
                result = analyzer.content_analysis(self.kwargs.get('text_column'))
            elif self.analysis_type == "sentiment":
                result = analyzer.sentiment_analysis(self.kwargs.get('text_column'))
            elif self.analysis_type == "ai_analysis":
                ai_service = AIService()
                result = ai_service.analyze_social_media_data(self.data)
            else:
                result = {"error": "未知的分析类型"}
                
            self.analysis_completed.emit(result)
            
        except Exception as e:
            self.analysis_completed.emit({"error": str(e)})

class DataAnalysisView(QWidget):
    """数据分析界面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = None
        self.analyzer = DataAnalyzer()
        self.ai_service = AIService()
        self.analysis_results = {}
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("数据分析")
        self.setMinimumSize(1200, 800)
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("社交媒体数据分析")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧控制面板
        control_panel = self.create_control_panel()
        splitter.addWidget(control_panel)
        
        # 右侧结果显示区域
        result_panel = self.create_result_panel()
        splitter.addWidget(result_panel)
        
        # 设置分割器比例
        splitter.setSizes([300, 900])
        main_layout.addWidget(splitter)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.back_btn = QPushButton("返回主界面")
        self.back_btn.clicked.connect(self.go_back)
        
        self.export_btn = QPushButton("导出报告")
        self.export_btn.clicked.connect(self.export_report)
        
        button_layout.addWidget(self.export_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.back_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def create_control_panel(self):
        """创建控制面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setMaximumWidth(300)
        
        layout = QVBoxLayout()
        
        # 数据信息
        data_info_group = QGroupBox("数据信息")
        data_info_layout = QVBoxLayout()
        
        self.data_info_label = QLabel("未加载数据")
        self.data_info_label.setWordWrap(True)
        data_info_layout.addWidget(self.data_info_label)
        
        data_info_group.setLayout(data_info_layout)
        layout.addWidget(data_info_group)
        
        # 分析选项
        analysis_group = QGroupBox("分析选项")
        analysis_layout = QVBoxLayout()
        
        # 基础统计
        self.basic_btn = QPushButton("基础统计分析")
        self.basic_btn.clicked.connect(lambda: self.run_analysis("basic"))
        analysis_layout.addWidget(self.basic_btn)
        
        # 时间序列分析
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("日期列:"))
        self.date_column_combo = QComboBox()
        time_layout.addWidget(self.date_column_combo)
        analysis_layout.addLayout(time_layout)
        
        self.time_series_btn = QPushButton("时间序列分析")
        self.time_series_btn.clicked.connect(lambda: self.run_analysis("time_series"))
        analysis_layout.addWidget(self.time_series_btn)
        
        # 互动分析
        engagement_layout = QHBoxLayout()
        engagement_layout.addWidget(QLabel("互动列:"))
        self.engagement_column_combo = QComboBox()
        self.engagement_column_combo.setEditable(True)
        engagement_layout.addWidget(self.engagement_column_combo)
        analysis_layout.addLayout(engagement_layout)
        
        self.engagement_btn = QPushButton("互动分析")
        self.engagement_btn.clicked.connect(lambda: self.run_analysis("engagement"))
        analysis_layout.addWidget(self.engagement_btn)
        
        # 内容分析
        content_layout = QHBoxLayout()
        content_layout.addWidget(QLabel("文本列:"))
        self.text_column_combo = QComboBox()
        content_layout.addWidget(self.text_column_combo)
        analysis_layout.addLayout(content_layout)
        
        self.content_btn = QPushButton("内容分析")
        self.content_btn.clicked.connect(lambda: self.run_analysis("content"))
        analysis_layout.addWidget(self.content_btn)
        
        # 情感分析
        self.sentiment_btn = QPushButton("情感分析")
        self.sentiment_btn.clicked.connect(lambda: self.run_analysis("sentiment"))
        analysis_layout.addWidget(self.sentiment_btn)
        
        # AI分析
        self.ai_analysis_btn = QPushButton("AI智能分析")
        self.ai_analysis_btn.setStyleSheet("background-color: #0071e3; color: white; font-weight: bold;")
        self.ai_analysis_btn.clicked.connect(lambda: self.run_analysis("ai_analysis"))
        analysis_layout.addWidget(self.ai_analysis_btn)
        
        analysis_group.setLayout(analysis_layout)
        layout.addWidget(analysis_group)
        
        # 图表生成
        chart_group = QGroupBox("图表生成")
        chart_layout = QVBoxLayout()
        
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems([
            "互动趋势图", "内容分布图", "情感饼图", "词云图"
        ])
        chart_layout.addWidget(self.chart_type_combo)
        
        self.generate_chart_btn = QPushButton("生成图表")
        self.generate_chart_btn.clicked.connect(self.generate_chart)
        chart_layout.addWidget(self.generate_chart_btn)
        
        chart_group.setLayout(chart_layout)
        layout.addWidget(chart_group)
        
        layout.addStretch()
        panel.setLayout(layout)
        return panel
        
    def create_result_panel(self):
        """创建结果面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout()
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 文本结果标签页
        self.text_result_tab = QWidget()
        text_layout = QVBoxLayout()
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        text_layout.addWidget(self.result_text)
        
        self.text_result_tab.setLayout(text_layout)
        self.tab_widget.addTab(self.text_result_tab, "分析结果")
        
        # 表格结果标签页
        self.table_result_tab = QWidget()
        table_layout = QVBoxLayout()
        
        self.result_table = QTableWidget()
        table_layout.addWidget(self.result_table)
        
        self.table_result_tab.setLayout(table_layout)
        self.tab_widget.addTab(self.table_result_tab, "数据表格")
        
        # 图表结果标签页
        self.chart_result_tab = QWidget()
        chart_layout = QVBoxLayout()
        
        # 使用标签显示图表（简化版本）
        self.chart_view = QLabel("图表显示区域")
        self.chart_view.setStyleSheet("border: 1px solid #ddd; background-color: #f9f9f9;")
        chart_layout.addWidget(self.chart_view)
        
        self.chart_result_tab.setLayout(chart_layout)
        self.tab_widget.addTab(self.chart_result_tab, "图表展示")
        
        layout.addWidget(self.tab_widget)
        panel.setLayout(layout)
        return panel
        
    def set_data(self, data):
        """设置数据"""
        self.data = data
        self.analyzer.load_data(data)
        
        # 更新数据信息
        if data is not None:
            info_text = f"数据形状: {data.shape[0]} 行 × {data.shape[1]} 列\n"
            info_text += f"列名: {', '.join(data.columns.tolist())}"
            self.data_info_label.setText(info_text)
            
            # 更新列选择下拉框
            self.date_column_combo.clear()
            self.engagement_column_combo.clear()
            self.text_column_combo.clear()
            
            for col in data.columns:
                self.date_column_combo.addItem(col)
                self.engagement_column_combo.addItem(col)
                self.text_column_combo.addItem(col)
                
            # 启用分析按钮
            self.enable_analysis_buttons(True)
        else:
            self.data_info_label.setText("未加载数据")
            self.enable_analysis_buttons(False)
            
    def enable_analysis_buttons(self, enabled):
        """启用/禁用分析按钮"""
        self.basic_btn.setEnabled(enabled)
        self.time_series_btn.setEnabled(enabled)
        self.engagement_btn.setEnabled(enabled)
        self.content_btn.setEnabled(enabled)
        self.sentiment_btn.setEnabled(enabled)
        self.ai_analysis_btn.setEnabled(enabled)
        self.generate_chart_btn.setEnabled(enabled)
        
    def run_analysis(self, analysis_type):
        """运行分析"""
        if self.data is None:
            QMessageBox.warning(self, "警告", "请先加载数据")
            return
            
        # 准备参数
        kwargs = {}
        if analysis_type == "time_series":
            kwargs['date_column'] = self.date_column_combo.currentText()
        elif analysis_type == "engagement":
            engagement_cols = self.engagement_column_combo.currentText().split(',')
            kwargs['engagement_columns'] = [col.strip() for col in engagement_cols]
        elif analysis_type in ["content", "sentiment"]:
            kwargs['text_column'] = self.text_column_combo.currentText()
            
        # 创建并启动工作线程
        self.worker = AnalysisWorker(self.data, analysis_type, **kwargs)
        self.worker.progress_updated.connect(self.progress_bar.setValue)
        self.worker.analysis_completed.connect(self.handle_analysis_result)
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 禁用按钮
        self.enable_analysis_buttons(False)
        
        self.worker.start()
        
    def handle_analysis_result(self, result):
        """处理分析结果"""
        self.progress_bar.setVisible(False)
        self.enable_analysis_buttons(True)
        
        if "error" in result:
            QMessageBox.critical(self, "错误", f"分析失败: {result['error']}")
            return
            
        # 保存结果
        analysis_type = getattr(self.worker, 'analysis_type', 'unknown')
        self.analysis_results[analysis_type] = result
        
        # 显示结果
        self.display_result(result, analysis_type)
        
    def display_result(self, result, analysis_type):
        """显示分析结果"""
        # 显示文本结果
        if analysis_type == "ai_analysis":
            text_content = result.get("analysis", "无分析结果")
        else:
            text_content = json.dumps(result, ensure_ascii=False, indent=2)
            
        self.result_text.setText(text_content)
        
        # 显示表格结果（如果有）
        if isinstance(result, dict) and any(isinstance(v, (list, pd.Series)) for v in result.values()):
            self.display_table_result(result)
            
        # 切换到文本结果标签页
        self.tab_widget.setCurrentIndex(0)
        
    def display_table_result(self, result):
        """显示表格结果"""
        # 找到可以显示为表格的数据
        table_data = None
        for key, value in result.items():
            if isinstance(value, (list, pd.Series)):
                table_data = value
                break
                
        if table_data is not None:
            if isinstance(table_data, pd.Series):
                df = pd.DataFrame(table_data)
            else:
                df = pd.DataFrame(table_data)
                
            self.result_table.setRowCount(len(df))
            self.result_table.setColumnCount(len(df.columns))
            self.result_table.setHorizontalHeaderLabels(df.columns)
            
            for i in range(len(df)):
                for j in range(len(df.columns)):
                    item = QTableWidgetItem(str(df.iloc[i, j]))
                    self.result_table.setItem(i, j, item)
                    
            self.result_table.resizeColumnsToContents()
            
    def generate_chart(self):
        """生成图表"""
        if self.data is None:
            QMessageBox.warning(self, "警告", "请先加载数据")
            return
            
        chart_type = self.chart_type_combo.currentText()
        
        try:
            if chart_type == "互动趋势图":
                date_col = self.date_column_combo.currentText()
                engagement_col = self.engagement_column_combo.currentText().split(',')[0].strip()
                result = self.analyzer.generate_charts("engagement_trend", 
                                                      date_column=date_col, 
                                                      engagement_column=engagement_col)
            elif chart_type == "内容分布图":
                text_col = self.text_column_combo.currentText()
                result = self.analyzer.generate_charts("content_distribution", column=text_col)
            elif chart_type == "情感饼图":
                text_col = self.text_column_combo.currentText()
                result = self.analyzer.generate_charts("sentiment_pie", text_column=text_col)
            elif chart_type == "词云图":
                text_col = self.text_column_combo.currentText()
                result = self.analyzer.generate_charts("wordcloud", text_column=text_col)
            else:
                QMessageBox.warning(self, "警告", "不支持的图表类型")
                return
                
            if "error" in result:
                QMessageBox.critical(self, "错误", f"图表生成失败: {result['error']}")
                return
                
            # 显示图表
            self.display_chart(result)
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"图表生成失败: {str(e)}")
            
    def display_chart(self, chart_result):
        """显示图表"""
        try:
            # 简化版本：显示图表信息
            chart_info = f"图表类型: {chart_result.get('chart_type', '未知')}\n"
            if 'data' in chart_result:
                chart_info += f"数据点数量: {len(chart_result['data'])}\n"
                
            self.chart_view.setText(chart_info)
            
            # 切换到图表标签页
            self.tab_widget.setCurrentIndex(2)
            
        except Exception as e:
            QMessageBox.warning(self, "警告", f"图表显示失败: {str(e)}")
            
    def export_report(self):
        """导出报告"""
        if not self.analysis_results:
            QMessageBox.warning(self, "警告", "没有可导出的分析结果")
            return
            
        try:
            from PyQt6.QtWidgets import QFileDialog
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存报告", "", "JSON文件 (*.json)"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.analysis_results, f, ensure_ascii=False, indent=2)
                    
                QMessageBox.information(self, "成功", f"报告已导出到: {file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"报告导出失败: {str(e)}")
            
    def go_back(self):
        """返回主界面"""
        if hasattr(self.parent(), 'show_main_view'):
            self.parent().show_main_view() 