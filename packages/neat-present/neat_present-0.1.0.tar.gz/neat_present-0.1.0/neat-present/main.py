import sys
import os
import logging
import json
import base64
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog, QLabel, QStatusBar, QComboBox
from PySide6.QtGui import QPixmap, QTransform, QImage
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPointF, QTimer, QByteArray, QBuffer

from custom_graphics_view import CustomGraphicsView
from utils import save_state, load_state, log_session

class ImagePresenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_variables()
        self.setup_connections()
        self.load_last_state()
        self.update_window_title()  # Set initial window title

    def setup_ui(self):
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.top_bar = QWidget()
        self.top_layout = QVBoxLayout(self.top_bar)
        self.controls_layout = QHBoxLayout()
        self.top_layout.addLayout(self.controls_layout)
        
        self.load_button = self.create_button("Load Image/Presentation", self.load_image)
        self.save_button = self.create_button("Save Presentation", self.save_presentation)
        
        self.recent_files_dropdown = QComboBox()
        self.recent_files_dropdown.setFixedWidth(200)
        self.recent_files_dropdown.addItem("Recent Files")
        self.recent_files_dropdown.currentIndexChanged.connect(self.load_recent_file)
        self.controls_layout.addWidget(self.recent_files_dropdown)
        
        self.instructions_label = QLabel("S: Set point | Enter/N: Next point | Backspace/P: Previous point R: Reset view | Mouse wheel: Scroll | Ctrl + Mouse wheel: Zoom | Mouse drag: Pan")
        self.top_layout.addWidget(self.instructions_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.top_bar)

        self.graphics_view = CustomGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        self.layout.addWidget(self.graphics_view)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.setMouseTracking(True)
        self.graphics_view.setMouseTracking(True)

    def create_button(self, text, callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        self.controls_layout.addWidget(button)
        return button

    def setup_variables(self):
        self.image_item = None
        self.presentation_points = []
        self.current_point_index = -1
        self.image_format = None
        self.last_accessed_folder = None
        self.recent_files = []
        self.current_file_path = None  # Add this line to store the current file path

        self.animation = QPropertyAnimation(self, b"")
        self.setup_animation(self.animation)

        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide_top_bar_and_cursor)

    def setup_animation(self, animation):
        animation.setDuration(500)  # 500 ms for the animation
        animation.setEasingCurve(QEasingCurve.InOutCubic)

    def setup_connections(self):
        self.graphics_view.mouse_moved.connect(self.on_mouse_move)

    def load_last_state(self):
        state = load_state()
        last_opened_file = state.get("last_opened_file")
        self.last_accessed_folder = state.get("last_accessed_folder")
        self.recent_files = state.get("recent_files", [])
        self.update_recent_files_dropdown()
        if last_opened_file and os.path.exists(last_opened_file):
            if last_opened_file.lower().endswith('.neatp'):
                self.load_presentation(last_opened_file)
            else:
                self.load_image_file(last_opened_file)
            self.current_file_path = last_opened_file
            log_session(f"Loaded last opened file: {last_opened_file}")

    def update_recent_files_dropdown(self):
        self.recent_files_dropdown.clear()
        self.recent_files_dropdown.addItem("Recent Files")
        for file in self.recent_files:
            self.recent_files_dropdown.addItem(os.path.basename(file), file)

    def load_recent_file(self, index):
        if index > 0:  # 0 is the "Recent Files" placeholder
            file_path = self.recent_files_dropdown.itemData(index)
            self.load_file(file_path)
            self.recent_files_dropdown.setCurrentIndex(0)  # Reset to placeholder

    def add_to_recent_files(self, file_path):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:7]  # Keep only the last 7 files
        self.update_recent_files_dropdown()

    def start_hide_timer(self):
        self.hide_timer.start(5000)

    def hide_top_bar_and_cursor(self):
        self.top_bar.hide()
        QApplication.setOverrideCursor(Qt.BlankCursor)
        self.graphics_view.viewport().setCursor(Qt.BlankCursor)

    def show_top_bar_and_cursor(self):
        self.top_bar.show()
        QApplication.restoreOverrideCursor()
        self.graphics_view.viewport().unsetCursor()

    def on_mouse_move(self):
        self.show_top_bar_and_cursor()
        self.start_hide_timer()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.on_mouse_move()

    def toggle_hiding(self, enable):
        if enable:
            self.hide_timer.timeout.connect(self.hide_top_bar_and_cursor)
            self.graphics_view.mouse_moved.connect(self.on_mouse_move)
        else:
            self.hide_timer.timeout.disconnect(self.hide_top_bar_and_cursor)
            self.graphics_view.mouse_moved.disconnect(self.on_mouse_move)
            self.show_top_bar_and_cursor()

    def load_image(self):
        self.toggle_hiding(False)
        initial_dir = self.last_accessed_folder if self.last_accessed_folder else os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image or Presentation", initial_dir, """
                                                   All Supported Files (*.bmp *.gif *.jpg *.jpeg *.png *.pbm *.pgm *.ppm *.xbm *.xpm *.neatp);;
                                                   Images (*.bmp *.gif *.jpg *.jpeg *.png *.pbm *.pgm *.ppm *.xbm *.xpm);;
                                                   Neat Presentation (*.neatp)""")
        self.toggle_hiding(True)

        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        self.last_accessed_folder = os.path.dirname(file_path)
        self.scene.clear()
        try:
            if file_path.lower().endswith('.neatp'):
                self.load_presentation(file_path)
            else:
                self.load_image_file(file_path)
            
            self.graphics_view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
            self.update_status_bar()
            logging.info(f"Image/Presentation loaded: {file_path}")
            self.add_to_recent_files(file_path)
            save_state(file_path, self.last_accessed_folder, self.recent_files)
            log_session(f"Loaded file: {file_path}")
            self.current_file_path = file_path  # Update the current file path
            self.update_window_title()  # Update the window title
        except Exception as e:
            logging.error(f"Error loading image/presentation: {e}")
            log_session(f"Error loading file: {file_path}, Error: {str(e)}")

    def load_image_file(self, file_path):
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            raise Exception("Failed to load image:", file_path)
        self.image_item = self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(pixmap.rect())
        self.image_format = QImage(file_path).format()
        self.presentation_points = []
        self.current_point_index = -1

    def load_presentation(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        image_data = base64.b64decode(data['image_data'])
        image_format = data['image_format']
        
        pixmap = QPixmap()
        pixmap.loadFromData(image_data, image_format.upper())
        self.image_item = self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(pixmap.rect())
        
        self.image_format = image_format
        self.presentation_points = [
            (QPointF(point['x'], point['y']), QTransform(*point['transform']))
            for point in data['presentation_points']
        ]
        self.current_point_index = -1

    def save_presentation(self):
        if not self.image_item:
            logging.warning("No image loaded to save")
            return

        self.toggle_hiding(False)
        initial_dir = self.last_accessed_folder if self.last_accessed_folder else os.path.expanduser("~")
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Presentation", initial_dir, "Neat Presentation (*.neatp)")
        self.toggle_hiding(True)

        if file_path:
            self.last_accessed_folder = os.path.dirname(file_path)
            if not file_path.lower().endswith('.neatp'):
                file_path += '.neatp'
            try:
                image_data = self.encode_image_data()
                data = {
                    'image_format': self.image_format,
                    'image_data': base64.b64encode(image_data).decode('utf-8'),
                    'presentation_points': [
                        {
                            'x': point[0].x(),
                            'y': point[0].y(),
                            'transform': [
                                point[1].m11(), point[1].m12(), point[1].m13(),
                                point[1].m21(), point[1].m22(), point[1].m23(),
                                point[1].m31(), point[1].m32(), point[1].m33()
                            ]
                        }
                        for point in self.presentation_points
                    ]
                }

                with open(file_path, 'w') as f:
                    json.dump(data, f)

                logging.info(f"Presentation saved: {file_path}")
                self.add_to_recent_files(file_path)
                save_state(file_path, self.last_accessed_folder, self.recent_files)
                log_session(f"Saved presentation: {file_path}")
                self.current_file_path = file_path  # Update the current file path
                self.update_window_title()  # Update the window title
            except Exception as e:
                logging.error(f"Error saving presentation: {e}")
                log_session(f"Error saving presentation: {file_path}, Error: {str(e)}")

    def encode_image_data(self):
        image = self.image_item.pixmap().toImage()
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QBuffer.WriteOnly)
        image.save(buffer, self.image_format)
        return byte_array.data()

    def keyPressEvent(self, event):
        key_actions = {
            Qt.Key_S: self.set_presentation_point,
            Qt.Key_Enter: self.next_point,
            Qt.Key_Return: self.next_point,
            Qt.Key_N: self.next_point,
            Qt.Key_Backspace: self.previous_point,
            Qt.Key_P: self.previous_point,
            Qt.Key_R: self.reset_view
        }
        action = key_actions.get(event.key())
        if action:
            action()
            if event.key() not in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Backspace, Qt.Key_N, Qt.Key_P):
                self.show_top_bar_and_cursor()
                self.start_hide_timer()
        else:
            super().keyPressEvent(event)
            self.show_top_bar_and_cursor()
            self.start_hide_timer()

    def set_presentation_point(self):
        if self.image_item:
            center = self.graphics_view.mapToScene(self.graphics_view.viewport().rect().center())
            transform = self.graphics_view.transform()
            self.presentation_points.append((center, transform))
            self.current_point_index = len(self.presentation_points) - 1
            self.update_status_bar()
            logging.info(f"Presentation point set: {center}, transform: {transform}")
            log_session(f"Set presentation point: {len(self.presentation_points)}")

    def navigate_to_point(self, point):
        if point:
            end_center, end_transform = point
            start_center = self.graphics_view.mapToScene(self.graphics_view.viewport().rect().center())
            start_transform = self.graphics_view.transform()
            self.smooth_navigate_to_point(start_center, end_center, start_transform, end_transform)
            self.update_status_bar()

    def smooth_navigate_to_point(self, start_center, end_center, start_transform, end_transform):
        self.animation = QPropertyAnimation(self, b"")
        self.setup_animation(self.animation)

        def update_view(progress):
            t = progress / 100.0
            current_center = QPointF(
                (1 - t) * start_center.x() + t * end_center.x(),
                (1 - t) * start_center.y() + t * end_center.y()
            )
            current_transform = QTransform(
                (1 - t) * start_transform.m11() + t * end_transform.m11(),
                (1 - t) * start_transform.m12() + t * end_transform.m12(),
                (1 - t) * start_transform.m13() + t * end_transform.m13(),
                (1 - t) * start_transform.m21() + t * end_transform.m21(),
                (1 - t) * start_transform.m22() + t * end_transform.m22(),
                (1 - t) * start_transform.m23() + t * end_transform.m23(),
                (1 - t) * start_transform.m31() + t * end_transform.m31(),
                (1 - t) * start_transform.m32() + t * end_transform.m32(),
                (1 - t) * start_transform.m33() + t * end_transform.m33()
            )
            self.graphics_view.setTransform(current_transform)
            self.graphics_view.centerOn(current_center)

        self.animation.valueChanged.connect(update_view)
        self.animation.setStartValue(0)
        self.animation.setEndValue(100)
        self.animation.start()

    def next_point(self):
        self.navigate_to_next_point(1)

    def previous_point(self):
        self.navigate_to_next_point(-1)

    def navigate_to_next_point(self, direction):
        if self.presentation_points:
            self.current_point_index = (self.current_point_index + direction) % len(self.presentation_points)
            self.navigate_to_point(self.presentation_points[self.current_point_index])
            log_session(f"Navigated to point: {self.current_point_index + 1}")

    def reset_view(self):
        if self.image_item:
            self.graphics_view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
            self.update_status_bar()
            logging.info("View reset")
            log_session("View reset")

    def update_status_bar(self):
        if self.image_item:
            status = f"Points: {len(self.presentation_points)} | Current: {self.current_point_index + 1 if self.current_point_index >= 0 else 'None'}"
            self.status_bar.showMessage(status)

    def update_window_title(self):
        if self.current_file_path:
            self.setWindowTitle(f"{self.current_file_path} - Neat")
        else:
            self.setWindowTitle("Neat")

def main():
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Neat")
    app.setApplicationName("Neat")
    app.setApplicationVersion("0.0.1")
    window = ImagePresenter()
    window.show()
    log_session("Application started")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()