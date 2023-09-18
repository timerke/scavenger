import os
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QWidget


class PasswordWidget(QWidget):

    text_changed: pyqtSignal = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._dir_media: str = os.path.join(os.curdir, "media")
        self._password_showed: bool = True
        self._init_ui()
        self.show_or_hide()

    def _init_ui(self) -> None:
        self.line_edit_password: QLineEdit = QLineEdit()
        self.line_edit_password.textChanged.connect(self.send_text_changed_signal)
        self.button_show_or_hide: QPushButton = QPushButton()
        self.button_show_or_hide.clicked.connect(self.show_or_hide)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.line_edit_password)
        layout.addWidget(self.button_show_or_hide)
        self.setLayout(layout)

    @pyqtSlot()
    def send_text_changed_signal(self) -> None:
        self.text_changed.emit()

    def set_text(self, password: str) -> None:
        """
        :param password: new password.
        """

        self.line_edit_password.setText(password)

    @pyqtSlot()
    def show_or_hide(self) -> None:
        self._password_showed = not self._password_showed
        if self._password_showed:
            icon_path = os.path.join(self._dir_media, "crossed_out_eye.png")
            mode = QLineEdit.EchoMode.Normal
        else:
            icon_path = os.path.join(self._dir_media, "eye.png")
            mode = QLineEdit.EchoMode.Password
        self.button_show_or_hide.setIcon(QIcon(icon_path))
        self.line_edit_password.setEchoMode(mode)

    def text(self) -> str:
        """
        :return: text in widget.
        """

        return self.line_edit_password.text()
