import time
from enum import auto, Enum
from queue import Queue
from typing import Any, Dict
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
from gui.remotehost import RemoteHost


class ConnectionResult(Enum):

    CONNECTED = auto()
    CONNECTION_ERROR = auto()


class RemoteHostThread(QThread):

    connection_result_signal: pyqtSignal = pyqtSignal(dict)

    def __init__(self) -> None:
        super().__init__()
        self._is_running: bool = False
        self._remote_host: RemoteHost = None
        self._task: Queue = Queue()
        self.setTerminationEnabled(True)

    def _connect(self, connection_data: Dict[str, Any]) -> None:
        try:
            self._remote_host = RemoteHost(**connection_data)
            result = True
        except Exception:
            self._remote_host = None
            result = False
        connection_data["result"] = ConnectionResult.CONNECTED if result else ConnectionResult.CONNECTION_ERROR
        self.connection_result_signal.emit(connection_data)

    def _search_junk(self) -> None:
        pass

    @pyqtSlot(dict)
    def connect_host(self, connection_data: Dict[str, Any]) -> None:
        self._task.put(lambda: self._connect(connection_data))

    def remove_junk(self) -> None:
        pass

    def run(self) -> None:
        while self._is_running:
            if not self._task.empty():
                task = self._task.get()
                try:
                    task()
                except Exception:
                    pass
            time.sleep(0.2)

    def search_junk(self) -> None:
        self._task.put(lambda: self._search_junk())

    def start(self) -> None:
        self._is_running = True
        super().start()

    def stop(self) -> None:
        self._is_running = False
        self.quit()
