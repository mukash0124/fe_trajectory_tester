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

obstacles = [
    [120, 220],
    [520, 220],
    [120, 320],
    [520, 320],
    [120, 420],
    [520, 420],
    [220, 120],
    [220, 520],
    [320, 120],
    [320, 520],
    [420, 120],
    [420, 520],
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
        self.obstacles = [
            [120, 220],
            [120, 320],
            [120, 420],
            [220, 520],
            [320, 520],
            [420, 520],
            [520, 420],
            [520, 320],
            [520, 220],
            [420, 120],
            [320, 120],
            [220, 120],
        ]
        self.directionClockwise = True

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def findNearestPoint(self, coords):
        index = None
        for i in range(12):
            if (
                (
                    coords[0] == self.obstacles[i][0] - 20
                    or coords[0] == self.obstacles[i][0] + 20
                )
                and coords[1] == self.obstacles[i][1]
            ) or (
                (
                    coords[0] == self.obstacles[i][0] - 20
                    or coords[0] == self.obstacles[i][0] + 20
                )
                and coords[1] == self.obstacles[i][1]
            ):
                index = i
        return index

    def addOffset(self, coords):
        index = self.findNearestPoint(coords)
        if self.directionClockwise:
            if self.pen_color == QtGui.QColor("#ff0000"):
                if coords[0] <= 140 or coords[0] >= 500:
                    coords[0] += 20
                else:
                    coords[1] += 20
            else:
                if coords[0] <= 140 or coords[0] >= 500:
                    coords[0] -= 20
                else:
                    coords[1] -= 20
        else:
            if self.pen_color == QtGui.QColor("#ff0000"):
                if coords[0] <= 140 or coords[0] >= 500:
                    coords[0] -= 20
                else:
                    coords[1] -= 20
            else:
                if coords[0] <= 140 or coords[0] >= 500:
                    coords[0] += 20
                else:
                    coords[1] += 20
        self.obstacles[index] = coords

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

            self.addOffset([coords[0] + 5, coords[1] + 5])

    def build_trajectory(self):
        canvas = self.pixmap()
        painter = QtGui.QPainter(canvas)
        p = painter.pen()
        p.setWidth(4)
        p.setColor(QtGui.QColor("#000000"))
        painter.setPen(p)
        for i in range(len(self.obstacles)):
            painter.drawLine(
                QtCore.QPoint(self.obstacles[i - 1][0], self.obstacles[i - 1][1]),
                QtCore.QPoint(self.obstacles[i][0], self.obstacles[i][1]),
            )
        painter.end()
        self.setPixmap(canvas)


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

        build = QtWidgets.QPushButton()
        build.pressed.connect(self.canvas.build_trajectory)
        l.addWidget(build)

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
