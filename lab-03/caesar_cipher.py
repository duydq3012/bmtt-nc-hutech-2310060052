import sys

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from ui.caesar import Ui_MainWindow


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._connect_buttons()

    def _get_widget(self, *names):
        for name in names:
            widget = getattr(self.ui, name, None)
            if widget is not None:
                return widget
        return None

    def _connect_buttons(self):
        btn_encrypt = self._get_widget("btn_encrypt", "pushButton")
        btn_decrypt = self._get_widget("btn_decrypt", "pushButton_2")

        if btn_encrypt is None or btn_decrypt is None:
            QMessageBox.critical(self, "UI Error", "Không tìm thấy button Encrypt/Decrypt trong UI.")
            return

        btn_encrypt.clicked.connect(self.call_api_encrypt)
        btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        txt_plain_text = self._get_widget("txt_plain_text", "textEdit")
        txt_key = self._get_widget("txt_key", "lineEdit")
        txt_cipher_text = self._get_widget("txt_cipher_text", "textEdit_2")

        if txt_plain_text is None or txt_key is None or txt_cipher_text is None:
            QMessageBox.critical(self, "UI Error", "Thiếu ô nhập/xuất dữ liệu trong UI.")
            return

        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": txt_plain_text.toPlainText(),
            "key": txt_key.text(),
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                txt_cipher_text.setText(data.get("encrypted_message", ""))

                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                QMessageBox.warning(self, "API Error", "Error while calling API")
        except requests.exceptions.RequestException as error:
            QMessageBox.critical(self, "Request Error", f"Error: {error}")

    def call_api_decrypt(self):
        txt_plain_text = self._get_widget("txt_plain_text", "textEdit")
        txt_key = self._get_widget("txt_key", "lineEdit")
        txt_cipher_text = self._get_widget("txt_cipher_text", "textEdit_2")

        if txt_plain_text is None or txt_key is None or txt_cipher_text is None:
            QMessageBox.critical(self, "UI Error", "Thiếu ô nhập/xuất dữ liệu trong UI.")
            return

        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": txt_cipher_text.toPlainText(),
            "key": txt_key.text(),
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                txt_plain_text.setText(data.get("decrypted_message", ""))

                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                QMessageBox.warning(self, "API Error", "Error while calling API")
        except requests.exceptions.RequestException as error:
            QMessageBox.critical(self, "Request Error", f"Error: {error}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
