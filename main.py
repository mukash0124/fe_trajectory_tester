import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt, QPoint

possible_positions = [
    (95, 215),
    (135, 215),
    (495, 215),
    (535, 215),
    (95, 315),
    (135, 315),
    (495, 315),
    (535, 315),
    (95, 415),
    (135, 415),
    (495, 415),
    (535, 415),
    (215, 95),
    (215, 135),
    (215, 495),
    (215, 535),
    (315, 95),
    (315, 135),
    (315, 495),
    (315, 535),
    (415, 95),
    (415, 135),
    (415, 495),
    (415, 535),
]
colors = ["#ff0000", "#00ff00"]


def isPossiblePosition(point):
    for i in possible_positions:
        if (
            point.x() >= i[0]
            and point.x() <= i[0] + 10
            and point.y() >= i[1]
            and point.y() <= i[1] + 10
        ):
            return True, i
    return False, None


class QPaletteButton(QtWidgets.QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(24, 24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)


class Canvas(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()

        pixmap = QtGui.QPixmap("bg.png")
        self.setPixmap(pixmap)
        self.pen_color = QtGui.QColor("#ff0000")

        self.obstacles = []

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def mousePressEvent(self, e):
        isPossible, coords = isPossiblePosition(e.position())
        if isPossible:
            canvas = self.pixmap()
            painter = QtGui.QPainter(canvas)
            p = painter.pen()
            p.setWidth(4)
            p.setColor(self.pen_color)
            painter.setPen(p)
            painter.fillRect(coords[0], coords[1], 10, 10, self.pen_color)
            painter.end()
            self.setPixmap(canvas)

            self.obstacles.append((coords[0] + 5, coords[1] + 5))


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.canvas = Canvas()

        w = QtWidgets.QWidget()
        l = QtWidgets.QVBoxLayout()
        w.setLayout(l)
        l.addWidget(self.canvas)

        palette = QtWidgets.QHBoxLayout()
        self.add_palette_buttons(palette)
        l.addLayout(palette)

        self.setCentralWidget(w)

    def add_palette_buttons(self, layout):
        for c in colors:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.set_pen_color(c))
            layout.addWidget(b)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
