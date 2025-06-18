from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QHBoxLayout, QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class RegisterView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()
        
    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('社交媒体营销分析系统 - 注册')
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # 创建标题
        title_label = QLabel('社交媒体营销分析系统 - 注册')
        title_font = QFont('Arial', 20, QFont.Weight.Bold)
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
        
        # 邮箱
        email_layout = QHBoxLayout()
        email_label = QLabel('邮箱:')
        email_label.setFixedWidth(80)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('请输入邮箱')
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        form_layout.addLayout(email_layout)
        
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
        
        # 确认密码
        confirm_layout = QHBoxLayout()
        confirm_label = QLabel('确认密码:')
        confirm_label.setFixedWidth(80)
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText('请再次输入密码')
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        confirm_layout.addWidget(confirm_label)
        confirm_layout.addWidget(self.confirm_input)
        form_layout.addLayout(confirm_layout)
        
        # 添加表单容器到主布局
        main_layout.addWidget(form_container)
        
        # 按钮布局
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # 注册按钮
        self.register_button = QPushButton('注册')
        self.register_button.setMinimumHeight(40)
        self.register_button.clicked.connect(self.handle_register)
        buttons_layout.addWidget(self.register_button)
        
        # 返回按钮
        self.back_button = QPushButton('返回')
        self.back_button.setMinimumHeight(40)
        self.back_button.clicked.connect(self.handle_back)
        buttons_layout.addWidget(self.back_button)
        
        main_layout.addLayout(buttons_layout)
        
        # 设置布局
        self.setLayout(main_layout)
        
    def handle_register(self):
        """处理注册按钮点击事件"""
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_input.text()
        
        if not username or not email or not password or not confirm_password:
            QMessageBox.warning(self, '注册失败', '所有字段都不能为空')
            return
            
        if password != confirm_password:
            QMessageBox.warning(self, '注册失败', '两次输入的密码不一致')
            return
            
        # 调用控制器的注册方法
        success, message = self.controller.register(username, email, password)
        
        if success:
            QMessageBox.information(self, '注册成功', '注册成功，请登录')
            self.controller.show_login_view()
        else:
            QMessageBox.warning(self, '注册失败', message)
            
    def handle_back(self):
        """处理返回按钮点击事件"""
        self.controller.show_login_view()    