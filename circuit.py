from PyQt5 import QtCore, QtGui
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
        self.elements = []
        self.lines = []
        self.selected_element = -1
        self.selected_element_dpos = [0, 0]
        self.is_ctrl = False
        self.add_connection_img = QImage("images/add_connection.png")
        self.rem_connection_img = QImage("images/rem_connection.png")
        self.is_mouse_pressed = False

        # Example:
        self.add_element(ElementTypes.INPUT, 60, 100)
        self.add_element(ElementTypes.INPUT, 60, 200)
        self.add_element(ElementTypes.AND, 250, 120)
        self.add_connection(0, "o", 2, "i1")
        self.add_connection(1, "o", 2, "i2")
        self.setMouseTracking(True)

    def add_connection(self, id1, port1, id2, port2):
        is_added = False
        line = Line(id1, id2, port1, port2)
        line_id = len(self.lines)

        for i in range(len(self.lines)):
            if self.lines[i] is None:
                self.lines[i] = line
                line_id = i
                is_added = True
                break
        if not is_added:
            self.lines.append(line)

        self.elements[id1].connections[port1] = line_id
        self.elements[id2].connections[port2] = line_id
        self.repaint()

    def remove_connection(self, element_id, port):
        """ Delete line between elements """
        if element_id != -1 and self.elements[element_id] is not None:  # if id is valid
            line_id = self.elements[element_id].connections[port]  # get line id
            if self.lines[line_id] is not None:
                id = self.lines[line_id].elements[0]
                second_element_id = id if id != element_id else self.lines[line_id].elements[1]
                second_element_port = self.lines[line_id].ports[0] if id != element_id else self.lines[line_id].ports[1]
                self.elements[element_id].connections[port] = -1
                self.elements[second_element_id].connections[second_element_port] = -1
                self.lines[line_id] = None
        self.repaint()

    def add_element(self, element_type, x=20, y=20):
        is_added = False
        for i in range(len(self.elements)):
            if self.elements[i] is None:
                self.elements[i] = Element(element_type, x, y)
                is_added = True
                break
        if not is_added:
            self.elements.append(Element(element_type, x, y))
        self.repaint()

    def remove_element(self, id: int):
        self.remove_connection(id, 'i1')
        self.remove_connection(id, 'i2')
        self.remove_connection(id, 'o')
        self.elements[id] = None
        self.selected_element = -1
        self.repaint()

    def paintEvent(self, a0: QPaintEvent) -> None:
        """ Draw elements. """
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        qp.setBackground(QBrush(QColor(255, 255, 255)))
        for line in self.lines:
            if line is not None:
                id_1 = line.elements[0]
                port_1 = line.ports[0]
                point_1 = self.elements[id_1].get_connection_point(port_1)

                id_2 = line.elements[1]
                port_2 = line.ports[1]
                point_2 = self.elements[id_2].get_connection_point(port_2)

                qp.drawLine(*point_1, point_1[0], point_2[1])
                qp.drawLine(point_1[0], point_2[1], *point_2)

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
                                print(f"create connection from {port}")
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
            self.is_ctrl = False
        self.repaint()
        super().keyPressEvent(a0)