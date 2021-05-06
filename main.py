""" Simple editor for logical schemes based qt5. """
import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QRect, QSize
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QMessageBox, QWidget
from PyQt5.QtGui import QIcon, QPainter, QColor, QBrush, QImage, QMouseEvent, QPaintEvent

from circuit import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._create_ui()
        self.show()

    def run_circuit(self):
        print("Run circuit")

    def add_operator_not(self):
        self.circuit.add_element(ElementTypes.NOT)

    def add_operator_or(self):
        self.circuit.add_element(ElementTypes.OR)

    def add_operator_and(self):
        self.circuit.add_element(ElementTypes.AND)

    def add_input(self):
        self.circuit.add_element(ElementTypes.INPUT)

    def new_project(self):
        print("New Project")

    def save_project(self):
        print("Save Project")

    def save_project_as(self):
        print("Save Project as")

    def open_project(self):
        print("Open Project")

    def exit_app(self):
        print("Exit App")
        qApp.quit()

    def about_app(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("About")
        message_box.setText("Combinational Circuit Editor.\nLicense: GNU GPLv3\nhttps://github.com/dovydenkovas/Combinational-Circuit-Editor")
        message_box.exec()

    def _create_menu_bar(self):
        new_project_action = QAction('&New', self)
        new_project_action.setShortcut('Ctrl+N')
        new_project_action.setStatusTip('New')
        new_project_action.triggered.connect(self.new_project)

        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save')
        save_action.triggered.connect(self.save_project)

        save_as_action = QAction('&Save as...', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.setStatusTip('Save as')
        save_as_action.triggered.connect(self.save_project_as)

        open_action = QAction('&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open')
        open_action.triggered.connect(self.open_project)

        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.exit_app)

        about_action = QAction('&About', self)
        about_action.setShortcut('F1')
        about_action.setStatusTip('About application')
        about_action.triggered.connect(self.about_app)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(new_project_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        about_menu = menubar.addMenu('&About')
        about_menu.addAction(about_action)

    def _create_tool_bar(self):
        run_action = QAction(QIcon("images/run.png"), 'Run', self)
        run_action.setShortcut('Ctrl+R')
        run_action.triggered.connect(self.run_circuit)

        and_action = QAction(QIcon("images/and.bmp"), 'and', self)
        and_action.setShortcut('Ctrl+A')
        and_action.triggered.connect(self.add_operator_and)

        or_action = QAction(QIcon("images/or.bmp"), 'or', self)
        or_action.setShortcut('Ctrl+R')
        or_action.triggered.connect(self.add_operator_or)

        not_action = QAction(QIcon("images/not.bmp"), 'not', self)
        not_action.setShortcut('Ctrl+N')
        not_action.triggered.connect(self.add_operator_not)

        input_action = QAction(QIcon("images/input.png"), 'input', self)
        input_action.setShortcut('Ctrl+I')
        input_action.triggered.connect(self.add_input)

        self.toolbar = self.addToolBar('Tools')
        self.toolbar.setIconSize(QSize(40, 40))
        self.toolbar.addAction(run_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(input_action)
        self.toolbar.addAction(and_action)
        self.toolbar.addAction(or_action)
        self.toolbar.addAction(not_action)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)

    def _create_ui(self):
        self.setWindowTitle("Combinational Circuit Editor")
        self.resize(800, 600)
        self._create_menu_bar()
        self._create_tool_bar()
        self.circuit = Circuit()
        self.setCentralWidget(self.circuit)
        self.statusBar()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.circuit.keyPressEvent(a0)
        super().keyPressEvent(a0)

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.circuit.keyReleaseEvent(a0)
        super().keyPressEvent(a0)


if __name__ == "__main__":
    boolean_editor = QApplication(sys.argv)
    boolean_editor.setWindowIcon(QIcon("images/run.png"))
    window = MainWindow()
    boolean_editor.exec()
