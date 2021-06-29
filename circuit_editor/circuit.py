from PyQt5 import QtCore, QtGui, Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QMouseEvent, QPaintEvent

from elements import *


class Circuit(QWidget):
    """ class Circuit is class of circuit field.
        It calculate events like selecting, moving, adding, removing elements and connection
        and calculate signals in run mode.
    """

    def __init__(self):
        super(Circuit, self).__init__()
        self.setAttribute(Qt.Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: white;')
        self.elements = []
        self.lines = []
        self.selected_element = -1
        self.selected_element_dpos = [0, 0]
        self.is_ctrl = False
        self.add_connection_img = QImage("images/add_connection.png")
        self.rem_connection_img = QImage("images/rem_connection.png")
        self.is_mouse_pressed = False
        self.new_line = {"id1": None,
                         "port1": None,
                         "id2": None,
                         "port2": None
                         }
        self.setMouseTracking(True)

        # # Example:
        # self.add_element(ElementTypes.INPUT, 60, 100)
        # self.add_element(ElementTypes.INPUT, 60, 200)
        # self.add_element(ElementTypes.AND, 250, 120)
        # self.add_connection(0, "o", 2, "i1")
        # self.add_connection(1, "o", 2, "i2")


    def add_connection(self, id1, port1, id2, port2):
        line = Line(id1, id2, port1, port2)

        for i in range(len(self.lines)):
            if self.lines[i] is None:
                self.lines[i] = line
                line_id = i
                break
        else:
            line_id = len(self.lines)
            self.lines.append(line)

        self.elements[id1].connections[port1] = line_id
        self.elements[id2].connections[port2] = line_id
        self.repaint()

    def remove_connection(self, element_id, port):
        """ Delete line between elements """
        if element_id == -1 or element_id >= len(self.elements) or \
           self.elements[element_id] is None:
            return

        line_id = self.elements[element_id].connections[port]  # get line id
        if line_id < 0 or line_id >= len(self.lines) or self.lines[line_id] is None:
            return

        id = self.lines[line_id].elements[0]
        if id != element_id:
            second_element_id = id
            second_element_port = self.lines[line_id].ports[0]
        else:
            self.lines[line_id].elements[1]
            second_element_port = self.lines[line_id].ports[1]

        self.elements[element_id].connections[port] = -1
        self.elements[second_element_id].connections[second_element_port] = -1
        self.lines[line_id] = None
        self.repaint()

    def add_element(self, element_type, x=20, y=20):
        for i in range(len(self.elements)):
            if self.elements[i] is None:
                self.elements[i] = Element(element_type, x, y)
                break
        else:
            self.elements.append(Element(element_type, x, y))
        self.repaint()

    def remove_element(self, id: int):
        self.remove_connection(id, 'o')
        if self.elements[id].element_type != ElementTypes.INPUT:
            self.remove_connection(id, 'i1')
            if self.elements[id].element_type != ElementTypes.NOT:
                self.remove_connection(id, 'i2')

        self.elements[id] = None
        self.selected_element = -1
        self.repaint()

    def draw_line(self, x1, y1, x2, y2, qp):
        qp.drawLine(x1, y1, (x1 + x2) // 2, y1)
        qp.drawLine((x1 + x2) // 2, y1, (x1 + x2) // 2, y2)
        qp.drawLine((x1 + x2) // 2, y2, x2, y2)

    def paintEvent(self, a0: QPaintEvent) -> None:
        """ Draw elements. """
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        qp.setBackground(QBrush(QColor(255, 255, 255)))
        for line in self.lines:
            if line is not None:
                point_1 = self.elements[line.elements[0]].get_connection_point(line.ports[0])
                point_2 = self.elements[line.elements[1]].get_connection_point(line.ports[1])
                self.draw_line(*point_1, *point_2, qp)

        for element in self.elements:
            if element is not None:
                element.draw(qp)
                if self.is_ctrl:
                    for port in element.connections:
                        point = element.get_connection_point(port)
                        qp.drawImage(point[0] - 15, point[1] - 15,
                                     self.add_connection_img if element.connections[port] == -1 else self.rem_connection_img)
        qp.end()

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        self.is_mouse_pressed = False

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        """ Check for trying select object or create/remove connection. """
        self.is_mouse_pressed = True
        is_find = False
        x, y = a0.x(), a0.y()
        for i in range(len(self.elements)):
            if self.elements[i] is not None:
                if self.is_ctrl:
                    # Check for add or remove connection
                    for port in self.elements[i].connections:
                        point = self.elements[i].get_connection_point(port)
                        if abs(point[0] - x) < 15 and abs(point[1] - y) < 15:
                            if self.elements[i].connections[port] != -1:
                                 self.remove_connection(i, port)
                            else:
                                if self.new_line["id1"] is not None:
                                    self.new_line["id2"] = i
                                    self.new_line["port2"] = port
                                    self.add_connection(**self.new_line)
                                    self.new_line = {item: None for item in self.new_line}
                                else:
                                    self.new_line["id1"] = i
                                    self.new_line["port1"] = port
                            is_find = True
                elif self.elements[i].is_clicked(x, y):
                    # Select element
                    if self.selected_element > -1:
                        self.elements[self.selected_element].state = ElementState.DEFAULT
                    self.selected_element = i
                    self.elements[self.selected_element].state = ElementState.CHOOSING
                    is_find = True
                if is_find:
                    break

        # If click to air: remove selection.
        if not self.is_ctrl and not is_find and self.selected_element > -1:
            self.elements[self.selected_element].state = ElementState.DEFAULT
            self.selected_element = -1

        # Change the offset of the click relative to the object to move it correct.
        if self.selected_element > -1:
            self.selected_element_dpos[0] = a0.x() - self.elements[self.selected_element].x
            self.selected_element_dpos[1] = a0.y() - self.elements[self.selected_element].y

        self.repaint()
        super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        """ Move selected element. """
        if self.is_mouse_pressed and not self.is_ctrl and self.selected_element > -1:
            i = self.selected_element
            self.elements[i].x = a0.x() - self.selected_element_dpos[0]
            self.elements[i].y = a0.y() - self.selected_element_dpos[1]
            self.repaint()
        #super().mouseMoveEvent(a0)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key_Delete:
            # Delete selected element
            if self.selected_element > -1:
                self.remove_element(self.selected_element)

        elif a0.key() == QtCore.Qt.Key_Control:
            self.is_ctrl = True
        self.repaint()
        super().keyPressEvent(a0)

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key_Control:
            self.new_line = {item: None for item in self.new_line}
            self.is_ctrl = False

        self.repaint()
        super().keyPressEvent(a0)
