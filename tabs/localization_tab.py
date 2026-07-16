#!/usr/bin/env python3
"""
Вкладка: Sky Localization Tool
Редактор Localizable.strings с подсветкой синтаксиса, номерами строк,
поиском (Ctrl+F) и авто-бэкапом при сохранении.
"""
import os
import shutil

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                              QLabel, QFileDialog, QMessageBox)

from editor_widgets import CodeEditor, StringsHighlighter, FindBar

# ⚙️ Путь по умолчанию для диалога открытия файла (при желании поменяйте)
DEFAULT_STRINGS_PATH = r"D:/Sky_arhiv_versii/Sky Children of the Light/data/assets/initial/Data"


class LocalizationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.current_file_path = ""

        layout = QVBoxLayout()

        top_bar = QHBoxLayout()
        self.btn_open = QPushButton("📂 Открыть Localizable.strings")
        self.btn_open.clicked.connect(self.open_file)
        self.btn_save = QPushButton("💾 Сохранить и применить в игре")
        self.btn_save.clicked.connect(self.save_file)

        top_bar.addWidget(self.btn_open)
        top_bar.addWidget(self.btn_save)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        self.lbl_status = QLabel("Файл не выбран. Нажмите кнопку 'Открыть' для начала редактирования.")
        layout.addWidget(self.lbl_status)

        self.editor = CodeEditor()
        self.highlighter = StringsHighlighter(self.editor.document())
        layout.addWidget(self.editor)

        self.find_bar = FindBar(self.editor)
        layout.addWidget(self.find_bar)

        find_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        find_shortcut.activated.connect(self.find_bar.show_bar)

        self.setLayout(layout)

    def open_file(self):
        start_dir = DEFAULT_STRINGS_PATH if os.path.isdir(DEFAULT_STRINGS_PATH) else ""
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл локализации", start_dir, "Файлы строк (*.strings *.txt)"
        )
        if path:
            self.current_file_path = path
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.editor.setPlainText(f.read())
                self.lbl_status.setText(f"🟢 Активный файл: {path}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка чтения", f"Не удалось прочитать файл:\n{str(e)}")

    def save_file(self):
        if not self.current_file_path:
            QMessageBox.warning(self, "Внимание", "Сначала откройте файл через кнопку 'Открыть'!")
            return

        try:
            backup_path = self.current_file_path + ".bak"
            if not os.path.exists(backup_path):
                shutil.copy2(self.current_file_path, backup_path)

            with open(self.current_file_path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())

            QMessageBox.information(
                self, "Успех!",
                "Файл локализации успешно обновлен прямо в папке игры!\n\nОригинал сохранен рядом с расширением .strings.bak"
            )
        except Exception as e:
            QMessageBox.critical(self, "Ошибка сохранения", f"Не удалось перезаписать файл:\n{str(e)}")
