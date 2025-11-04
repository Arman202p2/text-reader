import sys
from os import path

import cv2
import numpy as np

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox

import pytesseract
from PIL import Image
from pytesseract import image_to_string
from gtts import gTTS
from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env file

tesseract_path = os.getenv("TESSERACT_PATH", "C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
tessdata_dir_path = os.getenv("TESSERACT_LANG_DATA_PATH", "C:\\Program Files\\Tesseract-OCR\\tessdata")

#pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your path
pytesseract.pytesseract.tesseract_cmd = tesseract_path

#tessdata_dir_config = r'--tessdata-dir "<replace_with_your_tessdata_dir_path>"'
tessdata_dir_config = f'--tessdata-dir "{tessdata_dir_path}"' if tessdata_dir_path else ''



class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture(camera_port)

        self.timer = QtCore.QBasicTimer()

    def start_recording(self):
        self.timer.start(0, self)

    
    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)
    def framesave(self):
        save_path = os.path.join(os.path.expanduser("~"), "Documents", "a.png")

        read, data = self.camera.read()
        if read:
            result=cv2.imwrite(save_path, data)
            if not result:
                msg = QMessageBox()
                msg.setText(f"Failed to save image at {save_path}")
                msg.exec_()
                return
        try:
            img = Image.fromarray(cv2.cvtColor(data, cv2.COLOR_BGR2RGB))
            img.load()
        except Exception as e:
            msg = QMessageBox()
            msg.setText(f"Image conversion failed: {e}")
            msg.exec_()
            return

        try:
            text = pytesseract.image_to_string(img, lang='eng', config=tessdata_dir_config)
        except Exception as e:
            msg = QMessageBox()
            msg.setText(f"OCR failed: {e}")
            msg.exec_()
            return
        
        msg = QMessageBox()
        msg.setText(f"Text Found: {text}\nLength: {len(text)}")
        msg.exec_()
        print('Text_Found: ', text, len(text))
        if len(text) > 0:
            try:
                tts = gTTS(text=text, lang='en')  # for english language use (lang='en')
                tts.save(os.path.join(os.path.expanduser("~"), "Documents", "pcvoice.mp3"))
                os.startfile(os.path.join(os.path.expanduser("~"), "Documents", "pcvoice.mp3"))
            except Exception as e:
                msg = QMessageBox()
                msg.setText(f"TTS or playback failed: {e}")
                msg.exec_()
        else:
            # 2. Output visibility: Message box for "No text found"
            msg = QMessageBox()
            msg.setText("No text found in image.")
            msg.exec_()
            


class FaceDetectionWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (30, 30)


    def image_data_slot(self, image_data):


        
        self.image = self.get_qimage(image_data)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()
    
        
        
    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.face_detection_widget = FaceDetectionWidget()

        # TODO: set video port
        self.record_video = RecordVideo()

        image_data_slot = self.face_detection_widget.image_data_slot
        self.record_video.image_data.connect(image_data_slot)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.face_detection_widget)
        self.run_button = QtWidgets.QPushButton('Start')
        layout.addWidget(self.run_button)

        self.run_button.clicked.connect(self.record_video.start_recording)

        self.screenshot = QtWidgets.QPushButton('Snap Shot')
        layout.addWidget(self.screenshot)

        self.screenshot.clicked.connect(self.record_video.framesave)
        self.setLayout(layout)


    
def main():
    app = QtWidgets.QApplication(sys.argv)

    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget()
    main_window.setCentralWidget(main_widget)
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':

    main()

