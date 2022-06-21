from PyQt6.QtWidgets import QMainWindow, QPushButton
from PyQt6.QtCore import QSize, Qt


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Organizer")
        button = QPushButton("Press Me!")

        # Set the central widget of the Window.
        self.setCentralWidget(button)
