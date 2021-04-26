""" Simple editor for logical schemes based qt5. """
import sys
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QMessageBox, QWidget
from PyQt5.QtGui import QIcon, QPainter, QColor, QBrush, QImage, QMouseEvent, QPaintEvent


class Element:
    # types of element
    OR = 0
    AND = 1
    NOT = 2

    def __init__(self, element_type, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.element_type = element_type

    def draw(self, qpainter):
        """ Draw Element. """
        qpainter.drawImage(QRect(self.x, self.y, self.width, self.height), QImage("images/AND2.bmp"))


class Circuit(QWidget):
    def __init__(self):
        super(Circuit, self).__init__()
        self.elements = [Element(Element.AND, 10, 10)]
        self.selected_element = -1
        self.selected_element_dpos = [0, 0]

    def paintEvent(self, a0: QPaintEvent) -> None:
        """ Draw elements. """
        qp = QPainter()
        qp.begin(self)
        qp.setBackground(QBrush(QColor(255, 255, 255)))
        for element in self.elements:
            element.draw(qp)
        qp.end()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        """ Select element to move. """
        x, y = a0.x(), a0.y()
        for i in range(len(self.elements)):
            if self.elements[i].x <= x <= self.elements[i].x + self.elements[i].width and \
                    self.elements[i].y <= y <= self.elements[i].y + self.elements[i].height:
                self.selected_element = i
                self.selected_element_dpos[0] = x - self.elements[i].x
                self.selected_element_dpos[1] = y - self.elements[i].y
                break
        super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        """ Move selected element. """
        if self.selected_element > -1:
            i = self.selected_element
            self.elements[i].x = a0.x() - self.selected_element_dpos[0]
            self.elements[i].y = a0.y() - self.selected_element_dpos[1]
            self.repaint()
        super().mouseMoveEvent(a0)

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        """ Stop moving selected element. """
        self.selected_element = -1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._create_ui()
        self.show()

    def run_circuit(self):
        print("Run circuit")

    def add_operator_not(self):
        print("add operator not")

    def add_operator_or(self):
        print("add operator or")

    def add_operator_and(self):
        print("add operator and")

    def add_input(self):
        print("add input")

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
        run_action = QAction('Run', self)
        run_action.setShortcut('Ctrl+R')
        run_action.triggered.connect(self.run_circuit)

        and_action = QAction('and', self)
        and_action.setShortcut('Ctrl+A')
        and_action.triggered.connect(self.add_operator_and)

        or_action = QAction('or', self)
        or_action.setShortcut('Ctrl+R')
        or_action.triggered.connect(self.add_operator_or)

        not_action = QAction('not', self)
        not_action.setShortcut('Ctrl+N')
        not_action.triggered.connect(self.add_operator_not)

        input_action = QAction('input', self)
        input_action.setShortcut('Ctrl+I')
        input_action.triggered.connect(self.add_input)

        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(run_action)
        self.toolbar.addAction(input_action)
        self.toolbar.addAction(and_action)
        self.toolbar.addAction(or_action)
        self.toolbar.addAction(not_action)

    def _create_ui(self):
        self.setWindowTitle("Combinational Circuit Editor")
        self.resize(800, 600)
        self._create_menu_bar()
        self._create_tool_bar()
        self.scheme = Circuit()
        self.setCentralWidget(self.scheme)
        self.statusBar()


if __name__ == "__main__":
    boolean_editor = QApplication(sys.argv)
    window = MainWindow()
    boolean_editor.exec()
