"""
Compact Avatar - Small desktop pet that stays on screen when menu is closed
"""
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QPixmap
import os

class CompactAvatar(QWidget):
    """Small draggable avatar that acts as a desktop pet"""
    
    clicked = pyqtSignal()  # Signal when avatar is clicked (for chat bubble)
    moved = pyqtSignal(QPoint)  # Signal when avatar is moved (for chat bubble to follow)
    
    def __init__(self, assistant=None, image_path="image.png"):
        super().__init__()
        self.assistant = assistant
        self.image_path = image_path
        self.dragging = False
        self.offset = QPoint()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the compact avatar UI"""
        # Window flags for desktop pet behavior - higher z-index than menu
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.ToolTip  # Higher z-index
        )
        
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Avatar with custom image
        self.avatar_label = QLabel()
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setCursor(Qt.PointingHandCursor)
        
        # Load custom image
        if os.path.exists(self.image_path):
            pixmap = QPixmap(self.image_path)
            # Scale to 100x100 while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.avatar_label.setPixmap(scaled_pixmap)
            # Set widget size to match image
            self.setFixedSize(scaled_pixmap.width(), scaled_pixmap.height())
        else:
            # Fallback to text if image not found
            self.avatar_label.setText("🦊")
            from PyQt5.QtGui import QFont
            avatar_font = QFont("Arial", 48)
            self.avatar_label.setFont(avatar_font)
            self.setFixedSize(100, 100)
        
        layout.addWidget(self.avatar_label)
        self.setLayout(layout)
        
        # Styling - transparent background to show only the image
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
            QLabel {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Position in bottom-right by default
        self.position_default()
    
    def position_default(self):
        """Position in bottom-right corner"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen_geometry = QDesktopWidget().availableGeometry()
        x = screen_geometry.width() - self.width() - 100
        y = screen_geometry.height() - self.height() - 100
        self.move(x, y)
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging or clicking"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()
            self.drag_start_pos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if self.dragging:
            new_pos = event.globalPos() - self.offset
            self.move(new_pos)
            # Emit signal so chat bubble can follow
            self.moved.emit(self.pos())
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release - detect click vs drag"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            
            # If mouse didn't move much, treat as click
            if hasattr(self, 'drag_start_pos'):
                distance = (event.globalPos() - self.drag_start_pos).manhattanLength()
                if distance < 10:  # Small threshold for click detection
                    self.clicked.emit()
                    print("Avatar clicked - showing pet menu")
    
    def enterEvent(self, event):
        """Add hover effect - slightly increase opacity"""
        self.setWindowOpacity(0.95)
    
    def leaveEvent(self, event):
        """Remove hover effect"""
        self.setWindowOpacity(1.0)

