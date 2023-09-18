import ipaddress
import os
from typing import Any, Dict
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QLineEdit, QSpinBox
from PyQt5.uic import loadUi
from gui.passwordwidget import PasswordWidget


class ConnectionDialog(QDialog):

    DEFAULT_PORT: int = 39000
    DEFAULT_USER_NAME: str = "root"
    connection_signal: pyqtSignal = pyqtSignal(dict)

    def __init__(self, host: str = None, port: int = None, username: str = None, password: str = None) -> None:
        """
        :param host:
        :param port:
        :param username:
        :param password:
        """

        super().__init__()
        self._dir_media: str = os.path.join(os.curdir, "media")
        self._init_ui()
        self._set_connection_data({"host": host,
                                   "port": port,
                                   "username": username,
                                   "password": password})

    def _check_host(self) -> bool:
        """
        :return: True if correct IP address is entered.
        """

        result = False
        if self.line_edit_host.hasAcceptableInput():
            try:
                ipaddress.ip_address(self.line_edit_host.text())
            except Exception:
                pass
            else:
                result = True
        return result

    def _get_connection_data(self) -> Dict[str, Any]:
        """
        :return: dictionary with data for connecting to remote computer.
        """

        return {"host": self.line_edit_host.text(),
                "port": self.spin_box_port.value(),
                "username": self.line_edit_username.text(),
                "password": self.password_widget.text()}

    def _init_ui(self) -> None:
        loadUi(os.path.join(self._dir_media, "connectiondialog.ui"), self)
        self.password_widget: PasswordWidget = PasswordWidget()
        self.password_widget.text_changed.connect(lambda: self.check_input_data())
        self.form_layout.addRow("Пароль", self.password_widget)
        self.line_edit_host.textChanged.connect(lambda: self.check_input_data())
        self.line_edit_host.setValidator(QRegExpValidator(QRegExp(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")))
        self.spin_box_port.textChanged.connect(lambda: self.check_input_data())
        self.spin_box_port.setValue(ConnectionDialog.DEFAULT_PORT)
        self.line_edit_username.textChanged.connect(lambda: self.check_input_data())
        self.line_edit_username.setText(ConnectionDialog.DEFAULT_USER_NAME)
        self.button_connect.clicked.connect(self.connect)
        self.button_connect.setFocus()
        self.button_close.clicked.connect(self.close)

    def _set_connection_data(self, connection_data: Dict[str, Any]) -> None:
        widgets = {"host": self.line_edit_host,
                   "port": self.spin_box_port,
                   "username": self.line_edit_username,
                   "password": self.password_widget}
        for key, widget in widgets.items():
            new_value = connection_data.get(key, None)
            if new_value:
                if isinstance(widget, QSpinBox):
                    widget.setValue(new_value)
                elif isinstance(widget, QLineEdit):
                    widget.setText(new_value)
                elif isinstance(widget, PasswordWidget):
                    widget.set_text(new_value)

    @pyqtSlot()
    def check_input_data(self) -> None:
        empty = False
        for widget in (self.spin_box_port, self.line_edit_username, self.password_widget):
            if not widget.text():
                empty = True
                break
        self.button_connect.setEnabled(not empty and self._check_host())

    @pyqtSlot()
    def connect(self) -> None:
        self.close()
        self.connection_signal.emit(self._get_connection_data())
