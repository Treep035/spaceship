import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
import subprocess
import os

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio de Sesión")
        self.setGeometry(100, 100, 300, 200)
        
        # Layouts
        layout = QVBoxLayout()
        form_layout = QVBoxLayout()
        
        # Usuario
        self.username_label = QLabel("Usuario:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Introduce tu nombre de usuario")
        form_layout.addWidget(self.username_label)
        form_layout.addWidget(self.username_input)
        
        # Contraseña
        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Introduce tu contraseña")
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)
        
        # Botón de inicio de sesión
        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.clicked.connect(self.validate_login)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.login_button)
        
        self.setLayout(layout)

    def validate_login(self):
        logged_in = validate_login_backend(self.username_input.text(), self.password_input.text())
        
        # Aquí puedes validar el usuario y la contraseña
        if logged_in:
            self.show_message("¡Bienvenido!")
            self.start_game()
        else:
            self.show_message("Usuario o contraseña incorrectos.")
    
    def show_message(self, message):
        self.message_label = QLabel(message)
        self.layout().addWidget(self.message_label)
    
    def start_game(self):
        # Cierra la ventana de inicio de sesión
        self.close()
        self.run_game()

    def run_game(self):
        # Ruta al archivo 'game.py' en la carpeta 'core'
        game_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core', 'game.py'))
        subprocess.run(["python", game_path])