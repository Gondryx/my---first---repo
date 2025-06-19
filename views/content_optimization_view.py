from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTextEdit, QComboBox, QSpinBox, QGroupBox, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QFrame, QLineEdit, 
                             QCheckBox, QListWidget, QSplitter, QProgressBar, QSlider,
                             QTabWidget, QProgressDialog)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QDate
from PyQt6.QtGui import QFont
import json
import random

class ContentOptimizationView(QWidget):
    """内容优化界面"""
    
    optimization_started_signal = pyqtSignal(dict)
    optimization_completed_signal = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.optimizations = []
        self.current_optimization = None
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("内容优化")
        self.setMinimumSize(1200, 800)
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("内容优化")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧内容输入
        content_input_panel = self.create_content_input_panel()
        splitter.addWidget(content_input_panel)
        
        # 右侧优化结果
        optimization_results_panel = self.create_optimization_results_panel()
        splitter.addWidget(optimization_results_panel)
        
        # 设置分割器比例
        splitter.setSizes([500, 700])
        main_layout.addWidget(splitter)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.optimize_btn = QPushButton("开始优化")
        self.optimize_btn.clicked.connect(self.start_optimization)
        
        self.save_btn = QPushButton("保存优化")
        self.save_btn.clicked.connect(self.save_optimization)
        
        self.export_btn = QPushButton("导出内容")
        self.export_btn.clicked.connect(self.export_content)
        
        self.back_btn = QPushButton("返回主界面")
        self.back_btn.clicked.connect(self.go_back)
        
        button_layout.addWidget(self.optimize_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.back_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def create_content_input_panel(self):
        """创建内容输入面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setMaximumWidth(500)
        
        layout = QVBoxLayout()
        
        # 平台选择组
        platform_group = QGroupBox("发布平台")
        platform_layout = QVBoxLayout()
        
        self.platform_combo = QComboBox()
        self.platform_combo.addItems([
            "微博", "微信", "抖音", "小红书", "B站", "知乎", "多平台"
        ])
        platform_layout.addWidget(self.platform_combo)
        
        platform_group.setLayout(platform_layout)
        layout.addWidget(platform_group)
        
        # 内容类型组
        content_type_group = QGroupBox("内容类型")
        content_type_layout = QVBoxLayout()
        
        self.content_type_combo = QComboBox()
        self.content_type_combo.addItems([
            "文章", "视频", "图片", "直播", "活动", "问答", "故事"
        ])
        content_type_layout.addWidget(self.content_type_combo)
        
        content_type_group.setLayout(content_type_layout)
        layout.addWidget(content_type_group)
        
        # 原始内容组
        original_content_group = QGroupBox("原始内容")
        original_layout = QVBoxLayout()
        
        self.original_content = QTextEdit()
        self.original_content.setPlaceholderText("请输入要优化的原始内容...")
        self.original_content.setMinimumHeight(150)
        original_layout.addWidget(self.original_content)
        
        original_content_group.setLayout(original_layout)
        layout.addWidget(original_content_group)
        
        # 优化目标组
        optimization_goals_group = QGroupBox("优化目标")
        goals_layout = QVBoxLayout()
        
        self.goal_engagement = QCheckBox("提高互动率")
        self.goal_engagement.setChecked(True)
        goals_layout.addWidget(self.goal_engagement)
        
        self.goal_reach = QCheckBox("扩大传播范围")
        self.goal_reach.setChecked(True)
        goals_layout.addWidget(self.goal_reach)
        
        self.goal_conversion = QCheckBox("提高转化率")
        self.goal_conversion.setChecked(False)
        goals_layout.addWidget(self.goal_conversion)
        
        self.goal_brand = QCheckBox("提升品牌认知")
        self.goal_brand.setChecked(True)
        goals_layout.addWidget(self.goal_brand)
        
        optimization_goals_group.setLayout(goals_layout)
        layout.addWidget(optimization_goals_group)
        
        # 优化参数组
        optimization_params_group = QGroupBox("优化参数")
        params_layout = QVBoxLayout()
        
        # 创意程度
        creativity_layout = QHBoxLayout()
        creativity_layout.addWidget(QLabel("创意程度:"))
        self.creativity_slider = QSlider(Qt.Orientation.Horizontal)
        self.creativity_slider.setRange(1, 10)
        self.creativity_slider.setValue(7)
        self.creativity_label = QLabel("7")
        self.creativity_slider.valueChanged.connect(
            lambda v: self.creativity_label.setText(str(v))
        )
        creativity_layout.addWidget(self.creativity_slider)
        creativity_layout.addWidget(self.creativity_label)
        params_layout.addLayout(creativity_layout)
        
        # 专业程度
        professionalism_layout = QHBoxLayout()
        professionalism_layout.addWidget(QLabel("专业程度:"))
        self.professionalism_slider = QSlider(Qt.Orientation.Horizontal)
        self.professionalism_slider.setRange(1, 10)
        self.professionalism_slider.setValue(8)
        self.professionalism_label = QLabel("8")
        self.professionalism_slider.valueChanged.connect(
            lambda v: self.professionalism_label.setText(str(v))
        )
        professionalism_layout.addWidget(self.professionalism_slider)
        professionalism_layout.addWidget(self.professionalism_label)
        params_layout.addLayout(professionalism_layout)
        
        # 目标受众
        audience_layout = QHBoxLayout()
        audience_layout.addWidget(QLabel("目标受众:"))
        self.target_audience = QLineEdit()
        self.target_audience.setPlaceholderText("例如：18-35岁年轻女性")
        audience_layout.addWidget(self.target_audience)
        params_layout.addLayout(audience_layout)
        
        optimization_params_group.setLayout(params_layout)
        layout.addWidget(optimization_params_group)
        
        # 关键词组
        keywords_group = QGroupBox("关键词设置")
        keywords_layout = QVBoxLayout()
        
        self.keywords_input = QTextEdit()
        self.keywords_input.setMaximumHeight(80)
        self.keywords_input.setPlaceholderText("输入相关关键词，每行一个")
        keywords_layout.addWidget(self.keywords_input)
        
        keywords_group.setLayout(keywords_layout)
        layout.addWidget(keywords_group)
        
        panel.setLayout(layout)
        return panel
        
    def create_optimization_results_panel(self):
        """创建优化结果面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout()
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 优化内容标签页
        self.optimized_content_tab = QWidget()
        optimized_layout = QVBoxLayout(self.optimized_content_tab)
        
        self.optimized_content = QTextEdit()
        self.optimized_content.setReadOnly(True)
        self.optimized_content.setPlaceholderText("优化完成后将显示优化后的内容...")
        optimized_layout.addWidget(self.optimized_content)
        
        self.tab_widget.addTab(self.optimized_content_tab, "优化内容")
        
        # 优化建议标签页
        self.suggestions_tab = QWidget()
        suggestions_layout = QVBoxLayout(self.suggestions_tab)
        
        self.suggestions_text = QTextEdit()
        self.suggestions_text.setReadOnly(True)
        self.suggestions_text.setPlaceholderText("优化完成后将显示详细建议...")
        suggestions_layout.addWidget(self.suggestions_text)
        
        self.tab_widget.addTab(self.suggestions_tab, "优化建议")
        
        # 效果预测标签页
        self.prediction_tab = QWidget()
        prediction_layout = QVBoxLayout(self.prediction_tab)
        
        self.prediction_text = QTextEdit()
        self.prediction_text.setReadOnly(True)
        self.prediction_text.setPlaceholderText("优化完成后将显示效果预测...")
        prediction_layout.addWidget(self.prediction_text)
        
        self.tab_widget.addTab(self.prediction_tab, "效果预测")
        
        # 对比分析标签页
        self.comparison_tab = QWidget()
        comparison_layout = QVBoxLayout(self.comparison_tab)
        
        self.comparison_table = QTableWidget()
        self.comparison_table.setColumnCount(4)
        self.comparison_table.setHorizontalHeaderLabels(["指标", "原始内容", "优化后", "提升幅度"])
        comparison_layout.addWidget(self.comparison_table)
        
        self.tab_widget.addTab(self.comparison_tab, "对比分析")
        
        layout.addWidget(self.tab_widget)
        
        panel.setLayout(layout)
        return panel
        
    def start_optimization(self):
        """开始优化"""
        if not self.original_content.toPlainText().strip():
            QMessageBox.warning(self, "警告", "请输入要优化的内容")
            return
            
        # 获取优化参数
        optimization_params = {
            'platform': self.platform_combo.currentText(),
            'content_type': self.content_type_combo.currentText(),
            'original_content': self.original_content.toPlainText(),
            'goals': {
                'engagement': self.goal_engagement.isChecked(),
                'reach': self.goal_reach.isChecked(),
                'conversion': self.goal_conversion.isChecked(),
                'brand': self.goal_brand.isChecked()
            },
            'creativity': self.creativity_slider.value(),
            'professionalism': self.professionalism_slider.value(),
            'target_audience': self.target_audience.text(),
            'keywords': self.keywords_input.toPlainText().split('\n')
        }
        
        # 显示QProgressDialog
        self.progress_dialog = QProgressDialog("正在优化内容，请稍候...", "取消", 0, 100, self)
        self.progress_dialog.setWindowTitle("内容优化进度")
        self.progress_dialog.setWindowModality(Qt.WindowModality.NonModal)
        self.progress_dialog.setValue(0)
        self.progress_dialog.canceled.connect(self.cancel_optimization)
        self.progress_dialog.show()
        self._optimization_canceled = False
        
        # 模拟优化过程
        self.simulation_timer = QTimer()
        self.simulation_timer.timeout.connect(self.update_progress)
        self.simulation_timer.start(100)
        
        # 发送优化开始信号
        self.optimization_started_signal.emit(optimization_params)
        
    def update_progress(self):
        """更新进度条"""
        if hasattr(self, '_optimization_canceled') and self._optimization_canceled:
            self.simulation_timer.stop()
            if hasattr(self, 'progress_dialog'):
                self.progress_dialog.close()
            self.optimize_btn.setEnabled(True)
            return
        current_value = self.progress_dialog.value() if hasattr(self, 'progress_dialog') else 0
        if current_value < 100:
            if hasattr(self, 'progress_dialog'):
                self.progress_dialog.setValue(current_value + 5)
        else:
            self.simulation_timer.stop()
            if hasattr(self, 'progress_dialog'):
                self.progress_dialog.close()
            self.generate_optimization_results()
            
    def generate_optimization_results(self):
        """生成优化结果（模拟）"""
        platform = self.platform_combo.currentText()
        content_type = self.content_type_combo.currentText()
        original_content = self.original_content.toPlainText()
        
        # 生成优化后的内容
        optimized_content = f"""
【优化后的内容】

{original_content}

#社交媒体营销 #{platform} #{content_type}

💡 小贴士：根据{platform}平台特点，建议在以下时间发布：
- 工作日：19:00-21:00
- 周末：10:00-12:00, 15:00-17:00

🎯 目标受众：{self.target_audience.text() or '年轻用户群体'}

📈 预期效果：互动率提升30%，传播范围扩大50%
        """
        
        # 生成优化建议
        suggestions = f"""
内容优化建议：

1. 标题优化
   - 使用数字开头，如"5个技巧"、"3个方法"
   - 添加情感词汇，如"震惊"、"必看"、"独家"
   - 控制在20字以内，提高点击率

2. 内容结构优化
   - 使用emoji表情，增加视觉吸引力
   - 分段清晰，每段不超过3行
   - 添加话题标签，提高发现率

3. 互动元素
   - 在内容末尾添加问题，鼓励评论
   - 使用"你觉得呢？"、"欢迎分享"等引导语
   - 设置投票或问卷，增加参与度

4. 视觉优化
   - 配图要高清、有吸引力
   - 使用品牌色彩，保持一致性
   - 考虑视频内容，提高完播率

5. 发布时间优化
   - 根据平台用户活跃时间发布
   - 避开竞品发布时间
   - 保持发布频率一致性
        """
        
        # 生成效果预测
        prediction = f"""
效果预测分析：

📊 互动率预测
- 原始内容预期互动率：2.5%
- 优化后预期互动率：4.2%
- 提升幅度：68%

📈 传播范围预测
- 原始内容预期触达：1,000人
- 优化后预期触达：1,800人
- 提升幅度：80%

🎯 转化率预测
- 原始内容预期转化：0.8%
- 优化后预期转化：1.5%
- 提升幅度：87.5%

⏰ 最佳发布时间
- 工作日：19:00-21:00
- 周末：10:00-12:00, 15:00-17:00
- 节假日：全天分布均匀

💰 ROI预测
- 预期投入：内容制作成本
- 预期收益：品牌曝光 + 用户增长
- 投资回报率：预计300%+
        """
        
        # 生成对比分析表格
        self.comparison_table.setRowCount(6)
        comparison_data = [
            ["互动率", "2.5%", "4.2%", "+68%"],
            ["传播范围", "1,000人", "1,800人", "+80%"],
            ["转化率", "0.8%", "1.5%", "+87.5%"],
            ["完播率", "45%", "68%", "+51%"],
            ["分享率", "1.2%", "2.8%", "+133%"],
            ["评论率", "0.8%", "1.6%", "+100%"]
        ]
        
        for i, (metric, original, optimized, improvement) in enumerate(comparison_data):
            self.comparison_table.setItem(i, 0, QTableWidgetItem(metric))
            self.comparison_table.setItem(i, 1, QTableWidgetItem(original))
            self.comparison_table.setItem(i, 2, QTableWidgetItem(optimized))
            self.comparison_table.setItem(i, 3, QTableWidgetItem(improvement))
            
        # 更新界面
        self.optimized_content.setPlainText(optimized_content)
        self.suggestions_text.setPlainText(suggestions)
        self.prediction_text.setPlainText(prediction)
        
        # 切换到优化内容标签页
        self.tab_widget.setCurrentIndex(0)
        
        # 保存优化结果
        self.current_optimization = {
            'platform': platform,
            'content_type': content_type,
            'original_content': original_content,
            'optimized_content': optimized_content,
            'suggestions': suggestions,
            'prediction': prediction,
            'timestamp': QDate.currentDate().toString("yyyy-MM-dd")
        }
        
        QMessageBox.information(self, "优化完成", "内容优化已完成！")
        
    def save_optimization(self):
        """保存优化结果"""
        if not self.current_optimization:
            QMessageBox.warning(self, "警告", "没有可保存的优化结果")
            return
            
        try:
            # 这里应该保存到数据库
            self.optimizations.append(self.current_optimization)
            QMessageBox.information(self, "成功", "优化结果已保存")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
            
    def export_content(self):
        """导出内容"""
        if not self.current_optimization:
            QMessageBox.warning(self, "警告", "没有可导出的内容")
            return
            
        try:
            from PyQt6.QtWidgets import QFileDialog
            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出优化内容", f"优化内容_{self.current_optimization['timestamp']}.txt", 
                "文本文件 (*.txt)"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("=== 原始内容 ===\n")
                    f.write(self.current_optimization['original_content'])
                    f.write("\n\n=== 优化后内容 ===\n")
                    f.write(self.current_optimization['optimized_content'])
                    f.write("\n\n=== 优化建议 ===\n")
                    f.write(self.current_optimization['suggestions'])
                    f.write("\n\n=== 效果预测 ===\n")
                    f.write(self.current_optimization['prediction'])
                    
                QMessageBox.information(self, "成功", f"内容已导出到: {file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
            
    def go_back(self):
        """返回主界面"""
        if hasattr(self.parent(), 'show_main_view'):
            self.parent().show_main_view()
            
    def cancel_optimization(self):
        """取消优化流程"""
        self._optimization_canceled = True
        if hasattr(self, 'simulation_timer'):
            self.simulation_timer.stop()
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.close()
        self.optimize_btn.setEnabled(True) 