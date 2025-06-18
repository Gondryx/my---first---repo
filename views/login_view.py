from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QHBoxLayout, QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class LoginView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()
        
    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('社交媒体营销分析系统 - 登录')
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # 创建标题
        title_label = QLabel('社交媒体营销分析系统')
        title_font = QFont('Arial', 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)
        
        # 创建表单容器
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(15)
        
        # 用户名
        username_layout = QHBoxLayout()
        username_label = QLabel('用户名:')
        username_label.setFixedWidth(80)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('请输入用户名')
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        form_layout.addLayout(username_layout)
        
        # 密码
        password_layout = QHBoxLayout()
        password_label = QLabel('密码:')
        password_label.setFixedWidth(80)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('请输入密码')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        form_layout.addLayout(password_layout)
        
        # 添加表单容器到主布局
        main_layout.addWidget(form_container)
        
        # 按钮布局
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # 登录按钮
        self.login_button = QPushButton('登录')
        self.login_button.setMinimumHeight(40)
        self.login_button.clicked.connect(self.handle_login)
        buttons_layout.addWidget(self.login_button)
        
        # 注册按钮
        self.register_button = QPushButton('注册')
        self.register_button.setMinimumHeight(40)
        self.register_button.clicked.connect(self.handle_register)
        buttons_layout.addWidget(self.register_button)
        
        main_layout.addLayout(buttons_layout)
        
        # 设置布局
        self.setLayout(main_layout)
        
    def handle_login(self):
        """处理登录按钮点击事件"""
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, '登录失败', '用户名和密码不能为空')
            return
            
        # 调用控制器的登录方法
        success, message = self.controller.login(username, password)
        
        if success:
            QMessageBox.information(self, '登录成功', '欢迎回来！')
            self.controller.show_main_view()
        else:
            QMessageBox.warning(self, '登录失败', message)
            
    def handle_register(self):
        """处理注册按钮点击事件"""
        self.controller.show_register_view()    