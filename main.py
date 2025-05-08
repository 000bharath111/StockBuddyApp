import sys
import datetime
import yfinance as yf
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from login import StockBuddyApp_login
from live_stock_page import LiveStockPage

class StockDetailsPage(QWidget):
    def __init__(self, stock_name):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(f"📊 Detailed View for: {stock_name}")
        label.setFont(QFont("Arial", 22, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

class StockBuddyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StockBuddy AI Home Page")
        self.showMaximized()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # === TOP BAR ===
        topbar = QFrame()
        topbar.setFixedHeight(80)
        topbar.setStyleSheet("background-color: #2c3e50; color: white;")
        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(10, 0, 20, 0)

        logo = QLabel()
        logo.setPixmap(QPixmap("1.png").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setFixedSize(60, 60)

        app_name = QLabel("StockBuddy AI")
        app_name.setFont(QFont("Arial", 22, QFont.Bold))
        app_name.setStyleSheet("color: white")

        user_button = QPushButton()
        user_button.setIcon(QIcon("user.png"))
        user_button.setIconSize(QSize(40, 40))
        user_button.setFlat(True)
        user_button.setCursor(QCursor(Qt.PointingHandCursor))
        user_button.clicked.connect(self.login)

        topbar_layout.addWidget(logo)
        topbar_layout.addSpacing(10)
        topbar_layout.addWidget(app_name)
        topbar_layout.addStretch()
        topbar_layout.addWidget(user_button)

        # === MAIN BODY ===
        body_layout = QHBoxLayout()

        # === SIDEBAR ===
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: #1f2b3e; color: white;")
        sidebar.setFixedWidth(int(self.screen().size().width() * 0.12))
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(7)

        # Sidebar Title
        sidebar_title = QLabel("📁 Navigation")
        sidebar_title.setFont(QFont("Arial", 14, QFont.Bold))
        sidebar_title.setAlignment(Qt.AlignCenter)
        sidebar_title.setStyleSheet("color: #ecf0f1;")
        sidebar_layout.addWidget(sidebar_title)

        sidebar_layout.addSpacing(10)

        # === PAGES ===
        self.stack = QStackedWidget()

        self.home_page = QWidget()
        self.live_stock_page = LiveStockPage()
        self.prediction_page = QWidget()
        self.analysis_page = QWidget()
        self.planner_page = QWidget()
        self.alerts_page = QWidget()

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.live_stock_page)
        self.stack.addWidget(self.prediction_page)
        self.stack.addWidget(self.analysis_page)
        self.stack.addWidget(self.planner_page)
        self.stack.addWidget(self.alerts_page)

        pages = {
            "🏠 Home": 0,
            "📈 Live Stock": 1,
            "🔮 Prediction": 2,
            "📊 Analysis": 3,
            "🗓️ Planner": 4,
            "🚨 Alerts": 5
        }

        for text, index in pages.items():
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2c3e50;
                    color: white;
                    padding: 12px;
                    border-radius: 5px;
                    font-size: 14px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #34495e;
                }
            """)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda _, i=index: self.stack.setCurrentIndex(i))
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)

        # === HOME PAGE ===
        home_layout = QVBoxLayout(self.home_page)
        home_layout.setContentsMargins(50, 30, 50, 30)

        grow_logo = QLabel()
        grow_logo.setPixmap(QPixmap("growimg.png").scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        grow_logo.setFixedSize(50, 50)
        grow_logo.setAlignment(Qt.AlignCenter)

        welcome_label = QLabel("Welcome to StockBuddy AI!")
        welcome_label.setFont(QFont("Times New Roman", 24, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            color: black;
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #2193b0, stop:1 #6dd5ed);
            padding: 15px;
            border-radius: 10px;
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor("black"))
        shadow.setOffset(2, 2)
        welcome_label.setGraphicsEffect(shadow)
        home_layout.addWidget(welcome_label)

        title = QLabel("Top Gainers Today")
        title.setFont(QFont("Georgia", 26, QFont.Bold))
        title.setStyleSheet("color: #2c3e50")
        title.setAlignment(Qt.AlignCenter)

        title_layout = QHBoxLayout()
        title_layout.addWidget(grow_logo)
        title_layout.addSpacing(10)
        title_layout.addWidget(title)
        title_layout.addStretch()
        home_layout.addLayout(title_layout)
        home_layout.addSpacing(20)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QVBoxLayout()
        content_widget = QWidget()
        content_widget.setLayout(self.scroll_content)
        self.scroll.setWidget(content_widget)
        home_layout.addWidget(self.scroll)

        body_layout.addWidget(sidebar)
        body_layout.addWidget(self.stack)

        main_layout.addWidget(topbar)
        main_layout.addLayout(body_layout)

        self.update_stocks()
        timer = QTimer()
        timer.timeout.connect(self.update_stocks)
        timer.start(5 * 60 * 1000)

    def update_stocks(self):
        for i in reversed(range(self.scroll_content.count())):
            widget = self.scroll_content.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        stocks = self.get_top_increasing_stocks()
        for stock, change in stocks:
            stock_frame = QFrame()
            stock_frame.setStyleSheet("background-color: #9be7c4; border-radius: 10px;")
            stock_layout = QHBoxLayout(stock_frame)

            name_btn = QPushButton(stock)
            name_btn.setFont(QFont("Arial", 20, QFont.Bold))
            name_btn.setStyleSheet("color: #2e7d32; background: transparent;")
            name_btn.setCursor(QCursor(Qt.PointingHandCursor))
            name_btn.clicked.connect(lambda _, s=stock: self.show_details(s))

            change_label = QLabel(f"{change:.2f}%")
            change_label.setFont(QFont("Arial", 18))
            change_label.setStyleSheet("color: green; background-color: white; border-radius: 10px; padding: 8px;")

            stock_layout.addWidget(name_btn)
            stock_layout.addStretch()
            stock_layout.addWidget(change_label)
            self.scroll_content.addWidget(stock_frame)
            self.scroll_content.addSpacing(10)

    def show_details(self, stock_name):
        detail_page = StockDetailsPage(stock_name)
        self.stack.addWidget(detail_page)
        self.stack.setCurrentWidget(detail_page)

    def get_top_increasing_stocks(self):
        symbols = ["TCS.NS", "INFY.NS", "HDFCBANK.NS", "RELIANCE.NS", "SBIN.NS", "ICICIBANK.NS", "AXISBANK.NS"]
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=5)
        performance = []

        for symbol in symbols:
            try:
                data = yf.download(symbol, start=start, end=end, progress=False, auto_adjust=True)
                closes = data['Close'].dropna()
                if len(closes) >= 2:
                    last_close = float(closes.iloc[-1])
                    prev_close = float(closes.iloc[-2])
                    percent_change = ((last_close - prev_close) / prev_close) * 100
                    performance.append((symbol.replace(".NS", ""), percent_change))
            except:
                pass

        sorted_perf = sorted(performance, key=lambda x: x[1], reverse=True)
        return sorted_perf[:10]

    def login(self):
        self.login_window = StockBuddyApp_login()
        self.login_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StockBuddyApp()
    window.show()
    sys.exit(app.exec_())
