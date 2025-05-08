from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect, QFrame, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
import random  # This simulates real-time data for now

class StockDetailsPage(QWidget):
    def __init__(self, stock_name="Tesla Inc", stock_symbol="TSLA"):
        super().__init__()

        self.stock_name_text = stock_name
        self.stock_symbol = stock_symbol
        self.setWindowTitle(f"{stock_name} - {stock_symbol} Details")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("background-color: #f5f5f5;")

        main_layout = QVBoxLayout()

        # Header (Stock Name, Price, Change)
        header_layout = QHBoxLayout()
        self.stock_name_label = QLabel(f"{stock_name} - {stock_symbol}")
        self.stock_name_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #333;")
        self.stock_price_label = QLabel()
        self.stock_price_label.setStyleSheet("font-size: 24px;")
        self.stock_change_label = QLabel()
        self.stock_change_label.setStyleSheet("font-size: 20px;")
        header_layout.addWidget(self.stock_name_label)
        header_layout.addWidget(self.stock_price_label)
        header_layout.addWidget(self.stock_change_label)
        main_layout.addLayout(header_layout)

        # Key Metrics
        metrics_layout = QHBoxLayout()
        self.pe_ratio = QLabel()
        self.eps = QLabel()
        self.market_cap = QLabel()
        self.high_low = QLabel()
        for lbl in [self.pe_ratio, self.eps, self.market_cap, self.high_low]:
            lbl.setStyleSheet("font-size: 16px; color: #555;")
            metrics_layout.addWidget(lbl)
        main_layout.addLayout(metrics_layout)

        # Graph Placeholder
        self.graph_placeholder = QLabel("📈 Real-Time Stock Graph (Coming soon)")
        self.graph_placeholder.setStyleSheet("font-size: 16px; color: gray;")
        main_layout.addWidget(self.graph_placeholder)

        # Company Overview
        overview = self.create_box("Company Overview", 
            f"{stock_name} is a tech company focused on future innovation in energy and transport.")
        main_layout.addWidget(overview)

        # Historical Data
        historical = self.create_box("Historical Data (Past Month)",
            "Price: $600 - $670\nVolume: 50M - 100M")
        main_layout.addWidget(historical)

        # News
        news = self.create_box("Recent News", 
            f"1. {stock_name} hits a new milestone.\n2. Analysts predict strong Q2 growth.\n3. New products expected.")
        main_layout.addWidget(news)

        # Apply shadow
        for widget in [overview, historical, news]:
            self.apply_shadow_effect(widget)

        # Scroll Area
        scroll_area = QScrollArea()
        content = QWidget()
        content.setLayout(main_layout)
        scroll_area.setWidget(content)
        scroll_area.setWidgetResizable(True)

        final_layout = QVBoxLayout()
        final_layout.addWidget(scroll_area)
        self.setLayout(final_layout)

        # Fetch and display dynamic data
        self.load_stock_data()

    def create_box(self, title, content):
        box = QFrame()
        box.setStyleSheet("border: 1px solid #ddd; padding: 10px; background-color: #fff;")
        layout = QVBoxLayout()
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-weight: bold; font-size: 16px;")
        content_lbl = QLabel(content)
        content_lbl.setWordWrap(True)
        layout.addWidget(title_lbl)
        layout.addWidget(content_lbl)
        box.setLayout(layout)
        return box

    def load_stock_data(self):
        # Simulated values — replace with real API fetch logic
        price = round(random.uniform(600, 700), 2)
        change_percent = round(random.uniform(-3, 3), 2)
        color = "green" if change_percent >= 0 else "red"

        self.stock_price_label.setText(f"Price: ${price}")
        self.stock_price_label.setStyleSheet(f"font-size: 24px; color: {color};")

        self.stock_change_label.setText(f"{'+' if change_percent >= 0 else ''}{change_percent}%")
        self.stock_change_label.setStyleSheet(f"font-size: 20px; color: {color};")

        self.pe_ratio.setText(f"P/E Ratio: {random.randint(10, 30)}")
        self.eps.setText(f"EPS: {round(random.uniform(2.0, 10.0), 2)}")
        self.market_cap.setText(f"Market Cap: ${random.randint(50, 150)}B")
        self.high_low.setText(f"Day High: ${price + random.randint(1, 5)} / Low: ${price - random.randint(1, 5)}")

    def apply_shadow_effect(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 0)
        widget.setGraphicsEffect(shadow)

# Run standalone test
if __name__ == "__main__":
    app = QApplication([])
    win = StockDetailsPage("Infosys Ltd", "INFY")
    win.show()
    app.exec_()
