import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox


def show_message(message: str, header: str, icon: QIcon = QMessageBox.Warning, no_button: bool = False,
                 cancel_button: bool = False, yes_button: bool = False) -> bool:
    """
    Function show message box.
    :param message: message;
    :param header: header;
    :param icon: message box icon;
    :param no_button: if True, then No button will be shown;
    :param cancel_button: if True, then Cancel button will be shown;
    :param yes_button: if True, then Yes button will be shown.
    :return: True if user agreed with message.
    """

    message_box = QMessageBox()
    message_box.setWindowTitle(header)
    dir_media = os.path.join(os.curdir, "media")
    message_box.setWindowIcon(QIcon(os.path.join(dir_media, "truck.png")))
    message_box.setIcon(icon)
    message_box.setTextFormat(Qt.RichText)
    message_box.setTextInteractionFlags(Qt.TextBrowserInteraction)
    message_box.setText(message)
    if yes_button:
        message_box.addButton("Да", QMessageBox.AcceptRole)
    else:
        message_box.addButton("OK", QMessageBox.AcceptRole)
    if no_button:
        message_box.addButton("Нет", QMessageBox.NoRole)
    if cancel_button:
        message_box.addButton("Отмена", QMessageBox.RejectRole)
    return message_box.exec() == QMessageBox.AcceptRole
