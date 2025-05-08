from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QComboBox, QMessageBox, QHBoxLayout, QStackedWidget, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
import yfinance as yf
import sys
from stock_detial_page import StockDetailsPage  # Import the StockDetailWindow from the stock_detail_page file

class LiveStockPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f7;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QTableWidget {
                border-radius: 10px;
                background-color: white;
                border: 1px solid #ccc;
            }
            QTableWidget::item:hover {
                background-color: #f1f1f1;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: bold;
            }
        """)

        self.stack = QStackedWidget()
        self.trending_page = QWidget()
        self.investment_page = QWidget()

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #555; font-style: italic; margin-top: 8px;")

        self.init_trending_page()
        self.init_investment_page()

        self.stack.addWidget(self.trending_page)
        self.stack.addWidget(self.investment_page)

        toggle_btn_layout = QHBoxLayout()
        toggle_btn_layout.setSpacing(10)

        self.trending_btn = QPushButton("🔥 Trending")
        self.invest_btn = QPushButton("📈 Investment")

        for btn in [self.trending_btn, self.invest_btn]:
            btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.trending_btn.clicked.connect(lambda: self.switch_view(0))
        self.invest_btn.clicked.connect(lambda: self.switch_view(1))

        toggle_btn_layout.addWidget(self.trending_btn)
        toggle_btn_layout.addWidget(self.invest_btn)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        main_layout.addLayout(toggle_btn_layout)
        main_layout.addWidget(self.stack)
        main_layout.addWidget(self.status_label)

        self.switch_view(0)

    def switch_view(self, index):
        self.stack.setCurrentIndex(index)
        if index == 0:
            self.trending_btn.setStyleSheet("background-color: #2196F3; color: white;")
            self.invest_btn.setStyleSheet("background-color: #e0e0e0; color: #333;")
        else:
            self.invest_btn.setStyleSheet("background-color: #2196F3; color: white;")
            self.trending_btn.setStyleSheet("background-color: #e0e0e0; color: #333;")

    def init_trending_page(self):
        layout = QVBoxLayout()
        title = QLabel("🔥 Top Trending Stocks")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1976D2; margin-bottom: 10px;")
        layout.addWidget(title)

        self.trending_table = QTableWidget()
        self.trending_table.setColumnCount(4)
        self.trending_table.setHorizontalHeaderLabels(["Symbol", "Name", "Price", "Change %"])
        self.trending_table.horizontalHeader().setStretchLastSection(True)
        self.trending_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.trending_table.cellClicked.connect(self.trending_stock_clicked)

        layout.addWidget(self.trending_table)
        self.trending_page.setLayout(layout)
        self.load_trending_stocks()

    def init_investment_page(self):
        layout = QVBoxLayout()

        title = QLabel("📈 Stock Investment Research")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #388E3C; margin-bottom: 10px;")
        layout.addWidget(title)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter stock symbol (e.g., AAPL)")
        search_layout.addWidget(self.search_input)

        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_stock)
        search_layout.addWidget(self.search_btn)

        layout.addLayout(search_layout)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Symbol", "Name", "Price", "Change %"])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.cellClicked.connect(self.open_stock_details)
        layout.addWidget(self.result_table)

        self.investment_page.setLayout(layout)

    def trending_stock_clicked(self, row, col):
        symbol_item = self.trending_table.item(row, 0)
        if symbol_item:
            symbol = symbol_item.text()
            self.search_input.setText(symbol)
            self.switch_view(1)
            self.search_stock()

    def search_stock(self):
        symbol = self.search_input.text().strip()
        if not symbol:
            QMessageBox.warning(self, "Input Error", "Please enter a stock symbol.")
            return

        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            self.result_table.setRowCount(1)
            self.result_table.setItem(0, 0, QTableWidgetItem(symbol))
            self.result_table.setItem(0, 1, QTableWidgetItem(info.get("shortName", "N/A")))
            self.result_table.setItem(0, 2, QTableWidgetItem(str(info.get("regularMarketPrice", "N/A"))))
            self.result_table.setItem(0, 3, QTableWidgetItem(str(info.get("regularMarketChangePercent", "N/A")) + "%"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch data for {symbol}.\nError: {e}")

    def load_trending_stocks(self):
        trending_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]  # example trending
        self.trending_table.setRowCount(len(trending_symbols))

        for i, symbol in enumerate(trending_symbols):
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                self.trending_table.setItem(i, 0, QTableWidgetItem(symbol))
                self.trending_table.setItem(i, 1, QTableWidgetItem(info.get("shortName", "N/A")))
                self.trending_table.setItem(i, 2, QTableWidgetItem(str(info.get("regularMarketPrice", "N/A"))))
                self.trending_table.setItem(i, 3, QTableWidgetItem(str(info.get("regularMarketChangePercent", "N/A")) + "%"))
            except Exception as e:
                self.trending_table.setItem(i, 0, QTableWidgetItem(symbol))
                self.trending_table.setItem(i, 1, QTableWidgetItem("Error"))
                self.trending_table.setItem(i, 2, QTableWidgetItem("N/A"))
                self.trending_table.setItem(i, 3, QTableWidgetItem("N/A"))

    def open_stock_details(self, row, col):
        symbol_item = self.result_table.item(row, 0)
        if symbol_item:
            symbol = symbol_item.text()
            self.details_window = StockDetailsPage(symbol)
            self.details_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LiveStockPage()
    window.resize(800, 600)
    window.setWindowTitle("📊 StockBuddy AI")
    window.show()
    sys.exit(app.exec_())
