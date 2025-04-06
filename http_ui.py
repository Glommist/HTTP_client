import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit,
    QFileDialog, QComboBox, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

from client import send_request

class HttpClientUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTTP 客户端")
        self.setMinimumSize(900, 600)

        yahei_font = QFont("Microsoft YaHei", 10)
        title_font = QFont("Microsoft YaHei", 10, QFont.Bold)
        self.setFont(yahei_font)

        self.setStyleSheet("""
            QWidget {
                background-color: #F4F7FB;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #B0B0B0;
                padding: 8px;
                border-radius: 5px;
                font-family: 'Microsoft YaHei';
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Microsoft YaHei';
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                color: #333333;
            }
            QTextEdit {
                background-color: #EFEFEF;
                font-family: 'Microsoft YaHei';
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #a0a0a0;
                border-radius: 10px;
                padding: 5px 30px 5px 10px;
                font-size: 16px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 24px;
                border-left: 1px solid #c0c0c0;
            }
            QComboBox::down-arrow {
                image: url(ui/picture/Arrow-down.svg);
                width: 12px;
                height: 12px;
            }
            QComboBox:hover {
                border: 1px solid #4CAF50;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #a0a0a0;
                selection-background-color: #cdeccc;
                background: white;
            }
        """)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 请求方法标签
        label = QLabel("请求方法:")
        label.setFont(title_font)
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 请求方法选择框
        self.method_combo = QComboBox()
        self.method_combo.setFont(yahei_font)
        self.method_combo.addItems(["GET", "POST", "HEAD"])
        self.method_combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # URL 输入框（可伸缩）
        self.url_input = QLineEdit()
        self.url_input.setFont(yahei_font)
        self.url_input.setPlaceholderText("输入 URL，如：http://example.com")
        self.url_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 文件选择按钮
        self.file_button = QPushButton("选择上传文件")
        self.file_button.setFont(yahei_font)
        self.file_button.setIcon(QIcon("file_icon.png"))
        self.file_button.clicked.connect(self.select_file)
        self.file_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 发送按钮
        self.send_button = QPushButton("发送请求")
        self.send_button.setFont(yahei_font)
        self.send_button.setIcon(QIcon("send_icon.png"))
        self.send_button.clicked.connect(self.on_send_button_click)
        self.send_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 顶部布局
        top_layout = QHBoxLayout()
        top_layout.addWidget(label)
        top_layout.addWidget(self.method_combo)
        top_layout.addWidget(self.url_input, stretch=1)
        top_layout.addWidget(self.file_button)
        top_layout.addWidget(self.send_button)
        self.layout.addLayout(top_layout)

        # 响应状态行
        self.response_status = QTextEdit()
        self.response_status.setReadOnly(True)
        self.response_status.setFont(yahei_font)
        self.response_status.setPlaceholderText("状态行...")
        self.response_status.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.response_status.setMaximumHeight(60)

        # 响应头标签 + 显示框
        headers_label = QLabel("响应头：")
        headers_label.setFont(title_font)

        self.response_headers = QTextEdit()
        self.response_headers.setReadOnly(True)
        self.response_headers.setFont(yahei_font)
        self.response_headers.setPlaceholderText("响应头...")
        self.response_headers.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.response_headers.setMaximumHeight(150)

        # 响应体标签 + 显示框
        body_label = QLabel("响应体：")
        body_label.setFont(title_font)

        self.response_body = QTextEdit()
        self.response_body.setReadOnly(True)
        self.response_body.setFont(yahei_font)
        self.response_body.setPlaceholderText("响应体...")
        self.response_body.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 添加响应区域
        self.layout.addWidget(self.response_status)
        self.layout.addWidget(headers_label)
        self.layout.addWidget(self.response_headers)
        self.layout.addWidget(body_label)
        self.layout.addWidget(self.response_body)

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*.*)")
        if path:
            self.file_path = path
            self.file_button.setText(f"已选择: {path.split('/')[-1]}")
        else:
            self.file_path = None

    def on_send_button_click(self):
        url = self.url_input.text()
        method = self.method_combo.currentText()
        file_path = getattr(self, 'file_path', None)

        try:
            status_line, headers, body = send_request(url, method=method, file_path=file_path)
            self.response_status.setPlainText(str(status_line) if status_line else "无返回内容")
            self.response_headers.setPlainText(str(headers) if headers else "无返回内容")
            self.response_body.setPlainText(str(body) if body else "无返回内容")
        except Exception as e:
            self.response_body.setPlainText(f"请求失败: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HttpClientUI()
    window.show()
    sys.exit(app.exec_())
