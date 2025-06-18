import sys
from PyQt6.QtWidgets import QApplication
import matplotlib
matplotlib.use('qtagg')

from pathlib import Path
# 获取main.py所在的目录（项目根目录）
project_root = Path(__file__).parent
# 将项目根目录添加到Python搜索路径
sys.path.append(str(project_root))
# 现在可以导入controllers模块
from controllers.main_controller import MainController

def main():
    app = QApplication(sys.argv)
    
    # 设置全局样式
    app.setStyle("Fusion")
    
    # 应用苹果风格的样式
    app.setStyleSheet("""
        QWidget {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 13px;
        }
        QMainWindow, QDialog {
            background-color: #f5f5f7;
        }
        QLabel {
            color: #1d1d1f;
        }
        QPushButton {
            background-color: #0071e3;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #0066cc;
        }
        QPushButton:pressed {
            background-color: #0050a0;
        }
        QLineEdit, QTextEdit, QComboBox {
            border: 1px solid #d2d2d7;
            border-radius: 4px;
            padding: 5px;
            background-color: white;
        }
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
            border-color: #0071e3;
            outline: none;
        }
        QTabWidget::pane {
            border: 1px solid #d2d2d7;
            border-radius: 4px;
            background-color: white;
        }
        QTabBar::tab {
            background-color: #f5f5f7;
            border: 1px solid #d2d2d7;
            border-bottom: none;
            border-radius: 4px 4px 0 0;
            padding: 5px 10px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: white;
            color: #0071e3;
        }
        QTableView {
            gridline-color: #d2d2d7;
            border: 1px solid #d2d2d7;
            border-radius: 4px;
        }
        QHeaderView::section {
            background-color: #f5f5f7;
            border: none;
            border-bottom: 1px solid #d2d2d7;
            padding: 5px;
        }
        QScrollBar:vertical {
            background: #f5f5f7;
            width: 12px;
            margin: 0;
        }
        QScrollBar::handle:vertical {
            background: #d2d2d7;
            min-height: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical:hover {
            background: #b8b8b8;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0;
        }
        QScrollBar:horizontal {
            background: #f5f5f7;
            height: 12px;
            margin: 0;
        }
        QScrollBar::handle:horizontal {
            background: #d2d2d7;
            min-width: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal:hover {
            background: #b8b8b8;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0;
        }
    """)
    
    controller = MainController()
    controller.show_login_view()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
