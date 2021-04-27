""" Simple editor for logical schemes based qt5. """
import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QRect, QSize
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QMessageBox, QWidget
from PyQt5.QtGui import QIcon, QPainter, QColor, QBrush, QImage, QMouseEvent, QPaintEvent

from elements import *


class Line:
    def __init__(self):
        self.coordinates = []
        self.is_active = False


class Circuit(QWidget):
    def __init__(self):
        super(Circuit, self).__init__()
        self.elements = [Element(ElementTypes.OR, 40, 40), Element(ElementTypes.AND, 200, 40), Element(ElementTypes.NOT, 400, 40)]
        self.connect(0, "o", 1, "i2")
        self.connect(1, "o", 2, "i1")
        self.selected_element = -1
        self.selected_element_dpos = [0, 0]
        self.is_ctrl = False
        self.add_connection_img = QImage("images/add_connection.png")
        self.rem_connection_img = QImage("images/rem_connection.png")

    def paintEvent(self, a0: QPaintEvent) -> None:
        """ Draw elements. """
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        qp.setBackground(QBrush(QColor(255, 255, 255)))
        for element in self.elements:
            if element is not None:
                element.draw(qp)
                # Draw lines
                if element.connections["i1"] > -1:
                    qp.drawLine(
                        self.elements[element.connections["i1"]].x + self.elements[element.connections["i1"]].width,
                        self.elements[element.connections["i1"]].y + self.elements[
                            element.connections["i1"]].height // 4,
                        element.x,
                        element.y + element.height // 4, )
                if element.connections["i2"] > -1:
                    qp.drawLine(
                        self.elements[element.connections["i2"]].x + self.elements[element.connections["i2"]].width,
                        self.elements[element.connections["i2"]].y + self.elements[
                            element.connections["i2"]].height // 4,
                        element.x,
                        element.y + 3 * element.height // 4)
                if self.is_ctrl:
                    qp.drawImage(element.x - 15, element.y + element.height // 4 - 15,
                                 self.add_connection_img if element.connections[
                                                                "i1"] == -1 else self.rem_connection_img)
                    qp.drawImage(element.x + element.width - 15, element.y + element.height // 4 - 15,
                                 self.add_connection_img if element.connections["o"] == -1 else self.rem_connection_img)
                    if element.element_type != ElementTypes.NOT:
                        qp.drawImage(element.x - 15, element.y + 3 * element.height // 4 - 15,
                                     self.add_connection_img if element.connections[
                                                                    "i2"] == -1 else self.rem_connection_img)

        qp.end()

    def connect(self, id1, port1, id2, port2):
        self.elements[id1].connections[port1] = id2
        self.elements[id2].connections[port2] = id1

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        """ Select element to move. """
        is_find = False
        x, y = a0.x(), a0.y()
        for i in range(len(self.elements)):
            if self.elements[i] is not None:
                if self.elements[i].x <= x <= self.elements[i].x + self.elements[i].width and \
                        self.elements[i].y <= y <= self.elements[i].y + self.elements[i].height:
                    if self.is_ctrl:
                        # Check for add connection
                        if abs(self.elements[i].x - x) < 15 and abs(self.elements[i].y + self.elements[i].height // 4 - y) < 15:
                            print("i1")
                        if self.elements[i].element_type != ElementTypes.NOT and abs(self.elements[i].x - x) < 15 and \
                                abs(self.elements[i].y + 3 * self.elements[i].height // 4 - y) < 15:
                            print("i2")
                        if abs(self.elements[i].x + self.elements[i].width - x) < 15 and \
                            abs(self.elements[i].y + self.elements[i].height // 4 - y) < 15:
                            print("o")
                    else:
                        # Select element
                        if self.selected_element > -1:
                            self.elements[self.selected_element].state = ElementState.DEFAULT
                        self.selected_element = i
                        self.elements[self.selected_element].state = ElementState.CHOOSING
                    is_find = True
                    break

        if not is_find and self.selected_element > -1 and not self.is_ctrl:
            self.elements[self.selected_element].state = ElementState.DEFAULT
            self.selected_element = -1

        if self.selected_element > -1:
            self.selected_element_dpos[0] = a0.x() - self.elements[self.selected_element].x
            self.selected_element_dpos[1] = a0.y() - self.elements[self.selected_element].y
        self.repaint()
        super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        """ Move selected element. """
        if not self.is_ctrl and self.selected_element > -1:
            i = self.selected_element
            self.elements[i].x = a0.x() - self.selected_element_dpos[0]
            self.elements[i].y = a0.y() - self.selected_element_dpos[1]
            self.repaint()
        #super().mouseMoveEvent(a0)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key_Delete:
            # Delete selected element
            if self.selected_element > -1:
                i = self.selected_element
                if self.elements[i].connections['i1'] != -1:
                    self.elements[self.elements[i].connections['i1']].connections['o'] = -1
                if self.elements[i].connections['i2'] != -1:
                    self.elements[self.elements[i].connections['i2']].connections['o'] = -1
                if self.elements[i].connections['o'] != -1:
                    if self.elements[self.elements[i].connections['o']].connections['i1'] == i:
                        self.elements[self.elements[i].connections['o']].connections['i1'] = -1
                    else:
                        self.elements[self.elements[i].connections['o']].connections['i1'] = -1
                self.elements[i] = None
                self.selected_element = -1
                self.repaint()

        elif a0.key() == QtCore.Qt.Key_Control:
            self.is_ctrl = True
        self.repaint()
        super().keyPressEvent(a0)

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key_Control:
            self.is_ctrl = False
        self.repaint()
        super().keyPressEvent(a0)

    def add_element(self, element_type):
        is_added = False
        for i in range(len(self.elements)):
            if self.elements[i] is None:
                self.elements[i] = Element(element_type, 20, 20)
                is_added = True
                break
        if not is_added:
            self.elements.append(Element(element_type, 20, 20))
        self.repaint()


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
