from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMainWindow


class MessageReceivingThread(QThread):

    messageReceived = pyqtSignal(str)

    def __init__(self):
        super(MessageReceivingThread, self).__init__()
        self.is_running = True

    def __del__(self):
        self.wait()

    def run(self):
        import struct

        while self.is_running:
            message_length_bytes = sys.stdin.buffer.read(4)
            if len(message_length_bytes) == 0:
                continue
            message_length = struct.unpack("i", message_length_bytes)[0]
            message = sys.stdin.buffer.read(message_length).decode("utf-8")
            self.messageReceived.emit(message)


class MainWindow(QMainWindow):

    def __init__(self, application):

        from PyQt5 import uic
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QIcon

        super(MainWindow, self).__init__()

        ui_file_path = "resources/interface.ui"
        icon_file_path = "resources/icon.png"

        uic.loadUi(ui_file_path, self)
        self.setWindowIcon(QIcon(icon_file_path))

        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint)

        self.line_edit.returnPressed.connect(self.on_button_clicked)
        self.log_widget.setReadOnly(True)

        application.aboutToQuit.connect(self.on_quit)

        self.message_receiving_thread = MessageReceivingThread()
        self.message_receiving_thread.messageReceived.connect(self.on_message_received)
        self.message_receiving_thread.start()
    
    def excepthook(self, exctype, value, traceback):
        self.log(f"Exception: {exctype}, \"{value}\"\n{traceback.tb_frame}\n")

    @pyqtSlot(str)
    def on_message_received(self, message):
        self.log(f"Received message: {message}")

    @pyqtSlot()
    def on_button_clicked(self):

        import json

        text = self.line_edit.text()
        self.line_edit.clear()

        message_object = {"text": text}

        message = json.dumps(message_object, ensure_ascii=False)
        message_bytes = message.encode()

        try:
            self.send_message_to_chrome(message_bytes)
        except IOError:
            raise RuntimeError("Failed to send message")
        else:
            self.log(f"Sent message: {message}")

    @pyqtSlot()
    def on_quit(self):
        import os
        import signal
        self.message_receiving_thread.is_running = False
        os.kill(os.getpid(), signal.SIGINT)

    def send_message_to_chrome(self, message):
        import struct
        header = struct.pack("I", len(message))
        sys.stdout.buffer.write(header)
        sys.stdout.buffer.write(message)
        sys.stdout.buffer.flush()

    def log(self, message):
        self.log_widget.appendPlainText(f"{message}")


def main():
    import sys
    from PyQt5.QtWidgets import QApplication

    if sys.platform == "win32":
        import os
        import msvcrt
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

    application = QApplication(sys.argv)
    window = MainWindow(application)
    sys.excepthook = window.excepthook

    window.show()

    return application.exec()


if __name__ == "__main__":
    import sys
    sys.exit(main())
