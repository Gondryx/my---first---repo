from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFileDialog, QTextEdit, QComboBox,
                             QTableWidget, QTableWidgetItem, QProgressBar,
                             QMessageBox, QGroupBox, QGridLayout, QSpinBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
import pandas as pd
import os
from datetime import datetime

class DataImportView(QWidget):
    """数据导入界面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = None
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("数据导入")
        self.setMinimumSize(800, 600)
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("社交媒体数据导入")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 文件选择区域
        file_group = QGroupBox("文件选择")
        file_layout = QGridLayout()
        
        self.file_path_label = QLabel("未选择文件")
        self.file_path_label.setStyleSheet("color: #666; padding: 5px; border: 1px solid #ddd; border-radius: 4px;")
        
        self.select_file_btn = QPushButton("选择文件")
        self.select_file_btn.clicked.connect(self.select_file)
        
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems(["CSV文件", "Excel文件", "JSON文件"])
        
        file_layout.addWidget(QLabel("文件类型:"), 0, 0)
        file_layout.addWidget(self.file_type_combo, 0, 1)
        file_layout.addWidget(QLabel("文件路径:"), 1, 0)
        file_layout.addWidget(self.file_path_label, 1, 1)
        file_layout.addWidget(self.select_file_btn, 1, 2)
        
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)
        
        # 数据预览区域
        preview_group = QGroupBox("数据预览")
        preview_layout = QVBoxLayout()
        
        self.preview_table = QTableWidget()
        self.preview_table.setMaximumHeight(200)
        preview_layout.addWidget(self.preview_table)
        
        preview_group.setLayout(preview_layout)
        main_layout.addWidget(preview_group)
        
        # 导入选项区域
        options_group = QGroupBox("导入选项")
        options_layout = QGridLayout()
        
        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems(["utf-8", "gbk", "gb2312", "latin1"])
        
        self.separator_combo = QComboBox()
        self.separator_combo.addItems([",", ";", "\t", "|"])
        
        self.header_checkbox = QPushButton("包含表头")
        self.header_checkbox.setCheckable(True)
        self.header_checkbox.setChecked(True)
        
        self.max_rows_spin = QSpinBox()
        self.max_rows_spin.setRange(100, 100000)
        self.max_rows_spin.setValue(1000)
        
        options_layout.addWidget(QLabel("编码格式:"), 0, 0)
        options_layout.addWidget(self.encoding_combo, 0, 1)
        options_layout.addWidget(QLabel("分隔符:"), 0, 2)
        options_layout.addWidget(self.separator_combo, 0, 3)
        options_layout.addWidget(QLabel("包含表头:"), 1, 0)
        options_layout.addWidget(self.header_checkbox, 1, 1)
        options_layout.addWidget(QLabel("最大行数:"), 1, 2)
        options_layout.addWidget(self.max_rows_spin, 1, 3)
        
        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.import_btn = QPushButton("导入数据")
        self.import_btn.clicked.connect(self.import_data)
        self.import_btn.setEnabled(False)
        
        self.clear_btn = QPushButton("清空")
        self.clear_btn.clicked.connect(self.clear_data)
        
        self.back_btn = QPushButton("返回")
        self.back_btn.clicked.connect(self.go_back)
        
        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.back_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def select_file(self):
        """选择文件"""
        file_type = self.file_type_combo.currentText()
        
        if "CSV" in file_type:
            file_filter = "CSV文件 (*.csv)"
        elif "Excel" in file_type:
            file_filter = "Excel文件 (*.xlsx *.xls)"
        else:
            file_filter = "JSON文件 (*.json)"
            
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "", file_filter
        )
        
        if file_path:
            self.file_path_label.setText(file_path)
            self.import_btn.setEnabled(True)
            self.preview_data(file_path)
            
    def preview_data(self, file_path):
        """预览数据"""
        try:
            file_type = self.file_type_combo.currentText()
            
            if "CSV" in file_type:
                encoding = self.encoding_combo.currentText()
                separator = self.separator_combo.currentText()
                header = 0 if self.header_checkbox.isChecked() else None
                
                data = pd.read_csv(
                    file_path, 
                    encoding=encoding, 
                    sep=separator, 
                    header=header,
                    nrows=100  # 只预览前100行
                )
            elif "Excel" in file_type:
                data = pd.read_excel(file_path, nrows=100)
            else:
                data = pd.read_json(file_path)
                if isinstance(data, dict):
                    # 如果是嵌套的JSON，尝试展平
                    data = pd.json_normalize(data)
                    
            # 显示预览
            self.display_preview(data)
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"文件预览失败: {str(e)}")
            
    def display_preview(self, data):
        """显示数据预览"""
        self.preview_table.setRowCount(min(len(data), 100))
        self.preview_table.setColumnCount(len(data.columns))
        
        # 设置表头
        self.preview_table.setHorizontalHeaderLabels(data.columns)
        
        # 填充数据
        for i in range(min(len(data), 100)):
            for j in range(len(data.columns)):
                item = QTableWidgetItem(str(data.iloc[i, j]))
                self.preview_table.setItem(i, j, item)
                
        # 调整列宽
        self.preview_table.resizeColumnsToContents()
        
    def import_data(self):
        """导入数据"""
        file_path = self.file_path_label.text()
        if file_path == "未选择文件":
            QMessageBox.warning(self, "警告", "请先选择文件")
            return
            
        try:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            # 获取导入参数
            encoding = self.encoding_combo.currentText()
            separator = self.separator_combo.currentText()
            has_header = self.header_checkbox.isChecked()
            max_rows = self.max_rows_spin.value()
            
            self.progress_bar.setValue(20)
            
            # 调用数据导入功能
            if hasattr(self, 'controller') and self.controller:
                # 如果有控制器，使用控制器的导入功能
                import_result = self.controller.import_data_file(
                    file_path, encoding, separator, has_header, max_rows
                )
            else:
                # 直接使用数据模型导入
                from models.social_media_data import SocialMediaData
                data_model = SocialMediaData()
                import_result = data_model.import_csv_data(
                    file_path, encoding, separator, has_header
                )
            
            self.progress_bar.setValue(80)
            
            if import_result['valid']:
                self.progress_bar.setValue(100)
                QMessageBox.information(self, "导入成功", import_result['message'])
                
                # 保存数据到本地
                if hasattr(self, 'controller') and self.controller:
                    save_result = self.controller.save_imported_data(
                        import_result['data'], 
                        f"imported_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    )
                    if save_result['success']:
                        QMessageBox.information(self, "保存成功", save_result['message'])
                else:
                    # 直接保存到data目录
                    import os
                    data_dir = "data"
                    os.makedirs(data_dir, exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"imported_data_{timestamp}.csv"
                    file_path = os.path.join(data_dir, filename)
                    import_result['data'].to_csv(file_path, index=False, encoding='utf-8')
                    QMessageBox.information(self, "保存成功", f"数据已保存到: {filename}")
                    
            else:
                QMessageBox.critical(self, "导入失败", import_result['error'])
                
        except Exception as e:
            QMessageBox.critical(self, "导入失败", f"导入过程中发生错误: {str(e)}")
        finally:
            self.progress_bar.setVisible(False)
            
    def clear_data(self):
        """清空数据"""
        self.data = None
        self.file_path_label.setText("未选择文件")
        self.preview_table.setRowCount(0)
        self.preview_table.setColumnCount(0)
        self.import_btn.setEnabled(False)
        
    def go_back(self):
        """返回主界面"""
        if hasattr(self.parent(), 'show_main_view'):
            self.parent().show_main_view() 