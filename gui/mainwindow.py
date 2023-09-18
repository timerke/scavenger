import os
from typing import Any, Dict
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from gui.connectiondialog import ConnectionDialog
from gui.messagewindow import show_message
from gui.remotehostthread import ConnectionResult, RemoteHostThread


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self._dir_media: str = os.path.join(os.curdir, "media")
        self._init_ui()
        self._remote_host: RemoteHostThread = RemoteHostThread()
        self._remote_host.connection_result_signal.connect(self.handle_connection_result)
        self._remote_host.start()
        self._timer: QTimer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.handle_connect)
        self._timer.start(100)

    def _init_ui(self) -> None:
        loadUi(os.path.join(self._dir_media, "mainwindow.ui"), self)
        self.setWindowTitle("Scavenger")
        self.action_connect.triggered.connect(self.handle_connect)
        self.button_search.clicked.connect(self.search_junk)
        self.button_remove.clicked.connect(self.remove_junk)
        self.progress_bar.setVisible(False)

    def _set_bad_connection(self, connection_result: Dict[str, Any]) -> None:
        self.setWindowTitle("Scavenger")
        host = connection_result["host"]
        port = connection_result["port"]
        username = connection_result["username"]
        show_message(f"Не удалось подключиться к хосту {username}@{host}:{port}.", "Ошибка")
        connection_result.pop("result", None)
        self.handle_connect(connection_result)

    def _set_good_connection(self, connection_result: Dict[str, Any]) -> None:
        host = connection_result["host"]
        port = connection_result["port"]
        username = connection_result["username"]
        self.setWindowTitle(f"Scavenger {username}@{host}:{port}")

    def closeEvent(self, event: QCloseEvent) -> None:
        self._remote_host.stop()

    @pyqtSlot()
    def handle_connect(self, connection_data: Dict[str, Any] = dict()) -> None:
        dialog = ConnectionDialog(**connection_data)
        dialog.connection_signal.connect(self._remote_host.connect_host)
        dialog.exec()

    @pyqtSlot(dict)
    def handle_connection_result(self, connection_result: Dict[str, Any]) -> None:
        if connection_result["result"] == ConnectionResult.CONNECTION_ERROR:
            self._set_bad_connection(connection_result)
        else:
            self._set_good_connection(connection_result)

    @pyqtSlot()
    def remove_junk(self) -> None:
        self._remote_host.remove_junk()

    @pyqtSlot()
    def search_junk(self) -> None:
        self._remote_host.search_junk()
