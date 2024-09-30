import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from threading import Thread
from flask import Flask, render_template

# Criar a aplicação Flask
app = Flask(__name__)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página de módulos no Windows
@app.route('/modulos_windows')
def modulos_windows():
    return render_template('modulos_windows.html')

# Rota para a página de módulos no Linux
@app.route('/modulos_linux')
def modulos_linux():
    return render_template('modulos_linux.html')

# Função para iniciar o servidor Flask numa thread separada
def run_flask():
    app.run(debug=False, use_reloader=False)

# Classe para a GUI com PyQt5
class FlaskServerControl(QWidget):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela principal
        self.setWindowTitle("Controlo do Servidor Flask")
        self.setGeometry(100, 100, 400, 200)

        # Layout
        layout = QVBoxLayout()

        # Rótulo para exibir o caminho selecionado
        self.label = QLabel("Caminho do Projeto:")
        layout.addWidget(self.label)

        # Campo para exibir o caminho
        self.path_edit = QLineEdit(self)
        layout.addWidget(self.path_edit)

        # Botão para escolher a pasta
        self.browse_button = QPushButton("Escolher Caminho")
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.browse_button)

        # Botão para Ligar o servidor
        self.start_button = QPushButton("Ligar")
        self.start_button.clicked.connect(self.start_server)
        layout.addWidget(self.start_button)

        # Botão para Desligar o servidor
        self.stop_button = QPushButton("Desligar")
        self.stop_button.clicked.connect(self.stop_server)
        layout.addWidget(self.stop_button)

        # Botão para Sair
        self.exit_button = QPushButton("Sair")
        self.exit_button.clicked.connect(self.exit_app)
        layout.addWidget(self.exit_button)

        # Variável para controlar o processo do servidor
        self.server_thread = None

        # Configurar o layout na janela
        self.setLayout(layout)

    def browse_folder(self):
        # Abre um diálogo para escolher a pasta do projeto
        folder_selected = QFileDialog.getExistingDirectory(self, "Escolher Diretório")
        self.path_edit.setText(folder_selected)

    def start_server(self):
        # Verifica se o servidor Flask já está em execução
        if not self.server_thread or not self.server_thread.is_alive():
            self.server_thread = Thread(target=run_flask)
            self.server_thread.setDaemon(True)
            self.server_thread.start()

    def stop_server(self):
        # Parar o servidor Flask (implementação simplificada)
        if self.server_thread:
            print("O servidor será desligado ao fechar a aplicação.")

    def exit_app(self):
        # Fechar a aplicação e terminar o servidor
        self.close()
        if self.server_thread and self.server_thread.is_alive():
            print("Terminando o servidor Flask...")

if __name__ == '__main__':
    # Iniciar a aplicação GUI com PyQt5
    app_gui = QApplication(sys.argv)
    window = FlaskServerControl()
    window.show()
    
    # Executar a GUI
    sys.exit(app_gui.exec_())
