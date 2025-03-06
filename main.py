import sys
from PyQt5.QtWidgets import QApplication
from frontend.login import LoginWindow  # Importar la clase LoginWindow desde el archivo login.py

class Main:
    def __init__(self):
        # Crear la aplicación y la ventana de inicio de sesión
        self.app = QApplication(sys.argv)
        self.window = LoginWindow()
        self.window.show()

    def run(self):
        # Ejecutar la aplicación
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    main_app = Main()  # Crear una instancia de la clase Main
    main_app.run()  # Ejecutar la aplicación
