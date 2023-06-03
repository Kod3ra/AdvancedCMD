import sys
import subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QGroupBox, QVBoxLayout, QColorDialog, QHBoxLayout, QInputDialog, QDialog, QListWidget, QMessageBox


class ThemeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Themes config")
        self.setModal(True)
        self.layout = QVBoxLayout(self)
        self.theme_list = QListWidget()
        self.theme_list.itemDoubleClicked.connect(self.apply_theme)
        self.layout.addWidget(self.theme_list)
        self.load_themes()

    def load_themes(self):
        # Charger la liste des thèmes depuis votre source de stockage (fichier, base de données, etc.)
        # Dans cet exemple, nous ajoutons simplement des thèmes pré-définis à la liste
        self.theme_list.addItem("Theme 1")
        self.theme_list.addItem("Theme 2")
        self.theme_list.addItem("Theme 3")

    def apply_theme(self, item):
        theme_name = item.text()
        # Récupérer le thème complet à partir de votre source de stockage en utilisant le nom du thème
        # Dans cet exemple, nous utilisons une fonction "get_theme_from_storage" définie dans la classe AdvancedCMD
        theme = self.parent().get_theme_from_storage(theme_name)
        if theme:
            self.parent().apply_theme(theme)
            self.close()
        else:
            QMessageBox.warning(self, "Erreur", "Le thème sélectionné n'a pas pu être chargé.")


class AdvancedCMD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AdvancedCMD | Made by Kod3ra | V1.0.0")
        self.resize(1000, 600)  # Taille de la fenêtre

        # Création de la barre d'entrée
        self.input_line = QLineEdit()
        self.input_line.returnPressed.connect(self.execute_command)

        # Création du carré de sortie
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)

        # Création de la barre latérale
        self.sidebar = QGroupBox("Options")
        self.sidebar_layout = QVBoxLayout()

        # Bouton pour changer la couleur de fond de l'interface
        self.interface_background_button = QPushButton("Background color")
        self.interface_background_button.clicked.connect(self.change_interface_background_color)
        self.sidebar_layout.addWidget(self.interface_background_button)

        # Bouton pour changer la couleur de fond de l'input
        self.input_background_button = QPushButton("Input background color")
        self.input_background_button.clicked.connect(self.change_input_background_color)
        self.sidebar_layout.addWidget(self.input_background_button)

        # Bouton pour changer la couleur de fond de l'output
        self.output_background_button = QPushButton("Output background color")
        self.output_background_button.clicked.connect(self.change_output_background_color)
        self.sidebar_layout.addWidget(self.output_background_button)

        # Bouton pour changer la couleur du texte de l'input
        self.input_text_color_button = QPushButton("Input text color")
        self.input_text_color_button.clicked.connect(self.change_input_text_color)
        self.sidebar_layout.addWidget(self.input_text_color_button)

        # Bouton pour changer la couleur du texte de l'output
        self.output_text_color_button = QPushButton("Output text color")
        self.output_text_color_button.clicked.connect(self.change_output_text_color)
        self.sidebar_layout.addWidget(self.output_text_color_button)

        # Bouton pour gérer les thèmes
        self.theme_button = QPushButton("Themes")
        self.theme_button.clicked.connect(self.show_theme_dialog)
        self.sidebar_layout.addWidget(self.theme_button)

        self.sidebar.setLayout(self.sidebar_layout)

        # Configuration du layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.output_box)
        layout.addWidget(self.input_line)

        # Ajout de la barre latérale au layout principal
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addLayout(layout)

        # Configuration du widget central
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def execute_command(self):
        command = self.input_line.text()

        output = self.run_command(command)

        self.output_box.append(f"> {command}")
        if output:
            self.output_box.append(output)

        self.input_line.clear()

    def run_command(self, command):
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        output, _ = process.communicate()

        return output

    def change_interface_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            palette = self.palette()
            palette.setColor(QPalette.Window, color)
            self.setPalette(palette)

    def change_input_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            palette = self.input_line.palette()
            palette.setColor(QPalette.Base, color)
            self.input_line.setPalette(palette)

    def change_output_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            palette = self.output_box.palette()
            palette.setColor(QPalette.Base, color)
            self.output_box.setPalette(palette)

    def change_input_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            palette = self.input_line.palette()
            palette.setColor(QPalette.Text, color)
            self.input_line.setPalette(palette)

    def change_output_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            palette = self.output_box.palette()
            palette.setColor(QPalette.Text, color)
            self.output_box.setPalette(palette)

    def show_theme_dialog(self):
        dialog = ThemeDialog(self)
        dialog.exec_()

    def get_theme_from_storage(self, theme_name):
        # Récupérer le thème à partir de votre source de stockage en utilisant le nom du thème
        # Dans cet exemple, nous renvoyons simplement un thème prédéfini en fonction du nom
        if theme_name == "Theme 1":
            return {
                "interface_background": "#FFFFFF",
                "input_background": "#F7F7F7",
                "output_background": "#F7F7F7",
                "input_text_color": "#000000",
                "output_text_color": "#000000",
            }
        elif theme_name == "Theme 2":
            return {
                "interface_background": "#000000",
                "input_background": "#333333",
                "output_background": "#333333",
                "input_text_color": "#FFFFFF",
                "output_text_color": "#FFFFFF",
            }
        elif theme_name == "Theme 3":
            return {
                "interface_background": "#ECECEC",
                "input_background": "#D9D9D9",
                "output_background": "#D9D9D9",
                "input_text_color": "#000000",
                "output_text_color": "#000000",
            }
        else:
            return None

    def apply_theme(self, theme):
        interface_background = QColor(theme["interface_background"])
        input_background = QColor(theme["input_background"])
        output_background = QColor(theme["output_background"])
        input_text_color = QColor(theme["input_text_color"])
        output_text_color = QColor(theme["output_text_color"])

        palette = self.palette()
        palette.setColor(QPalette.Window, interface_background)
        self.setPalette(palette)

        input_palette = self.input_line.palette()
        input_palette.setColor(QPalette.Base, input_background)
        input_palette.setColor(QPalette.Text, input_text_color)
        self.input_line.setPalette(input_palette)

        output_palette = self.output_box.palette()
        output_palette.setColor(QPalette.Base, output_background)
        output_palette.setColor(QPalette.Text, output_text_color)
        self.output_box.setPalette(output_palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdvancedCMD()
    window.show()
    sys.exit(app.exec_())
