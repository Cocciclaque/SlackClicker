import random
import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from PyQt5.QtGui import QPixmap, QGuiApplication, QColor, QFont


class DesktopPet(QWidget):
    def __init__(self, image_path, hangup_path='hang_up.png'):
        super().__init__()
        self.answered = False
        self.current_message = ""
        self.speech_buble = None
        self.current_index = 0
        # Load sprites from files
        if not os.path.exists(image_path):
            print(f"Error: Image file not found: {image_path}")
            sys.exit(1)
        if not os.path.exists(hangup_path):
            print(f"Error: Hang-up image file not found: {hangup_path}")
            sys.exit(1)
        self.call_pixmap = QPixmap(image_path)
        self.hangup_pixmap = QPixmap(hangup_path)
        if self.call_pixmap.isNull() or self.hangup_pixmap.isNull():
            print("Error: Failed to load one of the images.")
            sys.exit(1)

        # Pixel-perfect upscale of icons
        self.scale_factor = 5  # scale original image by 5x
        def upscale(pix):
            w, h = pix.width(), pix.height()
            return pix.scaled(w * self.scale_factor, h * self.scale_factor,
                               Qt.KeepAspectRatio, Qt.FastTransformation)
        self.call_pixmap = upscale(self.call_pixmap)
        self.hangup_pixmap = upscale(self.hangup_pixmap)

        # Window setup
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Label for the call icon
        self.label = QLabel(self)
        self.label.setPixmap(self.call_pixmap)
        self.label.resize(self.call_pixmap.size())
        self.resize(self.call_pixmap.size())

        # Compute bottom-edge click threshold in widget coords
        # Only clicks in bottom 12px of original image (scaled)
        self.bottom_click_threshold = self.height() - (12 * self.scale_factor)

        # Determine animation start and end positions
        screen = QGuiApplication.primaryScreen().availableGeometry()
        margin_x, margin_y = 20, 50
        end_x = screen.x() + screen.width() - self.width() - margin_x
        end_y = screen.y() + screen.height() - self.height() - margin_y
        start_pos = QPoint(end_x, end_y + self.height() + 20)
        self.base_pos = QPoint(end_x, end_y)

        # Place off-screen and animate entry
        self.move(start_pos)
        self.anim = QPropertyAnimation(self, b"pos", self)
        self.anim.setDuration(300)
        self.anim.setStartValue(start_pos)
        self.anim.setEndValue(self.base_pos)
        self.anim.finished.connect(self.start_vibration)
        self.anim.start()

        # Vibration timer
        self.vib_timer = QTimer(self)
        self.vib_timer.setInterval(100)
        self.vib_timer.timeout.connect(self.vibrate)

        # Drag support
        self._drag_offset = None
        self._dragging = False

        # Bubble setup
        self.bubble_timer = QTimer(self)
        self.bubble_timer.timeout.connect(self.show_speech_bubble)

        # Track the bubble for hiding/showing
        self.speech_bubble = None

    def start_vibration(self):
        if not self.answered:
            self.vib_timer.start()

    def vibrate(self):
        dx = random.randint(-3, 3)
        dy = random.randint(-3, 3)
        self.move(self.base_pos.x() + dx, self.base_pos.y() + dy)

    def stop_vibration(self):
        self.vib_timer.stop()
        self.move(self.base_pos)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Start dragging
            self._drag_offset = event.globalPos() - self.frameGeometry().topLeft()
            self._dragging = False
            # Hide speech bubble when dragging starts
            if self.speech_bubble:
                self.speech_bubble.hide()

    def mouseMoveEvent(self, event):
        if self._drag_offset is not None:
            # Continue dragging
            self._dragging = True
            new_pos = event.globalPos() - self._drag_offset
            self.base_pos = new_pos  # update base_pos so vibration resets here
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.answered:
                self.show_speech_bubble(self.current_message)
            if self._dragging:
                # End dragging
                self._drag_offset = None
                self._dragging = False
                # Recreate and show the speech bubble when drag ends
            else:
                # Click on the bottom of the window to answer
                if event.pos().y() >= self.bottom_click_threshold:
                    if not self.answered:
                        self.answer_call()
                    else:
                        QApplication.quit()
                self._drag_offset = None

    def answer_call(self):
        # Answer the call: stop shaking and switch to hang-up sprite
        self.answered = True
        self.stop_vibration()
        screen = QGuiApplication.primaryScreen().availableGeometry()

        self.label.setPixmap(self.hangup_pixmap)
        self.label.resize(self.hangup_pixmap.size())
        self.resize(self.hangup_pixmap.size())
        self.move(screen.width()//2, screen.height()//2)

        # Recompute bottom threshold and reposition
        self.bottom_click_threshold = self.height() - (12 * self.scale_factor)
        margin_x, margin_y = 20, 50
        end_x = screen.x() + screen.width() - self.width() - margin_x
        end_y = screen.y() + screen.height() - self.height() - margin_y
        self.base_pos = QPoint(end_x, end_y)

        # Start showing speech bubbles periodically
        self.show_speech_bubble("Thanks for answering, I've been waiting to call you for ages\n tralilero tralala")
    def show_speech_bubble(self, text="Hello!"):
        if self.answered:  # Only show speech bubble if call is answered
            self.current_message = text
            self.current_index = 0  # Reset index for progressive display

            # Display specified text in the speech bubble
            if self.speech_bubble is None:
                self.speech_bubble = QLabel(self)
                self.speech_bubble.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip)
                self.speech_bubble.setAttribute(Qt.WA_TranslucentBackground, False)
                self.speech_bubble.setStyleSheet("""
                    background-color: white;
                    color: black;
                    border: 2px solid #333;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 25px;
                    font-weight: bold;
                """)

            # Initialize or reset the text being displayed progressively
            self.speech_bubble.setText("")
            self.speech_bubble.adjustSize()  # Adjust size here only once, when initializing the bubble

            # Position the speech bubble relative to the pet's position
            pet_top_left = self.rect().topLeft()
            bw, bh = self.speech_bubble.width(), self.speech_bubble.height()
            x = pet_top_left.x() + (self.width() - bw) // 2
            y = pet_top_left.y() - bh - 10  # Adjusted for positioning above the pet

            # Move the bubble relative to the widget's position
            self.speech_bubble.move(self.mapToGlobal(QPoint(x, y)))  # Correct positioning with widget's global position
            self.speech_bubble.show()

            # Start the progressive text reveal
            self.typing_timer = QTimer(self)
            self.typing_timer.setInterval(20)  # Adjust typing speed here
            self.typing_timer.timeout.connect(self.update_text)
            self.typing_timer.start()

    def update_text(self):
        if self.current_index < len(self.current_message):
            # Add one more character to the displayed text
            self.speech_bubble.setText(self.current_message[:self.current_index + 1])

            # Calculate the size based on text length
            self.speech_bubble.adjustSize()

            # Reposition the bubble to stay centered even as it expands
            pet_top_left = self.rect().topLeft()
            bw, bh = self.speech_bubble.width(), self.speech_bubble.height()
            x = pet_top_left.x() + (self.width() - bw) // 2
            y = pet_top_left.y() - bh - 10  # Adjusted for positioning above the pet
            self.speech_bubble.move(self.mapToGlobal(QPoint(x, y)))  # Reposition while expanding

            self.current_index += 1
        else:
            self.typing_timer.stop()  # Stop the timer once all text has been shown

        def remove_speech_bubble(self):
            # Remove the speech bubble when manually called
            if self.speech_bubble:
                self.speech_bubble.deleteLater()
                self.speech_bubble = None


def main():
    """Usage: python desktop_pet.py call.png hang_up.png"""
    app = QApplication(sys.argv)
    call_img = sys.argv[1] if len(sys.argv) > 1 else 'call.png'
    hangup_img = sys.argv[2] if len(sys.argv) > 2 else 'hang_up.png'
    pet = DesktopPet(call_img, hangup_img)
    pet.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
