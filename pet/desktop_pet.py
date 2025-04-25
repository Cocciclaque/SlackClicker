#!/usr/bin/env python3
import random
import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from PyQt5.QtGui import QPixmap, QGuiApplication
import saveManager


class DesktopPet(QWidget):
    def __init__(self, image_path, hangup_path, lang):
        super().__init__()
        self.answered = False
        self.current_message = ""
        self.speech_bubble = None
        self.current_index = 0

        self.last_arg = ""

        self.receive = saveManager.SaveManager("comToPet.json")
        self.send = saveManager.SaveManager('comToMain.json')

        self.send.set('status', "")

        self.lang = saveManager.SaveManager(lang)
        self.lang.load()

        # Load sprites
        if not os.path.exists(image_path) or not os.path.exists(hangup_path):
            raise FileNotFoundError("Error: Image files not found!")
        self.call_pixmap = QPixmap(image_path)
        self.hangup_pixmap = QPixmap(hangup_path)
        if self.call_pixmap.isNull() or self.hangup_pixmap.isNull():
            raise ValueError("Error: Failed to load one of the images.")

        # Upscale icons
        self.scale_factor = 5
        def upscale(pix):
            return pix.scaled(pix.width()*self.scale_factor,
                               pix.height()*self.scale_factor,
                               Qt.KeepAspectRatio,
                               Qt.FastTransformation)
        self.call_pixmap = upscale(self.call_pixmap)
        self.hangup_pixmap = upscale(self.hangup_pixmap)

        # Window flags
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Icon label
        self.label = QLabel(self)
        self.label.setPixmap(self.call_pixmap)
        self.label.resize(self.call_pixmap.size())
        self.resize(self.call_pixmap.size())

        # Click threshold
        self.bottom_click_threshold = self.height() - (12 * self.scale_factor)

        # Animate in
        QTimer.singleShot(0, self._animate_in)

        # Vibration timer
        self.vib_timer = QTimer(self)
        self.vib_timer.setInterval(100)
        self.vib_timer.timeout.connect(self._vibrate)

        # Drag support
        self._drag_offset = None
        self._dragging = False

        self.loop_timer = QTimer(self)
        self.loop_timer.setInterval(16)               # ~60 updates per second
        self.loop_timer.timeout.connect(self.main_loop)
        self.loop_timer.start()


    def move(self, x, y=None):
        """
        Overrides QWidget.move to animate position changes smoothly.
        Accepts either move(QPoint) or move(x, y).
        """
        if isinstance(x, QPoint) and y is None:
            target = x
        elif isinstance(x, (int, float)) and isinstance(y, (int, float)):
            target = QPoint(int(x), int(y))
        else:
            return super().move(x, y)

        # Animate the position change
        anim = QPropertyAnimation(self, b"pos", self)
        anim.setDuration(200)  # milliseconds, adjust for speed
        anim.setStartValue(self.pos())
        anim.setEndValue(target)
        anim.start()
        # Keep reference to prevent garbage collection
        self._move_anim = anim
        # Update base_pos so vibration/rest logic uses new target
        self.base_pos = target

    def _animate_in(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        margin_x, margin_y = 20, 50
        end_x = screen.x() + screen.width() - self.width() - margin_x
        end_y = screen.y() + screen.height() - self.height() - margin_y
        start = QPoint(end_x, end_y + self.height() + 20)
        self.base_pos = QPoint(end_x, end_y)
        self.move(start)
        anim = QPropertyAnimation(self, b"pos", self)
        anim.setDuration(300)
        anim.setStartValue(start)
        anim.setEndValue(self.base_pos)
        anim.finished.connect(lambda: self.vib_timer.start())
        anim.start()

    def main_loop(self):
    # called roughly every 16 ms
    # you can do periodic checks, animations or random actions here
        try:      
            self.receive.load()
            self.send.load()
            
            if self.receive.get('running') is False:
                QApplication.exit()

            if self.receive.get('visible') is True:
                self.setWindowOpacity(1.0)
                try:
                    self.speech_bubble.setWindowOpacity(1.0)
                except:
                    pass
                    
            else: 
                self.setWindowOpacity(0)
                try:
                    self.speech_bubble.setWindowOpacity(0)
                except:
                    pass

            if self.answered:


                if self.last_arg != self.receive.get('args'):
                    self.last_arg = self.receive.get('args')
                    if self.receive.get('command') == "tutorial":
                        self.answer_call()
                    if self.receive.get('command') == "talk":
                        self._show_bubble(self.receive.get('args'))
                    elif self.receive.get('command') == "move":
                        self.speech_bubble.hide()
                        arg1, arg2 = self.receive.get('args').split("-")
                        coords = QPoint(int(arg1), int(arg2))
                        self.move(coords)
                        self.send.set('status','arrived')
                if self.receive.get('command') == "move" and (round(super().x) != int(self.receive.get('args').split('-')[0]) or round(super().y) != int(self.receive.get('args').split('-')[1])):
                    self.move(QPoint(int(self.receive.get('args').split('-')[0]), int(self.receive.get('args').split('-')[1]))) 
        except:
            pass

    def _vibrate(self):
        if not self.answered:
            dx = random.randint(-3, 0)
            dy = random.randint(-3, 0)
            self.move(self.base_pos + QPoint(dx, dy))
        else:
            # self.vib_timer.stop()
            self.move(self.base_pos)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag_offset = e.globalPos() - self.frameGeometry().topLeft()
            self._dragging = False
            if self.speech_bubble:
                self.speech_bubble.hide()

    def mouseMoveEvent(self, e):
        if self._drag_offset:
            self._dragging = True
            newpos = e.globalPos() - self._drag_offset
            clamped = self._clamp_to_screen(newpos)
            self.base_pos = clamped
        self.move(clamped)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.answered:
                self._show_bubble(self.current_message)
            if self._dragging:
                self._drag_offset = None
                self._dragging = False
                
            else:
                if e.pos().y() >= self.bottom_click_threshold:
                    if not self.answered:
                        self.answer_call()
                    else:
                        self.send.set('visible', False)
                self._drag_offset = None

    def answer_call(self):
        self.answered = True
        # self.vib_timer.stop()
        self.label.setPixmap(self.hangup_pixmap)
        # Center on current screen
        screen = QGuiApplication.screenAt(self.base_pos) or QGuiApplication.primaryScreen()
        geom = screen.availableGeometry()
        center = QPoint(
            geom.x() + (geom.width() - self.width()) // 2,
            geom.y() + (geom.height() - self.height()) // 2
        )
        self.base_pos = center

    def _show_bubble(self, text):
        self.current_message = text
        self.current_index = 0
        if not self.speech_bubble:
            self.speech_bubble = QLabel(self)
            self.speech_bubble.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip)
            self.speech_bubble.setAttribute(Qt.WA_TranslucentBackground, False)
            self.speech_bubble.setStyleSheet(
                "background:white;color:black;border:2px solid #333;"
                "border-radius:10px;padding:10px;font-size:25px;font-weight:bold;"
            )
        self.speech_bubble.setText("")
        self.speech_bubble.adjustSize()
        self._position_bubble()
        self.speech_bubble.show()
        self.typing_timer = QTimer(self)
        self.typing_timer.setInterval(20)
        self.typing_timer.stop()
        self.typing_timer.timeout.connect(self._type)
        self.typing_timer.start()

    def _type(self):
        if self.current_index < len(self.current_message):
            self.speech_bubble.setText(self.current_message[:self.current_index + 1])
            self.speech_bubble.adjustSize()
            self._position_bubble()
            self.current_index += 1
        else:
            self.typing_timer.stop()

    def _position_bubble(self):
        tl = self.rect().topLeft()
        bw, bh = self.speech_bubble.width(), self.speech_bubble.height()
        x = tl.x() + (self.width() - bw) // 2
        y = tl.y() - bh - 10
        self.speech_bubble.move(self.mapToGlobal(QPoint(x, y)))

    def _clamp_to_screen(self, pos):
        screen = QGuiApplication.screenAt(pos) or QGuiApplication.primaryScreen()
        geom = screen.availableGeometry()
        x = max(geom.x(), min(pos.x(), geom.x() + geom.width() - self.width()))
        y = max(geom.y(), min(pos.y(), geom.y() + geom.height() - self.height()))
        return QPoint(x, y)

    def remove_speech_bubble(self):
        if self.speech_bubble:
            self.speech_bubble.deleteLater()
            self.speech_bubble = None

    def random_action(self):
        pass


def start_desktop_pet(lang="../localization/en.json", image='call.png', hangup='hang_up.png'):
    """
    Launches the desktop pet in a separate process, returns the subprocess.Popen handle.
    """
    script = os.path.abspath(__file__)
    return subprocess.Popen([sys.executable, script, image, hangup, lang])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet(sys.argv[1] if len(sys.argv)>1 else 'call.png',
                     sys.argv[2] if len(sys.argv)>2 else 'hang_up.png',
                     sys.argv[3])
    pet.show()
    sys.exit(app.exec_())
