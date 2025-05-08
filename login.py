import sys
import os
import pickle
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QWidget, QDialog, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont, QCursor, QIcon
from PyQt5.QtCore import Qt, QSize

# Google Auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


class StockBuddyApp_login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login to StockBuddy AI")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")
        self.logged_in = False
        self.user_email = ""
        self.check_existing_login()
        self.init_ui()

    def check_existing_login(self):
        SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if creds and creds.valid:
            try:
                service = build('oauth2', 'v2', credentials=creds)
                user_info = service.userinfo().get().execute()
                self.logged_in = True
                self.user_email = user_info.get('email', '')
            except Exception as e:
                print("Auto-login failed:", e)
                self.logged_in = False

    def init_ui(self):
        layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to StockBuddy AI")
        welcome_label.setFont(QFont("Comic Sans MS", 55, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("color: #d210d6;")

        status_label = QLabel()
        status_label.setFont(QFont("Arial", 12))
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet("color: #757575;")

        login_btn = QPushButton()
        login_btn.setCursor(QCursor(Qt.PointingHandCursor))
        login_btn.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            border: none;
        """)
        logo_label = QLabel()
        logo_icon = QIcon("google_img.png")  # Use full path if necessary

        if logo_icon.isNull():
            # If image not found, display fallback text
            print("Image not found!")
            logo_label.setText("Google")
        else:
            logo_label.setPixmap(logo_icon.pixmap(550, 850))  # You can scale the image here

        logo_label.setAlignment(Qt.AlignCenter)

        '''if self.logged_in:
            login_btn.setText("You are already logged in")
            login_btn.setEnabled(False)
            status_label.setText(f"Logged in as: {self.user_email}")
            login_btn.setStyleSheet("""
                font-size: 16px;
                padding: 10px;
                background-color: #757575;
                color: white;
                border-radius: 5px;
                border: none;
            """)
            login_btn.setCursor(QCursor(Qt.ForbiddenCursor))
            status_label.setStyleSheet("color: Yello;")
            status_label.setFont(QFont("Tahoma", 20))
            status_label.setAlignment(Qt.AlignCenter)
            
            # Add logout button
            logout_btn = QPushButton("Log out")
            logout_btn.setStyleSheet("""
                font-size: 16px;
                padding: 10px;
                background-color: #f44336;
                color: white;
                border-radius: 5px;
                border: none;
            """)
            logout_btn.clicked.connect(self.logout)
            layout.addWidget(logout_btn)
        else:
            login_btn.setText("Login with Google")
            login_btn.clicked.connect(self.show_login_dialog)'''

        # Add login button and status
        layout.addWidget(welcome_label)
        layout.addSpacing(10)
        layout.addWidget(logo_label)
        layout.addSpacing(20)
        layout.addWidget(status_label)
        layout.addWidget(login_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        if self.logged_in:
            login_btn.setText("You are already logged in")
            login_btn.setEnabled(False)
            status_label.setText(f"Logged in as: {self.user_email}")
            login_btn.setStyleSheet("""
                font-size: 16px;
                padding: 10px;
                background-color: #757575;
                color: white;
                border-radius: 5px;
                border: none;
            """)
            login_btn.setCursor(QCursor(Qt.ForbiddenCursor))
            status_label.setStyleSheet("color: Yello;")
            status_label.setFont(QFont("Tahoma", 20))
            status_label.setAlignment(Qt.AlignCenter)
            
            # Add logout button
            logout_btn = QPushButton("Log out")
            logout_btn.setStyleSheet("""
                font-size: 16px;
                padding: 10px;
                background-color: #f44336;
                color: white;
                border-radius: 5px;
                border: none;
            """)
            logout_btn.clicked.connect(self.logout)
            layout.addWidget(logout_btn)
        else:
            login_btn.setText("Login with Google")
            login_btn.clicked.connect(self.show_login_dialog)

    def show_login_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Google Login")
        dialog.setFixedSize(400, 300)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(30, 30, 30, 30)

        logo_label = QLabel()

        # Using QIcon to display the image
        logo_icon = QIcon("google_img.png")  # Use full path if necessary

        if logo_icon.isNull():
            # If image not found, display fallback text
            print("Image not found!")
            logo_label.setText("Google")
        else:
            logo_label.setPixmap(logo_icon.pixmap(100, 100))  # You can scale the image here

        logo_label.setAlignment(Qt.AlignCenter)

        title = QLabel("Sign in to StockBuddy AI")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #4CAF50;")

        info = QLabel("Use your Google account to log in.")
        info.setFont(QFont("Arial", 11))
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: #757575;")

        signin_btn = QPushButton("Sign in with Google")
        signin_btn.setCursor(QCursor(Qt.PointingHandCursor))
        signin_btn.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            background-color: #4285F4;
            color: white;
            border-radius: 5px;
            border: none;
        """)

        def google_login():
            try:
                SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
                creds = None

                if os.path.exists('token.pickle'):
                    with open('token.pickle', 'rb') as token:
                        creds = pickle.load(token)

                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
                        creds = flow.run_local_server(port=0)

                    with open('token.pickle', 'wb') as token:
                        pickle.dump(creds, token)

                service = build('oauth2', 'v2', credentials=creds)
                user_info = service.userinfo().get().execute()
                self.logged_in = True
                self.user_email = user_info.get('email', '')

                QMessageBox.information(dialog, "Success", f"Logged in as {self.user_email}")
                dialog.accept()
                self.init_ui()  # Refresh UI after login

            except Exception as e:
                QMessageBox.warning(dialog, "Login Failed", f"Error: {e}")

        signin_btn.clicked.connect(google_login)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))

        cancel_btn.clicked.connect(dialog.reject)
        cancel_btn.setStyleSheet("""
            font-size: 20px;
            padding: 12px;
            color: #000000;
            background-color: transparent;
            border: none;
        """)

        layout.addWidget(logo_label)
        layout.addSpacing(10)
        layout.addWidget(title)
        layout.addWidget(info)
        layout.addSpacing(20)
        layout.addWidget(signin_btn)
        layout.addSpacing(20)
        layout.addWidget(cancel_btn)

        dialog.exec_()

    def logout(self):
        # Remove the token and log the user out
        if os.path.exists('token.pickle'):
            os.remove('token.pickle')
        
        self.logged_in = False
        self.user_email = ""
        self.init_ui()  # Refresh the UI
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockBuddyApp_login()
    window.show()
    sys.exit(app.exec_())
'''