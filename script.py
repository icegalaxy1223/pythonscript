import sys
import re
import elevenlabs
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QPushButton, 
                             QVBoxLayout, QWidget, QLineEdit, QLabel)
from PyQt5.QtCore import Qt

class TextReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        elevenlabs.set_api_key('YOUR_ELEVENLABS_API_KEY')

    def initUI(self):
        self.setWindowTitle('ElevenLabs Text Reader')
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Voice ID Input
        voice_layout = QVBoxLayout()
        voice_label = QLabel('Voice ID:')
        self.voice_id_input = QLineEdit()
        self.voice_id_input.setPlaceholderText('Enter ElevenLabs Voice ID')
        voice_layout.addWidget(voice_label)
        voice_layout.addWidget(self.voice_id_input)
        layout.addLayout(voice_layout)

        # Text Edit Area
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        # Read Quotes Button
        read_button = QPushButton('Read Text in Quotes')
        read_button.clicked.connect(self.read_quotes)
        layout.addWidget(read_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def read_quotes(self):
        text = self.text_edit.toPlainText()
        quotes = re.findall(r'"([^"]*)"', text)
        voice_id = self.voice_id_input.text() or "Adam"
        
        if not quotes:
            print("No quotes found!")
            return

        for quote in quotes:
            if quote.strip():
                try:
                    audio = elevenlabs.generate(
                        text=quote, 
                        voice=voice_id,
                        model="eleven_monolingual_v1"
                    )
                    elevenlabs.play(audio)
                except Exception as e:
                    print(f"Error reading quote '{quote}': {e}")

def main():
    app = QApplication(sys.argv)
    ex = TextReaderApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
