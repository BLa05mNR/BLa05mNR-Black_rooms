import sys
import requests
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QStackedWidget, QTableWidget,
                               QTableWidgetItem, QMessageBox, QComboBox, QDateEdit, QTimeEdit,
                               QTabWidget, QFormLayout, QGroupBox, QCheckBox, QSpinBox, QTextEdit, QDialogButtonBox,
                               QDialog)
from PySide6.QtCore import Qt, QDate, QTime, QTimer
from PySide6.QtGui import QPalette, QColor, QIntValidator

# Базовый URL вашего FastAPI сервера
BASE_URL = "http://127.0.0.1:8000"


class DarkTheme:
    @staticmethod
    def apply(app):
        app.setStyle("Fusion")
        dark_palette = QPalette()

        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        app.setPalette(dark_palette)
        app.setStyleSheet("""
            QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }
            QTabWidget::pane { border: 1px solid #444; }
            QTabBar::tab { background: #353535; color: white; padding: 8px; }
            QTabBar::tab:selected { background: #2a82da; color: black; }
            QGroupBox { border: 1px solid #444; margin-top: 10px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px; }
        """)


class ApiClient:
    @staticmethod
    def get_positions():
        try:
            response = requests.get(f"{BASE_URL}/positions/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching positions: {e}")
            return []

    @staticmethod
    def create_position(position_data):
        try:
            response = requests.post(f"{BASE_URL}/positions/", json=position_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating position: {e}")
            return None

    @staticmethod
    def update_position(position_id, position_data):
        try:
            response = requests.put(f"{BASE_URL}/positions/{position_id}", json=position_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating position: {e}")
            return None

    @staticmethod
    def delete_position(position_id):
        try:
            response = requests.delete(f"{BASE_URL}/positions/{position_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting position: {e}")
            return False

    @staticmethod
    def get_clients():
        try:
            response = requests.get(f"{BASE_URL}/clients/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching clients: {e}")
            return []

    @staticmethod
    def get_client(client_id):
        try:
            response = requests.get(f"{BASE_URL}/clients/{client_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching client: {e}")
            return None

    @staticmethod
    def register_client(client_data):
        try:
            response = requests.post(f"{BASE_URL}/clients/register/", json=client_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error registering client: {e}")
            return None

    @staticmethod
    def login_client(login_data):
        try:
            response = requests.post(f"{BASE_URL}/clients/login/", json=login_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error logging in client: {e}")
            return None

    @staticmethod
    def update_client(client_id, client_data):
        try:
            response = requests.put(
                f"{BASE_URL}/clients/{client_id}",
                json=client_data
            )

            if response.status_code == 422:  # Ошибка валидации
                errors = response.json().get("detail", "Неизвестная ошибка валидации")
                print(f"Validation errors: {errors}")
                return None

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response:
                try:
                    error_msg = e.response.json().get("detail", error_msg)
                except:
                    pass
            print(f"Error updating client: {error_msg}")
            return None

    @staticmethod
    def delete_client(client_id):
        try:
            response = requests.delete(f"{BASE_URL}/clients/{client_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting client: {e}")
            return False

    @staticmethod
    def change_password(client_id, old_password, new_password):
        try:
            data = {
                "current_password": old_password,  # возможно, нужно "current_password" вместо "old_password"
                "new_password": new_password
            }

            response = requests.post(
                f"{BASE_URL}/auth/change-password",
                json=data
            )

            # Проверяем успешный ответ
            if response.status_code == 200:
                return response.json()

            # Обрабатываем ошибки
            error_detail = response.json().get("detail", "Неизвестная ошибка")
            print(f"Password change failed: {error_detail}")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    @staticmethod
    def get_employees():
        try:
            response = requests.get(f"{BASE_URL}/employees/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching employees: {e}")
            return []

    @staticmethod
    def create_employee(employee_data):
        try:
            response = requests.post(f"{BASE_URL}/employees/", json=employee_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating employee: {e}")
            return None

    @staticmethod
    def update_employee(employee_id, employee_data):
        try:
            response = requests.put(f"{BASE_URL}/employees/{employee_id}", json=employee_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating employee: {e}")
            return None

    @staticmethod
    def delete_employee(employee_id):
        try:
            response = requests.delete(f"{BASE_URL}/employees/{employee_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting employee: {e}")
            return False

    @staticmethod
    def get_quests():
        try:
            response = requests.get(f"{BASE_URL}/quests/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching quests: {e}")
            return []

    @staticmethod
    def create_quest(quest_data):
        try:
            response = requests.post(f"{BASE_URL}/quests/", json=quest_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating quest: {e}")
            return None

    @staticmethod
    def update_quest(quest_id, quest_data):
        try:
            response = requests.put(f"{BASE_URL}/quests/{quest_id}", json=quest_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating quest: {e}")
            return None

    @staticmethod
    def delete_quest(quest_id):
        try:
            response = requests.delete(f"{BASE_URL}/quests/{quest_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting quest: {e}")
            return False

    @staticmethod
    def get_rooms():
        try:
            response = requests.get(f"{BASE_URL}/rooms/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching rooms: {e}")
            return []

    @staticmethod
    def create_room(room_data):
        try:
            response = requests.post(f"{BASE_URL}/rooms/", json=room_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating room: {e}")
            return None

    @staticmethod
    def update_room(room_id, room_data):
        try:
            response = requests.put(f"{BASE_URL}/rooms/{room_id}", json=room_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating room: {e}")
            return None

    @staticmethod
    def delete_room(room_id):
        try:
            response = requests.delete(f"{BASE_URL}/rooms/{room_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting room: {e}")
            return False

    @staticmethod
    def get_schedules():
        try:
            response = requests.get(f"{BASE_URL}/schedules/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching schedules: {e}")
            return []

    @staticmethod
    def create_schedule(schedule_data):
        try:
            response = requests.post(f"{BASE_URL}/schedules/", json=schedule_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating schedule: {e}")
            return None

    @staticmethod
    def update_schedule(schedule_id, schedule_data):
        try:
            response = requests.put(f"{BASE_URL}/schedules/{schedule_id}", json=schedule_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating schedule: {e}")
            return None

    @staticmethod
    def delete_schedule(schedule_id):
        try:
            response = requests.delete(f"{BASE_URL}/schedules/{schedule_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting schedule: {e}")
            return False

    @staticmethod
    def get_bookings():
        try:
            response = requests.get(f"{BASE_URL}/bookings/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching bookings: {e}")
            return []

    @staticmethod
    def create_booking(booking_data):
        try:
            response = requests.post(f"{BASE_URL}/bookings/", json=booking_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating booking: {e}")
            return None

    @staticmethod
    def update_booking(booking_id, booking_data):
        try:
            response = requests.put(f"{BASE_URL}/bookings/{booking_id}", json=booking_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating booking: {e}")
            return None

    @staticmethod
    def delete_booking(booking_id):
        try:
            response = requests.delete(f"{BASE_URL}/bookings/{booking_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting booking: {e}")
            return False

    @staticmethod
    def get_payments():
        try:
            response = requests.get(f"{BASE_URL}/payments/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching payments: {e}")
            return []

    @staticmethod
    def create_payment(payment_data):
        try:
            response = requests.post(f"{BASE_URL}/payments/", json=payment_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating payment: {e}")
            return None

    @staticmethod
    def update_payment(payment_id, payment_data):
        try:
            response = requests.put(f"{BASE_URL}/payments/{payment_id}", json=payment_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating payment: {e}")
            return None

    @staticmethod
    def delete_payment(payment_id):
        try:
            response = requests.delete(f"{BASE_URL}/payments/{payment_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting payment: {e}")
            return False

    @staticmethod
    def get_reviews():
        try:
            response = requests.get(f"{BASE_URL}/reviews/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching reviews: {e}")
            return []

    @staticmethod
    def create_review(review_data):
        try:
            response = requests.post(f"{BASE_URL}/reviews/", json=review_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating review: {e}")
            return None

    @staticmethod
    def update_review(review_id, review_data):
        try:
            response = requests.put(f"{BASE_URL}/reviews/{review_id}", json=review_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating review: {e}")
            return None

    @staticmethod
    def delete_review(review_id):
        try:
            response = requests.delete(f"{BASE_URL}/reviews/{review_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting review: {e}")
            return False

    @staticmethod
    def get_services():
        try:
            response = requests.get(f"{BASE_URL}/services/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching services: {e}")
            return []

    @staticmethod
    def create_service(service_data):
        try:
            response = requests.post(f"{BASE_URL}/services/", json=service_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating service: {e}")
            return None

    @staticmethod
    def update_service(service_id, service_data):
        try:
            response = requests.put(f"{BASE_URL}/services/{service_id}", json=service_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating service: {e}")
            return None

    @staticmethod
    def delete_service(service_id):
        try:
            response = requests.delete(f"{BASE_URL}/services/{service_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting service: {e}")
            return False

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Black Rooms - Авторизация")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.title_label = QLabel("Black Rooms")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2a82da;")

        self.login_label = QLabel("Логин:")
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите ваш логин")

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите ваш пароль")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Войти")
        self.login_button.setStyleSheet("background-color: #2a82da; padding: 8px;")

        self.register_button = QPushButton("Регистрация")
        self.register_button.setStyleSheet("padding: 8px;")

        layout.addWidget(self.title_label)
        layout.addSpacing(20)
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addSpacing(20)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)


class ClientAccountWindow(QWidget):
    def __init__(self, client_id, parent=None):
        super().__init__(parent)
        self.client_id = client_id
        self.setup_ui()
        self.load_client_data()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Мой аккаунт")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        form_layout = QFormLayout()

        # Добавляем поле для логина
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите ваш логин")

        self.full_name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.birth_date_input = QDateEdit()
        self.birth_date_input.setCalendarPopup(True)
        self.birth_date_input.setDate(QDate.currentDate())

        # Добавляем поле логина в форму
        form_layout.addRow("Логин:", self.login_input)
        form_layout.addRow("ФИО:", self.full_name_input)
        form_layout.addRow("Телефон:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Дата рождения:", self.birth_date_input)

        password_group = QGroupBox("Смена пароля")
        password_layout = QFormLayout()

        self.current_password_input = QLineEdit()
        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        password_layout.addRow("Текущий пароль:", self.current_password_input)
        password_layout.addRow("Новый пароль:", self.new_password_input)
        password_layout.addRow("Подтвердите пароль:", self.confirm_password_input)

        password_group.setLayout(password_layout)

        self.save_button = QPushButton("Сохранить изменения")
        self.save_button.setStyleSheet("background-color: #2a82da; padding: 8px;")
        self.save_button.clicked.connect(self.save_client_data)

        self.delete_button = QPushButton("Удалить аккаунт")
        self.delete_button.setStyleSheet("background-color: #d9534f; padding: 8px;")
        self.delete_button.clicked.connect(self.delete_client_account)

        layout.addWidget(self.title_label)
        layout.addLayout(form_layout)
        layout.addWidget(password_group)
        layout.addWidget(self.save_button)
        layout.addWidget(self.delete_button)
        layout.addStretch()

        self.setLayout(layout)

    def load_client_data(self):
        if not self.client_id:
            return

        client_data = ApiClient.get_client(self.client_id)
        if client_data:
            self.login_input.setText(client_data.get("login", ""))
            self.full_name_input.setText(client_data.get("full_name", ""))
            self.phone_input.setText(client_data.get("phone", ""))
            self.email_input.setText(client_data.get("email", ""))

            birth_date = client_data.get("birth_date")
            if birth_date:
                year, month, day = map(int, birth_date.split("-"))
                self.birth_date_input.setDate(QDate(year, month, day))

    def save_client_data(self):
        if not self.client_id:
            return

        # Проверка валидации
        errors = self.validate_inputs()
        if errors:
            QMessageBox.warning(self, "Ошибка", "\n".join(errors))
            return

        # Подготовка данных для отправки
        client_data = {
            "login": self.login_input.text(),
            "full_name": self.full_name_input.text(),
            "phone": self.phone_input.text(),
            "email": self.email_input.text(),
            "birth_date": self.birth_date_input.date().toString("yyyy-MM-dd"),
            "password": ""  # Будет заполнено, если меняется пароль
        }

        # Обработка смены пароля (остаётся без изменений)
        current_password = self.current_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if current_password or new_password or confirm_password:
            if not (current_password and new_password and confirm_password):
                QMessageBox.warning(self, "Ошибка", "Для смены пароля заполните все поля")
                return

            if new_password != confirm_password:
                QMessageBox.warning(self, "Ошибка", "Новый пароль и подтверждение не совпадают")
                return

            client_data["password"] = new_password

        # Отправка данных
        result = ApiClient.update_client(self.client_id, client_data)

        if result:
            QMessageBox.information(self, "Успех", "Данные успешно обновлены!")
            self.current_password_input.clear()
            self.new_password_input.clear()
            self.confirm_password_input.clear()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось обновить данные")

    def validate_inputs(self):
        errors = []

        if not self.login_input.text().strip():
            errors.append("Логин обязателен для заполнения")
        elif len(self.login_input.text()) < 4:
            errors.append("Логин должен содержать минимум 4 символа")

        if not self.full_name_input.text().strip():
            errors.append("ФИО обязательно для заполнения")

        if self.new_password_input.text() and len(self.new_password_input.text()) < 6:
            errors.append("Пароль должен содержать минимум 6 символов")

        return errors

    def delete_client_account(self):
        if not self.client_id:
            return

        reply = QMessageBox.question(
            self, "Подтверждение",
            "Вы уверены, что хотите удалить свой аккаунт? Это действие нельзя отменить.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = ApiClient.delete_client(self.client_id)
            if success:
                QMessageBox.information(self, "Успех", "Аккаунт успешно удален")
                self.parent().logout()  # Возвращаемся к окну входа
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить аккаунт")

class QuestListWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.title_label = QLabel("Доступные квесты")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск квестов...")

        self.quests_table = QTableWidget()
        self.quests_table.setColumnCount(5)
        self.quests_table.setHorizontalHeaderLabels(["Название", "Описание", "Сложность", "Длительность", "Цена"])
        self.quests_table.horizontalHeader().setStretchLastSection(True)

        self.book_button = QPushButton("Забронировать")
        self.book_button.setStyleSheet("background-color: #2a82da; padding: 8px;")

        self.search_input.textChanged.connect(self.filter_quests)

        layout.addWidget(self.title_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.quests_table)
        layout.addWidget(self.book_button)

        self.setLayout(layout)

        # Загружаем квесты с сервера
        self.load_quests()

    def filter_quests(self):
        search_text = self.search_input.text().lower()
        quests = ApiClient.get_quests()

        if not search_text:
            self.load_quests()
            return

        filtered = [q for q in quests if
                    search_text in q["title"].lower() or
                    search_text in q["description"].lower() or
                    search_text in str(q["difficulty"]) or
                    search_text in str(q["duration"]) or
                    search_text in str(q["price"])]

        self.quests_table.setRowCount(len(filtered))
        for row, quest in enumerate(filtered):
            self.quests_table.setItem(row, 0, QTableWidgetItem(quest["title"]))
            self.quests_table.setItem(row, 1, QTableWidgetItem(quest["description"]))
            self.quests_table.setItem(row, 2, QTableWidgetItem(str(quest["difficulty"])))
            self.quests_table.setItem(row, 3, QTableWidgetItem(f"{quest['duration']} мин"))
            self.quests_table.setItem(row, 4, QTableWidgetItem(f"{quest['price']} руб"))

    def load_quests(self):
        quests = ApiClient.get_quests()

        self.quests_table.setRowCount(len(quests))
        for row, quest in enumerate(quests):
            self.quests_table.setItem(row, 0, QTableWidgetItem(quest["title"]))
            self.quests_table.setItem(row, 1, QTableWidgetItem(quest["description"]))
            self.quests_table.setItem(row, 2, QTableWidgetItem(str(quest["difficulty"])))
            self.quests_table.setItem(row, 3, QTableWidgetItem(f"{quest['duration']} мин"))
            self.quests_table.setItem(row, 4, QTableWidgetItem(f"{quest['price']} руб"))

        # Автоматическое подстраивание ширины столбцов
        self.quests_table.resizeColumnsToContents()
        # Добавляем немного отступа
        self.quests_table.horizontalHeader().setStretchLastSection(True)


class BookingWindow(QWidget):
    def __init__(self, client_id, parent=None):
        super().__init__(parent)
        self.client_id = client_id
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Бронирование квеста")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        form_layout = QFormLayout()

        # Выбор квеста
        self.quest_combo = QComboBox()
        quests = ApiClient.get_quests()
        for quest in quests:
            self.quest_combo.addItem(quest["title"], quest["quest_id"])

        # Выбор комнаты
        self.room_combo = QComboBox()
        rooms = ApiClient.get_rooms()
        for room in rooms:
            if room["is_available"]:
                self.room_combo.addItem(f"{room['title']} ({room['type']}, до {room['capacity']} чел.)",
                                        room["room_id"])

        # Выбор даты и времени
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setMinimumDate(QDate.currentDate())

        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime(18, 0))
        self.time_input.setDisplayFormat("HH:mm")

        # Количество участников
        self.participants_input = QSpinBox()
        self.participants_input.setRange(1, 10)
        self.participants_input.setValue(2)

        # Дополнительные услуги
        self.services_group = QGroupBox("Дополнительные услуги")
        services_layout = QVBoxLayout()

        services = ApiClient.get_services()
        self.service_checkboxes = []
        for service in services:
            cb = QCheckBox(f"{service['title']} (+{service['price']} руб)")
            cb.service_id = service["service_id"]
            self.service_checkboxes.append(cb)
            services_layout.addWidget(cb)

        self.services_group.setLayout(services_layout)

        # Кнопка подтверждения
        self.confirm_button = QPushButton("Подтвердить бронирование")
        self.confirm_button.setStyleSheet("background-color: #2a82da; padding: 8px;")
        self.confirm_button.clicked.connect(self.create_booking)

        form_layout.addRow("Квест:", self.quest_combo)
        form_layout.addRow("Комната:", self.room_combo)
        form_layout.addRow("Дата:", self.date_input)
        form_layout.addRow("Время:", self.time_input)
        form_layout.addRow("Количество участников:", self.participants_input)

        layout.addWidget(self.title_label)
        layout.addLayout(form_layout)
        layout.addWidget(self.services_group)
        layout.addWidget(self.confirm_button)
        layout.addStretch()

        self.setLayout(layout)

    def create_booking(self):
        if not self.client_id:
            QMessageBox.warning(self, "Ошибка", "Необходимо войти в систему")
            return

        # Получаем выбранные параметры
        quest_id = self.quest_combo.currentData()
        room_id = self.room_combo.currentData()
        date = self.date_input.date().toString("yyyy-MM-dd")
        time = self.time_input.time().toString("HH:mm")

        # Проверяем доступность комнаты
        rooms = ApiClient.get_rooms()
        room = next((r for r in rooms if r["room_id"] == room_id), None)
        if not room or not room["is_available"]:
            QMessageBox.warning(self, "Ошибка", "Выбранная комната недоступна")
            return

        # Проверяем количество участников
        participants = self.participants_input.value()
        if participants > room["capacity"]:
            QMessageBox.warning(
                self, "Ошибка",
                f"Выбранная комната вмещает до {room['capacity']} человек. "
                f"Уменьшите количество участников или выберите другую комнату."
            )
            return

        # Создаем новое расписание
        schedule_data = {
            "quest_id": quest_id,
            "room_id": room_id,
            "date": date,
            "start_time": time,
            "end_time": self.calculate_end_time(quest_id, time)
        }

        schedule = ApiClient.create_schedule(schedule_data)
        if not schedule:
            QMessageBox.warning(self, "Ошибка", "Не удалось создать расписание")
            return

        # Создаем бронирование
        booking_data = {
            "client_id": self.client_id,
            "schedule_id": schedule["schedule_id"],
            "employee_id": 1,
            "status": "На рассмотрение",
            "participants_count": participants
        }

        booking = ApiClient.create_booking(booking_data)
        if not booking:
            QMessageBox.warning(self, "Ошибка", "Не удалось создать бронирование")
            return

        # Добавляем выбранные услуги
        selected_services = [cb.service_id for cb in self.service_checkboxes if cb.isChecked()]
        for service_id in selected_services:
            service_data = {
                "service_id": service_id,
                "booking_id": booking["booking_id"]
            }
            ApiClient.update_service(service_id, service_data)

        QMessageBox.information(self, "Успех", "Бронирование успешно создано!")
        self.parent().stacked_widget.setCurrentIndex(0)  # Возвращаемся к списку квестов

    def calculate_end_time(self, quest_id, start_time):
        quests = ApiClient.get_quests()
        quest = next((q for q in quests if q["quest_id"] == quest_id), None)
        if not quest:
            return start_time

        duration = quest["duration"]
        start = QTime.fromString(start_time, "HH:mm")
        end = start.addSecs(duration * 60)
        return end.toString("HH:mm")


class AdminBookingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.title_label = QLabel("Управление бронированиями")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск бронирований...")
        self.search_input.textChanged.connect(self.filter_bookings)

        self.bookings_table = QTableWidget()
        self.bookings_table.setColumnCount(8)
        self.bookings_table.setHorizontalHeaderLabels(
            ["ID", "Клиент", "Квест", "Комната", "Дата", "Время", "Участники", "Статус"])
        self.bookings_table.horizontalHeader().setStretchLastSection(True)
        self.bookings_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.bookings_table.setSelectionMode(QTableWidget.SingleSelection)

        button_layout = QHBoxLayout()

        self.status_button = QPushButton("Изменить статус")
        self.status_button.setStyleSheet("background-color: #5bc0de; padding: 8px;")
        self.status_button.clicked.connect(self.change_booking_status)

        self.cancel_button = QPushButton("Отменить")
        self.cancel_button.setStyleSheet("background-color: #d9534f; padding: 8px;")
        self.cancel_button.clicked.connect(self.cancel_booking)

        button_layout.addWidget(self.status_button)
        button_layout.addWidget(self.cancel_button)

        layout.addWidget(self.title_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.bookings_table)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.load_bookings()

    def load_bookings(self):
        self.bookings = ApiClient.get_bookings()
        self.clients = {c["client_id"]: c["full_name"] for c in ApiClient.get_clients()}
        self.schedules = ApiClient.get_schedules()
        self.quests = {q["quest_id"]: q["title"] for q in ApiClient.get_quests()}
        self.rooms = {r["room_id"]: r["title"] for r in ApiClient.get_rooms()}
        self.employees = {e["employee_id"]: e["full_name"] for e in ApiClient.get_employees()}

        self.update_table()

    def update_table(self):
        self.bookings_table.setRowCount(len(self.bookings))

        for row, booking in enumerate(self.bookings):
            schedule = next((s for s in self.schedules if s["schedule_id"] == booking["schedule_id"]), None)

            self.bookings_table.setItem(row, 0, QTableWidgetItem(str(booking["booking_id"])))
            self.bookings_table.setItem(row, 1, QTableWidgetItem(self.clients.get(booking["client_id"], "Неизвестно")))

            if schedule:
                self.bookings_table.setItem(row, 2,
                                            QTableWidgetItem(self.quests.get(schedule["quest_id"], "Неизвестно")))
                self.bookings_table.setItem(row, 3, QTableWidgetItem(self.rooms.get(schedule["room_id"], "Неизвестно")))
                self.bookings_table.setItem(row, 4, QTableWidgetItem(schedule.get("date", "Неизвестно")))
                time = schedule.get("start_time", "")
                if isinstance(time, str) and "T" in time:
                    time = time.split("T")[1][:5]
                self.bookings_table.setItem(row, 5, QTableWidgetItem(time[:5] if time else "Неизвестно"))
            else:
                self.bookings_table.setItem(row, 2, QTableWidgetItem("Неизвестно"))
                self.bookings_table.setItem(row, 3, QTableWidgetItem("Неизвестно"))
                self.bookings_table.setItem(row, 4, QTableWidgetItem("Неизвестно"))
                self.bookings_table.setItem(row, 5, QTableWidgetItem("Неизвестно"))

            self.bookings_table.setItem(row, 6, QTableWidgetItem(str(booking.get("participants_count", 0))))
            self.bookings_table.setItem(row, 7, QTableWidgetItem(booking["status"]))

        self.bookings_table.resizeColumnsToContents()
        self.bookings_table.horizontalHeader().setStretchLastSection(True)

    def filter_bookings(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.update_table()
            return

        filtered = []
        for booking in self.bookings:
            schedule = next((s for s in self.schedules if s["schedule_id"] == booking["schedule_id"]), None)

            client_name = self.clients.get(booking["client_id"], "").lower()
            quest_name = self.quests.get(schedule["quest_id"], "").lower() if schedule else ""
            room_name = self.rooms.get(schedule["room_id"], "").lower() if schedule else ""
            date = schedule.get("date", "").lower() if schedule else ""
            time = schedule.get("start_time", "").lower() if schedule else ""
            participants = str(booking.get("participants_count", 0)).lower()
            status = booking.get("status", "").lower()

            if (search_text in str(booking["booking_id"]) or
                    search_text in client_name or
                    search_text in quest_name or
                    search_text in room_name or
                    search_text in date or
                    search_text in time or
                    search_text in participants or
                    search_text in status):
                filtered.append(booking)

        self.bookings_table.setRowCount(len(filtered))
        for row, booking in enumerate(filtered):
            schedule = next((s for s in self.schedules if s["schedule_id"] == booking["schedule_id"]), None)

            self.bookings_table.setItem(row, 0, QTableWidgetItem(str(booking["booking_id"])))
            self.bookings_table.setItem(row, 1, QTableWidgetItem(self.clients.get(booking["client_id"], "Неизвестно")))

            if schedule:
                self.bookings_table.setItem(row, 2,
                                            QTableWidgetItem(self.quests.get(schedule["quest_id"], "Неизвестно")))
                self.bookings_table.setItem(row, 3, QTableWidgetItem(self.rooms.get(schedule["room_id"], "Неизвестно")))
                self.bookings_table.setItem(row, 4, QTableWidgetItem(schedule.get("date", "Неизвестно")))
                time = schedule.get("start_time", "")
                if isinstance(time, str) and "T" in time:
                    time = time.split("T")[1][:5]
                self.bookings_table.setItem(row, 5, QTableWidgetItem(time[:5] if time else "Неизвестно"))
            else:
                self.bookings_table.setItem(row, 2, QTableWidgetItem("Неизвестно"))
                self.bookings_table.setItem(row, 3, QTableWidgetItem("Неизвестно"))
                self.bookings_table.setItem(row, 4, QTableWidgetItem("Неизвестно"))
                self.bookings_table.setItem(row, 5, QTableWidgetItem("Неизвестно"))

            self.bookings_table.setItem(row, 6, QTableWidgetItem(str(booking.get("participants_count", 0))))
            self.bookings_table.setItem(row, 7, QTableWidgetItem(booking["status"]))

    def change_booking_status(self):
        selected_row = self.bookings_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите бронирование для изменения статуса")
            return

        booking_id = int(self.bookings_table.item(selected_row, 0).text())
        booking = next((b for b in self.bookings if b["booking_id"] == booking_id), None)
        if not booking:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Изменение статуса бронирования")
        dialog.setModal(True)

        layout = QFormLayout(dialog)

        status_combo = QComboBox()
        status_combo.addItems(["Подтвержден", "Завершен", "Отменен"])
        status_combo.setCurrentText(booking["status"])

        layout.addRow("Новый статус:", status_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            new_status = status_combo.currentText()

            # Сохраняем все исходные данные, меняем только статус
            update_data = {
                "client_id": booking["client_id"],
                "schedule_id": booking["schedule_id"],
                "employee_id": booking["employee_id"],
                "status": new_status,
                "participants_count": booking["participants_count"]
            }

            success = ApiClient.update_booking(booking_id, update_data)
            if success:
                QMessageBox.information(self, "Успех", "Статус бронирования успешно изменен")
                self.load_bookings()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось изменить статус бронирования")

    def cancel_booking(self):
        selected_row = self.bookings_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите бронирование для отмены")
            return

        booking_id = int(self.bookings_table.item(selected_row, 0).text())
        booking_title = f"Бронирование #{booking_id}"

        reply = QMessageBox.question(
            self, "Подтверждение отмены",
            f"Вы уверены, что хотите отменить {booking_title}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            booking = next((b for b in self.bookings if b["booking_id"] == booking_id), None)
            if not booking:
                return

            update_data = {
                "client_id": booking["client_id"],
                "schedule_id": booking["schedule_id"],
                "employee_id": booking["employee_id"],
                "status": "Отменен",
                "participants_count": booking["participants_count"]
            }

            success = ApiClient.update_booking(booking_id, update_data)
            if success:
                QMessageBox.information(self, "Успех", "Бронирование успешно отменено")
                self.load_bookings()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось отменить бронирование")


class AdminServicesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.title_label = QLabel("Управление услугами")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск услуг...")
        self.search_input.textChanged.connect(self.filter_services)

        self.services_table = QTableWidget()
        self.services_table.setColumnCount(5)
        self.services_table.setHorizontalHeaderLabels(["ID", "Название", "Описание", "Цена", "Бронирование"])
        self.services_table.horizontalHeader().setStretchLastSection(True)
        self.services_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.services_table.setSelectionMode(QTableWidget.SingleSelection)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.add_button.setStyleSheet("background-color: #5cb85c; padding: 8px;")
        self.add_button.clicked.connect(self.add_service)

        self.edit_button = QPushButton("Редактировать")
        self.edit_button.setStyleSheet("background-color: #5bc0de; padding: 8px;")
        self.edit_button.clicked.connect(self.edit_service)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setStyleSheet("background-color: #d9534f; padding: 8px;")
        self.delete_button.clicked.connect(self.delete_service)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        layout.addWidget(self.title_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.services_table)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.load_services()

    def load_services(self):
        self.services = ApiClient.get_services()
        self.bookings = {b["booking_id"]: f"Бронь #{b['booking_id']}" for b in ApiClient.get_bookings()}
        self.update_table()

    def update_table(self):
        self.services_table.setRowCount(len(self.services))
        for row, service in enumerate(self.services):
            self.services_table.setItem(row, 0, QTableWidgetItem(str(service["service_id"])))
            self.services_table.setItem(row, 1, QTableWidgetItem(service["title"]))
            self.services_table.setItem(row, 2, QTableWidgetItem(service["description"]))
            self.services_table.setItem(row, 3, QTableWidgetItem(str(service["price"])))
            self.services_table.setItem(row, 4,
                                        QTableWidgetItem(self.bookings.get(service.get("booking_id", 0), "Не указано")))

        self.services_table.resizeColumnsToContents()
        self.services_table.setColumnWidth(2, 300)  # Фиксированная ширина для описания
        self.services_table.horizontalHeader().setStretchLastSection(True)

    def filter_services(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.update_table()
            return

        filtered = [s for s in self.services if
                    search_text in str(s["service_id"]) or
                    search_text in s["title"].lower() or
                    search_text in s["description"].lower() or
                    search_text in str(s["price"]) or
                    search_text in self.bookings.get(s.get("booking_id", 0), "").lower()]

        self.services_table.setRowCount(len(filtered))
        for row, service in enumerate(filtered):
            self.services_table.setItem(row, 0, QTableWidgetItem(str(service["service_id"])))
            self.services_table.setItem(row, 1, QTableWidgetItem(service["title"]))
            self.services_table.setItem(row, 2, QTableWidgetItem(service["description"]))
            self.services_table.setItem(row, 3, QTableWidgetItem(str(service["price"])))
            self.services_table.setItem(row, 4,
                                        QTableWidgetItem(self.bookings.get(service.get("booking_id", 0), "Не указано")))

    def add_service(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавление услуги")
        dialog.setModal(True)
        dialog.setMinimumWidth(500)

        layout = QFormLayout(dialog)

        title_input = QLineEdit()
        description_input = QTextEdit()
        price_input = QSpinBox()
        price_input.setRange(0, 100000)
        price_input.setValue(1000)
        price_input.setSuffix(" руб")

        booking_combo = QComboBox()
        booking_combo.addItem("Не привязано", 0)
        bookings = ApiClient.get_bookings()
        for booking in bookings:
            booking_combo.addItem(f"Бронь #{booking['booking_id']}", booking["booking_id"])

        layout.addRow("Название*:", title_input)
        layout.addRow("Описание:", description_input)
        layout.addRow("Цена*:", price_input)
        layout.addRow("Бронирование:", booking_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            # Валидация обязательных полей
            if not title_input.text() or not price_input.value():
                QMessageBox.warning(self, "Ошибка", "Поля с * обязательны для заполнения")
                return

            service_data = {
                "title": title_input.text(),
                "description": description_input.toPlainText(),
                "price": price_input.value(),
                "booking_id": booking_combo.currentData()
            }

            new_service = ApiClient.create_service(service_data)
            if new_service:
                self.load_services()
                QMessageBox.information(self, "Успех", "Услуга успешно добавлена")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить услугу")

    def edit_service(self):
        selected_row = self.services_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите услугу для редактирования")
            return

        service_id = int(self.services_table.item(selected_row, 0).text())
        service = next((s for s in self.services if s["service_id"] == service_id), None)
        if not service:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Редактирование услуги")
        dialog.setModal(True)
        dialog.setMinimumWidth(500)

        layout = QFormLayout(dialog)

        title_input = QLineEdit(service["title"])
        description_input = QTextEdit(service["description"])
        price_input = QSpinBox()
        price_input.setRange(0, 100000)
        price_input.setValue(service["price"])
        price_input.setSuffix(" руб")

        booking_combo = QComboBox()
        booking_combo.addItem("Не привязано", 0)
        bookings = ApiClient.get_bookings()
        for booking in bookings:
            booking_combo.addItem(f"Бронь #{booking['booking_id']}", booking["booking_id"])

        current_booking = service.get("booking_id", 0)
        index = booking_combo.findData(current_booking)
        if index >= 0:
            booking_combo.setCurrentIndex(index)

        layout.addRow("Название*:", title_input)
        layout.addRow("Описание:", description_input)
        layout.addRow("Цена*:", price_input)
        layout.addRow("Бронирование:", booking_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            # Валидация обязательных полей
            if not title_input.text() or not price_input.value():
                QMessageBox.warning(self, "Ошибка", "Поля с * обязательны для заполнения")
                return

            service_data = {
                "title": title_input.text(),
                "description": description_input.toPlainText(),
                "price": price_input.value(),
                "booking_id": booking_combo.currentData()
            }

            success = ApiClient.update_service(service_id, service_data)
            if success:
                self.load_services()
                QMessageBox.information(self, "Успех", "Услуга успешно обновлена")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось обновить услугу")

    def delete_service(self):
        selected_row = self.services_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите услугу для удаления")
            return

        service_id = int(self.services_table.item(selected_row, 0).text())
        service_name = self.services_table.item(selected_row, 1).text()

        reply = QMessageBox.question(
            self, "Подтверждение удаления",
            f"Вы уверены, что хотите удалить услугу '{service_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = ApiClient.delete_service(service_id)
            if success:
                self.load_services()
                QMessageBox.information(self, "Успех", "Услуга успешно удалена")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить услугу")


class AdminUsersWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.title_label = QLabel("Управление пользователями")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск пользователей...")
        self.search_input.textChanged.connect(self.filter_users)

        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels(["ID", "ФИО", "Телефон", "Email", "Дата рождения", "Логин"])
        self.users_table.horizontalHeader().setStretchLastSection(True)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.setSelectionMode(QTableWidget.SingleSelection)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.add_button.setStyleSheet("background-color: #5cb85c; padding: 8px;")
        self.add_button.clicked.connect(self.add_user)

        self.edit_button = QPushButton("Редактировать")
        self.edit_button.setStyleSheet("background-color: #5bc0de; padding: 8px;")
        self.edit_button.clicked.connect(self.edit_user)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setStyleSheet("background-color: #d9534f; padding: 8px;")
        self.delete_button.clicked.connect(self.delete_user)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        layout.addWidget(self.title_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.users_table)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.load_users()

    def load_users(self):
        clients = ApiClient.get_clients()
        self.users_table.setRowCount(len(clients))

        for row, client in enumerate(clients):
            self.users_table.setItem(row, 0, QTableWidgetItem(str(client["client_id"])))
            self.users_table.setItem(row, 1, QTableWidgetItem(client["full_name"]))
            self.users_table.setItem(row, 2, QTableWidgetItem(client["phone"]))
            self.users_table.setItem(row, 3, QTableWidgetItem(client["email"]))
            self.users_table.setItem(row, 4, QTableWidgetItem(client["birth_date"]))
            self.users_table.setItem(row, 5, QTableWidgetItem(client.get("login", "")))

        self.users_table.resizeColumnsToContents()
        self.users_table.horizontalHeader().setStretchLastSection(True)

    def filter_users(self):
        search_text = self.search_input.text().lower()
        clients = ApiClient.get_clients()

        if not search_text:
            self.load_users()
            return

        filtered = [c for c in clients if
                    search_text in str(c["client_id"]) or
                    search_text in c["full_name"].lower() or
                    search_text in c["phone"].lower() or
                    search_text in c["email"].lower() or
                    search_text in c["birth_date"].lower() or
                    search_text in c.get("login", "").lower()]

        self.users_table.setRowCount(len(filtered))
        for row, client in enumerate(filtered):
            self.users_table.setItem(row, 0, QTableWidgetItem(str(client["client_id"])))
            self.users_table.setItem(row, 1, QTableWidgetItem(client["full_name"]))
            self.users_table.setItem(row, 2, QTableWidgetItem(client["phone"]))
            self.users_table.setItem(row, 3, QTableWidgetItem(client["email"]))
            self.users_table.setItem(row, 4, QTableWidgetItem(client["birth_date"]))
            self.users_table.setItem(row, 5, QTableWidgetItem(client.get("login", "")))

    def add_user(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавление пользователя")
        dialog.setModal(True)
        dialog.setMinimumWidth(400)

        layout = QFormLayout(dialog)

        self.full_name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        self.birth_date_input = QDateEdit()
        self.birth_date_input.setDate(QDate.currentDate().addYears(-18))
        self.birth_date_input.setCalendarPopup(True)

        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        layout.addRow("ФИО*:", self.full_name_input)
        layout.addRow("Телефон*:", self.phone_input)
        layout.addRow("Email*:", self.email_input)
        layout.addRow("Дата рождения*:", self.birth_date_input)
        layout.addRow("Логин*:", self.login_input)
        layout.addRow("Пароль*:", self.password_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            # Валидация
            if not all([self.full_name_input.text(), self.phone_input.text(),
                        self.email_input.text(), self.login_input.text(),
                        self.password_input.text()]):
                QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения")
                return

            user_data = {
                "full_name": self.full_name_input.text(),
                "phone": self.phone_input.text(),
                "email": self.email_input.text(),
                "birth_date": self.birth_date_input.date().toString("yyyy-MM-dd"),
                "login": self.login_input.text(),
                "password": self.password_input.text()
            }

            result = ApiClient.register_client(user_data)
            if result:
                QMessageBox.information(self, "Успех", "Пользователь успешно добавлен")
                self.load_users()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить пользователя")

    def edit_user(self):
        selected_row = self.users_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для редактирования")
            return

        client_id = int(self.users_table.item(selected_row, 0).text())
        client_data = ApiClient.get_client(client_id)
        if not client_data:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные пользователя")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Редактирование пользователя")
        dialog.setModal(True)
        dialog.setMinimumWidth(400)

        layout = QFormLayout(dialog)

        self.full_name_input = QLineEdit(client_data["full_name"])
        self.phone_input = QLineEdit(client_data["phone"])
        self.email_input = QLineEdit(client_data["email"])

        self.birth_date_input = QDateEdit()
        if client_data["birth_date"]:
            year, month, day = map(int, client_data["birth_date"].split("-"))
            self.birth_date_input.setDate(QDate(year, month, day))
        else:
            self.birth_date_input.setDate(QDate.currentDate())
        self.birth_date_input.setCalendarPopup(True)

        self.login_input = QLineEdit(client_data.get("login", ""))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Оставьте пустым, чтобы не менять")
        self.password_input.setEchoMode(QLineEdit.Password)

        layout.addRow("ФИО:", self.full_name_input)
        layout.addRow("Телефон:", self.phone_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Дата рождения:", self.birth_date_input)
        layout.addRow("Логин:", self.login_input)
        layout.addRow("Новый пароль:", self.password_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            update_data = {
                "full_name": self.full_name_input.text(),
                "phone": self.phone_input.text(),
                "email": self.email_input.text(),
                "birth_date": self.birth_date_input.date().toString("yyyy-MM-dd"),
                "login": self.login_input.text()
            }

            password = self.password_input.text()
            if password:
                update_data["password"] = password

            result = ApiClient.update_client(client_id, update_data)
            if result:
                QMessageBox.information(self, "Успех", "Данные пользователя успешно обновлены")
                self.load_users()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось обновить данные пользователя")

    def delete_user(self):
        selected_row = self.users_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для удаления")
            return

        client_id = int(self.users_table.item(selected_row, 0).text())
        client_name = self.users_table.item(selected_row, 1).text()

        reply = QMessageBox.question(
            self, "Подтверждение удаления",
            f"Вы уверены, что хотите удалить пользователя {client_name}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = ApiClient.delete_client(client_id)
            if success:
                QMessageBox.information(self, "Успех", "Пользователь успешно удален")
                self.load_users()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить пользователя")


class AdminEmployeesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.title_label = QLabel("Управление сотрудниками")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск сотрудников...")
        self.search_input.textChanged.connect(self.filter_employees)

        self.employees_table = QTableWidget()
        self.employees_table.setColumnCount(5)
        self.employees_table.setHorizontalHeaderLabels(["ID", "ФИО", "Должность", "Логин", "Статус"])
        self.employees_table.horizontalHeader().setStretchLastSection(True)
        self.employees_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.employees_table.setSelectionMode(QTableWidget.SingleSelection)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.add_button.setStyleSheet("background-color: #5cb85c; padding: 8px;")
        self.add_button.clicked.connect(self.add_employee)

        self.edit_button = QPushButton("Редактировать")
        self.edit_button.setStyleSheet("background-color: #5bc0de; padding: 8px;")
        self.edit_button.clicked.connect(self.edit_employee)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setStyleSheet("background-color: #d9534f; padding: 8px;")
        self.delete_button.clicked.connect(self.delete_employee)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        layout.addWidget(self.title_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.employees_table)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.load_employees()

    def load_employees(self):
        employees = ApiClient.get_employees()
        positions = {p["position_id"]: p["title"] for p in ApiClient.get_positions()}

        self.employees_table.setRowCount(len(employees))
        for row, employee in enumerate(employees):
            self.employees_table.setItem(row, 0, QTableWidgetItem(str(employee["employee_id"])))
            self.employees_table.setItem(row, 1, QTableWidgetItem(employee["full_name"]))
            self.employees_table.setItem(row, 2, QTableWidgetItem(positions.get(employee["position_id"], "Неизвестно")))
            self.employees_table.setItem(row, 3, QTableWidgetItem(employee["login"]))
            self.employees_table.setItem(row, 4, QTableWidgetItem("Активен"))

        self.employees_table.resizeColumnsToContents()
        self.employees_table.horizontalHeader().setStretchLastSection(True)

    def filter_employees(self):
        search_text = self.search_input.text().lower()
        employees = ApiClient.get_employees()
        positions = {p["position_id"]: p["title"] for p in ApiClient.get_positions()}

        if not search_text:
            self.load_employees()
            return

        filtered = [e for e in employees if
                    search_text in str(e["employee_id"]) or
                    search_text in e["full_name"].lower() or
                    search_text in positions.get(e["position_id"], "").lower() or
                    search_text in e["login"].lower()]

        self.employees_table.setRowCount(len(filtered))
        for row, employee in enumerate(filtered):
            self.employees_table.setItem(row, 0, QTableWidgetItem(str(employee["employee_id"])))
            self.employees_table.setItem(row, 1, QTableWidgetItem(employee["full_name"]))
            self.employees_table.setItem(row, 2, QTableWidgetItem(positions.get(employee["position_id"], "Неизвестно")))
            self.employees_table.setItem(row, 3, QTableWidgetItem(employee["login"]))
            self.employees_table.setItem(row, 4, QTableWidgetItem("Активен"))

    def add_employee(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавление сотрудника")
        dialog.setModal(True)
        dialog.setMinimumWidth(400)

        layout = QFormLayout(dialog)

        self.full_name_input = QLineEdit()

        self.position_combo = QComboBox()
        positions = ApiClient.get_positions()
        for position in positions:
            self.position_combo.addItem(position["title"], position["position_id"])

        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        layout.addRow("ФИО*:", self.full_name_input)
        layout.addRow("Должность*:", self.position_combo)
        layout.addRow("Логин*:", self.login_input)
        layout.addRow("Пароль*:", self.password_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            # Валидация
            if not all([self.full_name_input.text(), self.login_input.text(),
                        self.password_input.text()]):
                QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения")
                return

            employee_data = {
                "full_name": self.full_name_input.text(),
                "position_id": self.position_combo.currentData(),
                "login": self.login_input.text(),
                "password": self.password_input.text()
            }

            result = ApiClient.create_employee(employee_data)
            if result:
                QMessageBox.information(self, "Успех", "Сотрудник успешно добавлен")
                self.load_employees()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить сотрудника")

    def edit_employee(self):
        selected_row = self.employees_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для редактирования")
            return

        employee_id = int(self.employees_table.item(selected_row, 0).text())
        employee_data = next((e for e in ApiClient.get_employees() if e["employee_id"] == employee_id), None)
        if not employee_data:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные сотрудника")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Редактирование сотрудника")
        dialog.setModal(True)
        dialog.setMinimumWidth(400)

        layout = QFormLayout(dialog)

        self.full_name_input = QLineEdit(employee_data["full_name"])

        self.position_combo = QComboBox()
        positions = ApiClient.get_positions()
        for position in positions:
            self.position_combo.addItem(position["title"], position["position_id"])
            if position["position_id"] == employee_data["position_id"]:
                self.position_combo.setCurrentIndex(self.position_combo.count() - 1)

        self.login_input = QLineEdit(employee_data["login"])
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Оставьте пустым, чтобы не менять")
        self.password_input.setEchoMode(QLineEdit.Password)

        layout.addRow("ФИО:", self.full_name_input)
        layout.addRow("Должность:", self.position_combo)
        layout.addRow("Логин:", self.login_input)
        layout.addRow("Новый пароль:", self.password_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            update_data = {
                "full_name": self.full_name_input.text(),
                "position_id": self.position_combo.currentData(),
                "login": self.login_input.text()
            }

            password = self.password_input.text()
            if password:
                update_data["password"] = password

            result = ApiClient.update_employee(employee_id, update_data)
            if result:
                QMessageBox.information(self, "Успех", "Данные сотрудника успешно обновлены")
                self.load_employees()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось обновить данные сотрудника")

    def delete_employee(self):
        selected_row = self.employees_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для удаления")
            return

        employee_id = int(self.employees_table.item(selected_row, 0).text())
        employee_name = self.employees_table.item(selected_row, 1).text()

        reply = QMessageBox.question(
            self, "Подтверждение удаления",
            f"Вы уверены, что хотите удалить сотрудника {employee_name}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = ApiClient.delete_employee(employee_id)
            if success:
                QMessageBox.information(self, "Успех", "Сотрудник успешно удален")
                self.load_employees()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить сотрудника")


class AdminQuestsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_quests()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Управление квестами")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск квестов...")
        self.search_input.textChanged.connect(self.filter_quests)

        self.quests_table = QTableWidget()
        self.quests_table.setColumnCount(6)
        self.quests_table.setHorizontalHeaderLabels(["ID", "Название", "Описание", "Сложность", "Длительность", "Цена"])
        self.quests_table.horizontalHeader().setStretchLastSection(True)
        self.quests_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.quests_table.setSelectionMode(QTableWidget.SingleSelection)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.add_button.setStyleSheet("background-color: #5cb85c; padding: 8px;")
        self.add_button.clicked.connect(self.show_add_quest_dialog)

        self.edit_button = QPushButton("Редактировать")
        self.edit_button.setStyleSheet("background-color: #5bc0de; padding: 8px;")
        self.edit_button.clicked.connect(self.edit_selected_quest)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setStyleSheet("background-color: #d9534f; padding: 8px;")
        self.delete_button.clicked.connect(self.delete_selected_quest)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        layout.addWidget(self.title_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.quests_table)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_quests(self):
        self.quests = ApiClient.get_quests()
        self.update_table()

    def update_table(self):
        self.quests_table.setRowCount(len(self.quests))
        for row, quest in enumerate(self.quests):
            self.quests_table.setItem(row, 0, QTableWidgetItem(str(quest["quest_id"])))
            self.quests_table.setItem(row, 1, QTableWidgetItem(quest["title"]))
            self.quests_table.setItem(row, 2, QTableWidgetItem(quest["description"]))
            self.quests_table.setItem(row, 3, QTableWidgetItem(str(quest["difficulty"])))
            self.quests_table.setItem(row, 4, QTableWidgetItem(f"{quest['duration']} мин"))
            self.quests_table.setItem(row, 5, QTableWidgetItem(f"{quest['price']} руб"))

        self.quests_table.resizeColumnsToContents()
        self.quests_table.setColumnWidth(2, 300)  # Фиксированная ширина для описания
        self.quests_table.horizontalHeader().setStretchLastSection(True)

    def filter_quests(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.update_table()
            return

        filtered = [q for q in self.quests if
                   search_text in q["title"].lower() or
                   search_text in q["description"].lower() or
                   search_text in str(q["difficulty"]) or
                   search_text in str(q["duration"]) or
                   search_text in str(q["price"])]

        self.quests_table.setRowCount(len(filtered))
        for row, quest in enumerate(filtered):
            self.quests_table.setItem(row, 0, QTableWidgetItem(str(quest["quest_id"])))
            self.quests_table.setItem(row, 1, QTableWidgetItem(quest["title"]))
            self.quests_table.setItem(row, 2, QTableWidgetItem(quest["description"]))
            self.quests_table.setItem(row, 3, QTableWidgetItem(str(quest["difficulty"])))
            self.quests_table.setItem(row, 4, QTableWidgetItem(f"{quest['duration']} мин"))
            self.quests_table.setItem(row, 5, QTableWidgetItem(f"{quest['price']} руб"))

    def show_add_quest_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить квест")
        dialog.setModal(True)
        dialog.setMinimumWidth(500)

        layout = QFormLayout(dialog)

        title_input = QLineEdit()
        description_input = QTextEdit()
        difficulty_input = QSpinBox()
        difficulty_input.setRange(1, 5)
        difficulty_input.setValue(3)
        duration_input = QSpinBox()
        duration_input.setRange(15, 180)
        duration_input.setValue(60)
        duration_input.setSuffix(" мин")
        price_input = QSpinBox()
        price_input.setRange(0, 10000)
        price_input.setValue(2000)
        price_input.setSuffix(" руб")

        layout.addRow("Название*:", title_input)
        layout.addRow("Описание:", description_input)
        layout.addRow("Сложность (1-5)*:", difficulty_input)
        layout.addRow("Длительность*:", duration_input)
        layout.addRow("Цена*:", price_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            # Валидация обязательных полей
            if not title_input.text() or not difficulty_input.value() or not duration_input.value() or not price_input.value():
                QMessageBox.warning(self, "Ошибка", "Поля с * обязательны для заполнения")
                return

            quest_data = {
                "title": title_input.text(),
                "description": description_input.toPlainText(),
                "difficulty": difficulty_input.value(),
                "duration": duration_input.value(),
                "price": price_input.value()
            }

            new_quest = ApiClient.create_quest(quest_data)
            if new_quest:
                self.load_quests()
                QMessageBox.information(self, "Успех", "Квест успешно добавлен")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить квест")

    def edit_selected_quest(self):
        selected = self.quests_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите квест для редактирования")
            return

        quest_id = int(self.quests_table.item(selected, 0).text())
        quest = next((q for q in self.quests if q["quest_id"] == quest_id), None)
        if not quest:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Редактировать квест")
        dialog.setModal(True)
        dialog.setMinimumWidth(500)

        layout = QFormLayout(dialog)

        title_input = QLineEdit(quest["title"])
        description_input = QTextEdit(quest["description"])
        difficulty_input = QSpinBox()
        difficulty_input.setRange(1, 5)
        difficulty_input.setValue(quest["difficulty"])
        duration_input = QSpinBox()
        duration_input.setRange(15, 180)
        duration_input.setValue(quest["duration"])
        duration_input.setSuffix(" мин")
        price_input = QSpinBox()
        price_input.setRange(0, 10000)
        price_input.setValue(quest["price"])
        price_input.setSuffix(" руб")

        layout.addRow("Название*:", title_input)
        layout.addRow("Описание:", description_input)
        layout.addRow("Сложность (1-5)*:", difficulty_input)
        layout.addRow("Длительность*:", duration_input)
        layout.addRow("Цена*:", price_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            # Валидация обязательных полей
            if not title_input.text() or not difficulty_input.value() or not duration_input.value() or not price_input.value():
                QMessageBox.warning(self, "Ошибка", "Поля с * обязательны для заполнения")
                return

            quest_data = {
                "title": title_input.text(),
                "description": description_input.toPlainText(),
                "difficulty": difficulty_input.value(),
                "duration": duration_input.value(),
                "price": price_input.value()
            }

            success = ApiClient.update_quest(quest_id, quest_data)
            if success:
                self.load_quests()
                QMessageBox.information(self, "Успех", "Квест успешно обновлен")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось обновить квест")

    def delete_selected_quest(self):
        selected = self.quests_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите квест для удаления")
            return

        quest_id = int(self.quests_table.item(selected, 0).text())
        quest_title = self.quests_table.item(selected, 1).text()

        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Вы уверены, что хотите удалить квест '{quest_title}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = ApiClient.delete_quest(quest_id)
            if success:
                self.load_quests()
                QMessageBox.information(self, "Успех", "Квест успешно удален")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить квест")

class ClientMainWindow(QMainWindow):
    def __init__(self, client_id):
        super().__init__()
        self.client_id = client_id  # Сохраняем ID клиента
        self.setWindowTitle("Black Rooms - Клиент")
        self.setMinimumSize(800, 600)

        self.stacked_widget = QStackedWidget()

        # Создаем виджеты для клиента, передавая client_id
        self.account_widget = ClientAccountWindow(client_id=self.client_id)
        self.quest_list_widget = QuestListWindow()
        self.booking_widget = BookingWindow(client_id=self.client_id)

        # Добавляем виджеты в stacked widget
        self.stacked_widget.addWidget(self.quest_list_widget)
        self.stacked_widget.addWidget(self.account_widget)
        self.stacked_widget.addWidget(self.booking_widget)

        # Создаем навигационное меню
        self.nav_layout = QHBoxLayout()

        self.quests_button = QPushButton("Квесты")
        self.quests_button.setStyleSheet("padding: 8px;")
        self.quests_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.quest_list_widget))

        self.account_button = QPushButton("Мой аккаунт")
        self.account_button.setStyleSheet("padding: 8px;")
        self.account_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.account_widget))

        self.logout_button = QPushButton("Выйти")
        self.logout_button.setStyleSheet("padding: 8px; background-color: #d9534f;")
        self.logout_button.clicked.connect(self.logout)

        self.nav_layout.addWidget(self.quests_button)
        self.nav_layout.addWidget(self.account_button)
        self.nav_layout.addStretch()
        self.nav_layout.addWidget(self.logout_button)

        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.nav_layout)
        main_layout.addWidget(self.stacked_widget)

        # Устанавливаем центральный виджет
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Подключаем кнопку бронирования
        self.quest_list_widget.book_button.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.booking_widget))

    def logout(self):
        self.close()
        # Здесь можно добавить дополнительную логику очистки, если необходимо


class AdminMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Black Rooms - Администратор")
        self.setMinimumSize(1000, 700)

        self.tab_widget = QTabWidget()

        # Создаем виджеты для администратора
        self.users_widget = AdminUsersWindow()
        self.employees_widget = AdminEmployeesWindow()
        self.quests_widget = AdminQuestsWindow()
        self.bookings_widget = AdminBookingsWindow()
        self.services_widget = AdminServicesWindow()

        # Добавляем вкладки
        self.tab_widget.addTab(self.users_widget, "Пользователи")
        self.tab_widget.addTab(self.employees_widget, "Сотрудники")
        self.tab_widget.addTab(self.quests_widget, "Квесты")
        self.tab_widget.addTab(self.bookings_widget, "Бронирования")
        self.tab_widget.addTab(self.services_widget, "Услуги")

        # Создаем кнопку выхода
        self.logout_button = QPushButton("Выйти")
        self.logout_button.setStyleSheet("padding: 8px; background-color: #d9534f;")

        # Таймер для обновления данных
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(30000)  # Обновление каждые 30 секунд

        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.logout_button, alignment=Qt.AlignRight)

        # Устанавливаем центральный виджет
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def refresh_data(self):
        """Обновление данных во всех вкладках"""
        current_tab = self.tab_widget.currentIndex()

        if current_tab == 0:
            self.users_widget.load_users()
        elif current_tab == 1:
            self.employees_widget.load_employees()
        elif current_tab == 2:
            self.quests_widget.load_quests()
        elif current_tab == 3:
            self.bookings_widget.load_bookings()
        elif current_tab == 4:
            self.services_widget.load_services()


class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        DarkTheme.apply(self.app)

        self.login_window = LoginWindow()
        self.client_window = None
        self.admin_window = None

        # Показываем окно входа при запуске
        self.login_window.show()

        # Подключаем кнопки входа
        self.login_window.login_button.clicked.connect(self.handle_login)
        self.login_window.register_button.clicked.connect(self.handle_register)

        sys.exit(self.app.exec())

    def handle_login(self):
        login = self.login_window.login_input.text()
        password = self.login_window.password_input.text()

        if not login or not password:
            QMessageBox.warning(self.login_window, "Ошибка", "Введите логин и пароль")
            return

        # Попробуем войти как клиент
        login_data = {"login": login, "password": password}
        client_response = ApiClient.login_client(login_data)

        if client_response and "client_id" in client_response:
            self.login_window.hide()
            self.client_window = ClientMainWindow(client_response["client_id"])
            self.client_window.show()
            return

        # Если не клиент, попробуем войти как сотрудник (админ)
        # Здесь нужно добавить проверку для сотрудников
        # Для демонстрации просто проверяем логин "admin"
        if login == "admin" and password == "admin123":
            self.login_window.hide()
            self.admin_window = AdminMainWindow()
            self.admin_window.show()
        else:
            QMessageBox.warning(self.login_window, "Ошибка", "Неверный логин или пароль")

    def handle_register(self):
        dialog = QDialog(self.login_window)
        dialog.setWindowTitle("Регистрация")
        dialog.setModal(True)

        layout = QFormLayout(dialog)

        full_name_input = QLineEdit()
        phone_input = QLineEdit()
        email_input = QLineEdit()
        birth_date_input = QDateEdit()
        birth_date_input.setCalendarPopup(True)
        birth_date_input.setDate(QDate.currentDate().addYears(-18))
        login_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        confirm_password_input = QLineEdit()
        confirm_password_input.setEchoMode(QLineEdit.Password)

        layout.addRow("ФИО:", full_name_input)
        layout.addRow("Телефон:", phone_input)
        layout.addRow("Email:", email_input)
        layout.addRow("Дата рождения:", birth_date_input)
        layout.addRow("Логин:", login_input)
        layout.addRow("Пароль:", password_input)
        layout.addRow("Подтвердите пароль:", confirm_password_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            if password_input.text() != confirm_password_input.text():
                QMessageBox.warning(dialog, "Ошибка", "Пароли не совпадают")
                return

            client_data = {
                "full_name": full_name_input.text(),
                "phone": phone_input.text(),
                "email": email_input.text(),
                "birth_date": birth_date_input.date().toString("yyyy-MM-dd"),
                "login": login_input.text(),
                "password": password_input.text()
            }

            result = ApiClient.register_client(client_data)
            if result:
                QMessageBox.information(dialog, "Успех", "Регистрация прошла успешно! Теперь вы можете войти.")
            else:
                QMessageBox.warning(dialog, "Ошибка",
                                    "Не удалось зарегистрироваться. Возможно, такой логин уже существует.")

    def logout(self):
        if self.client_window:
            self.client_window.hide()
            self.client_window = None
        if self.admin_window:
            self.admin_window.hide()
            self.admin_window = None

        self.login_window.login_input.clear()
        self.login_window.password_input.clear()
        self.login_window.show()

if __name__ == "__main__":
    MainApp()