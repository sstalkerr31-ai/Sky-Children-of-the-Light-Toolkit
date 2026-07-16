#!/usr/bin/env python3
"""
Mod Kit — единый инструмент моддера
=====================================
Объединяет:
  1. Localization Tool — редактор .strings файлов локализации
  2. Texture Tool       — декодер/энкодер KTX-текстур (BC7)
  3. Auto-Patcher       — менеджер замены файлов с автобэкапом

Запуск:  python3 main.py
Зависимости:  PyQt6, Pillow
  pip install PyQt6 Pillow --break-system-packages
"""
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtGui import QIcon

from style import DARK_STYLE
from tabs.localization_tab import LocalizationTab
from tabs.texture_tab import TextureTab
from tabs.patcher_tab import PatcherTab


class ModKitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛠 Mod Kit — набор инструментов моддера")
        self.setGeometry(100, 100, 1150, 800)
        self.setStyleSheet(DARK_STYLE)

        tabs = QTabWidget()
        tabs.setDocumentMode(True)

        tabs.addTab(LocalizationTab(), "📝 Localization")
        tabs.addTab(TextureTab(), "🖼 Textures (KTX)")
        tabs.addTab(PatcherTab(), "⚡ Auto-Patcher")

        self.setCentralWidget(tabs)
        self.statusBar().showMessage("Готов к работе")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ModKitWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
