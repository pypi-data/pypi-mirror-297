from PySide6.QtWidgets import QGraphicsView, QApplication
from PySide6.QtGui import QPainter, QWheelEvent
from PySide6.QtCore import Qt, Signal

class CustomGraphicsView(QGraphicsView):
    mouse_moved = Signal()  # Custom signal for mouse movement

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_graphics_view()

    def setup_graphics_view(self):
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMouseTracking(True)  # Enable mouse tracking

    def wheelEvent(self, event: QWheelEvent):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            # Zoom functionality when Ctrl is pressed
            zoom_factor = 1.02
            self.scale(zoom_factor ** (event.angleDelta().y() / 120), zoom_factor ** (event.angleDelta().y() / 120))
        else:
            # Scroll functionality
            scroll_factor = 0.1
            delta = event.angleDelta()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x() * scroll_factor)
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y() * scroll_factor)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.mouse_moved.emit()  # Emit the custom signal when mouse moves