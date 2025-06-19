import sys
import matplotlib
matplotlib.use('qtagg')
from PyQt6.QtWidgets import QApplication, QMessageBox
import platform
from PyQt6.QtCore import QTimer

from pathlib import Path
# 获取main.py所在的目录（项目根目录）
project_root = Path(__file__).parent
# 将项目根目录添加到Python搜索路径
sys.path.append(str(project_root))
# 现在可以导入controllers模块
from controllers.main_controller import MainController
from PyQt6.QtCore import QThread, pyqtSignal
import requests

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
            # 用官方的test_connection方法，避免卡死
            ok = api.test_connection()
            self.result_signal.emit(ok, "" if ok else "API连接失败")
        except Exception as e:
            self.result_signal.emit(False, str(e))

def is_windows_dark_mode():
    if platform.system() != "Windows":
        return False
    try:
        import winreg
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize")
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return value == 0  # 0=深色, 1=浅色
    except Exception:
        return False

class ThemeWatcher:
    def __init__(self, app):
        self.app = app
        self.last_dark = is_windows_dark_mode()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_theme)
        self.timer.start(1000)  # 每秒检测一次

    def check_theme(self):
        current_dark = is_windows_dark_mode()
        if current_dark != self.last_dark:
            self.last_dark = current_dark
            self.apply_theme()

    def apply_theme(self):
        from PyQt6.QtGui import QPalette, QColor
        if self.last_dark:
            # 深色
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor("#23272e"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#181a20"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#23272e"))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#23272e"))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#23272e"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.BrightText, QColor("#ff5555"))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#1976d2"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
            self.app.setPalette(palette)
            self.app.setStyleSheet("""
                QWidget { font-family: '微软雅黑', Arial, sans-serif; font-size: 13px; background-color: #23272e; color: #ffffff; }
                QMainWindow, QDialog { background-color: #23272e; }
                QLabel { color: #ffffff; font-size: 14px; font-weight: bold; }
                QPushButton { min-width: 80px; min-height: 32px; border-radius: 5px; background-color: #1976d2; color: #ffffff; font-weight: bold; }
                QPushButton:hover { background-color: #1565c0; }
                QPushButton:pressed { background-color: #0050a0; }
                QLineEdit, QTextEdit, QComboBox { border: 1px solid #444a58; border-radius: 4px; padding: 5px; background-color: #181a20; color: #ffffff; }
                QLineEdit:focus, QTextEdit:focus, QComboBox:focus { border-color: #1976d2; outline: none; }
                QTabWidget::pane { border: 1px solid #444a58; border-radius: 6px; }
                QTabBar::tab { background-color: #23272e; border: 1px solid #444a58; border-bottom: none; border-radius: 4px 4px 0 0; padding: 5px 10px; margin-right: 2px; color: #ffffff; }
                QTabBar::tab:selected { background-color: #181a20; color: #1976d2; }
                QTableView { gridline-color: #444a58; border: 1px solid #444a58; border-radius: 4px; color: #ffffff; background-color: #23272e; }
                QHeaderView::section { background-color: #181a20; font-weight: bold; border: 1px solid #444a58; color: #ffffff; }
                QGroupBox { font-weight: bold; border: 1px solid #444a58; border-radius: 6px; margin-top: 10px; color: #ffffff; }
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }
                QTableWidget { alternate-background-color: #23272e; gridline-color: #444a58; color: #ffffff; }
            """)
        else:
            # 浅色
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor("#f5f5f7"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#1d1d1f"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#f5f5f7"))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#1d1d1f"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#1d1d1f"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#f5f5f7"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#1d1d1f"))
            palette.setColor(QPalette.ColorRole.BrightText, QColor("#ff0000"))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#1976d2"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
            self.app.setPalette(palette)
            self.app.setStyleSheet("""
                QWidget { font-family: '微软雅黑', Arial, sans-serif; font-size: 13px; background-color: #f5f5f7; color: #1d1d1f; }
                QMainWindow, QDialog { background-color: #f5f5f7; }
                QLabel { color: #1d1d1f; font-size: 14px; font-weight: bold; }
                QPushButton { min-width: 80px; min-height: 32px; border-radius: 5px; background-color: #1976d2; color: #ffffff; font-weight: bold; }
                QPushButton:hover { background-color: #1565c0; }
                QPushButton:pressed { background-color: #0050a0; }
                QLineEdit, QTextEdit, QComboBox { border: 1px solid #d2d2d7; border-radius: 4px; padding: 5px; background-color: #ffffff; color: #1d1d1f; }
                QLineEdit:focus, QTextEdit:focus, QComboBox:focus { border-color: #1976d2; outline: none; }
                QTabWidget::pane { border: 1px solid #e0e0e0; border-radius: 6px; }
                QTabBar::tab { background-color: #f5f5f7; border: 1px solid #d2d2d7; border-bottom: none; border-radius: 4px 4px 0 0; padding: 5px 10px; margin-right: 2px; color: #1d1d1f; }
                QTabBar::tab:selected { background-color: #ffffff; color: #1976d2; }
                QTableView { gridline-color: #d2d2d7; border: 1px solid #d2d2d7; border-radius: 4px; color: #1d1d1f; background-color: #f5f5f7; }
                QHeaderView::section { background-color: #f0f0f0; font-weight: bold; border: 1px solid #e0e0e0; color: #1d1d1f; }
                QGroupBox { font-weight: bold; border: 1px solid #e0e0e0; border-radius: 6px; margin-top: 10px; color: #1d1d1f; }
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }
                QTableWidget { alternate-background-color: #f5f5f7; gridline-color: #e0e0e0; color: #1d1d1f; }
            """)

def main():
    app = QApplication(sys.argv)
    
    # 设置全局样式
    app.setStyle("Fusion")
    
    theme_watcher = ThemeWatcher(app)
    theme_watcher.apply_theme()  # 启动时立即应用一次
    
    controller = MainController()
    controller.show_login_view()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
