import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit,
    QFileDialog, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

from client import send_request

class HttpClientUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("手写 HTTP 客户端 UI")
        self.setMinimumSize(900, 600)

        # 设置背景颜色和字体
        self.setStyleSheet("""
            QWidget {
                background-color: #F4F7FB;
                font-family: 'Arial', sans-serif;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #B0B0B0;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QTextEdit {
                background-color: #EFEFEF;
                font-family: 'Courier New', monospace;
            }
        """)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 创建字体
        font = QFont("Arial", 16, QFont.Bold)  # 设置字体为 Arial，大小为 16，粗体

        # 请求方法标签
        label = QLabel("请求方法:")
        label.setFont(font)  # 设置字体

        # 请求方法选择框
        self.method_combo = QComboBox()
        self.method_combo.addItems(["GET", "POST", "HEAD"])

        # URL 输入框
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入 URL，如：http://example.com")

        # 文件选择按钮
        self.file_button = QPushButton("选择上传文件")
        self.file_button.setIcon(QIcon("file_icon.png"))  # 添加图标
        self.file_button.clicked.connect(self.select_file)
        self.file_path = ""

        # 发送按钮
        self.send_button = QPushButton("发送请求")
        self.send_button.setIcon(QIcon("send_icon.png"))  # 添加图标
        self.send_button.clicked.connect(self.on_send_button_click)

        # 布局
        top_layout = QHBoxLayout()
        top_layout.addWidget(label)  # 添加自定义字体的请求方法标签
        top_layout.addWidget(self.method_combo)
        top_layout.addWidget(self.url_input)
        top_layout.addWidget(self.file_button)
        top_layout.addWidget(self.send_button)

        self.layout.addLayout(top_layout)

        # 响应显示区域
        self.response_status = QLabel("状态行:")
        self.response_headers = QTextEdit()
        self.response_headers.setReadOnly(True)
        self.response_headers.setPlaceholderText("响应头...")

        self.response_body = QTextEdit()
        self.response_body.setReadOnly(True)
        self.response_body.setPlaceholderText("响应体...")

        self.layout.addWidget(self.response_status)
        self.layout.addWidget(QLabel("响应头："))
        self.layout.addWidget(self.response_headers, 2)
        self.layout.addWidget(QLabel("响应体："))
        self.layout.addWidget(self.response_body, 4)

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*.*)")
        if path:
            self.file_path = path
            self.file_button.setText(f"已选择: {path.split('/')[-1]}")

    def on_send_button_click(self):
        # 获取用户输入的 URL 和请求方法
        url = self.url_input.text()
        method = self.method_combo.currentText()  # 获取请求方法
        file_path = self.file_path if self.file_path else None  # 文件路径，若没有选择则为 None

        # 调用 send_request 函数
        try:
            body = send_request(url, method=method, file_path=file_path)  # 传递参数给 send_request
            self.response_body.setPlainText(body if body else "无返回内容")
        except Exception as e:
            self.response_body.setPlainText(f"请求失败: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HttpClientUI()
    window.show()
    sys.exit(app.exec_())
