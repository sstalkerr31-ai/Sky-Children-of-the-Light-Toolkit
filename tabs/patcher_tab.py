#!/usr/bin/env python3
"""
Вкладка: Auto-Patcher
Менеджер связок «Файл -> Путь замены» с автоматическим бэкапом.
"""
import json
import os
import shutil
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                              QLabel, QFileDialog, QMessageBox, QTableWidget,
                              QTableWidgetItem, QTextEdit, QAbstractItemView,
                              QFrame)

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


class PatcherTab(QWidget):
    def __init__(self):
        super().__init__()
        self.pairs = []
        self._build_ui()
        self.load_config()

    # ------------------------------------------------------------------ #
    #                              UI                                    #
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        layout = QVBoxLayout()

        # --- Верхняя панель ---
        top_bar = QHBoxLayout()
        btn_add = QPushButton("➕ Добавить пару")
        btn_add.clicked.connect(self.add_pair)
        btn_remove = QPushButton("🗑 Удалить")
        btn_remove.clicked.connect(self.remove_pair)
        btn_save_profile = QPushButton("💾 Сохранить профиль")
        btn_save_profile.clicked.connect(lambda: self.save_config(silent=False))
        btn_load_profile = QPushButton("📂 Загрузить профиль")
        btn_load_profile.clicked.connect(self.load_config)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)

        self.patch_button = QPushButton("⚡ ПАТЧИТЬ")
        self.patch_button.clicked.connect(self.run_patch)

        top_bar.addWidget(btn_add)
        top_bar.addWidget(btn_remove)
        top_bar.addWidget(btn_save_profile)
        top_bar.addWidget(btn_load_profile)
        top_bar.addWidget(sep)
        top_bar.addWidget(self.patch_button)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        # --- Таблица связок ---
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Мой новый файл (источник)", "Файл для замены (назначение)"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 440)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table, stretch=2)

        # --- Лог ---
        log_label = QLabel("Лог")
        layout.addWidget(log_label)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #111; color: #0f0; font-family: Consolas, monospace;")
        self.log_text.setMaximumHeight(180)
        layout.addWidget(self.log_text, stretch=1)

        # Статус
        self.status_label = QLabel("Готов")
        self.status_label.setStyleSheet("color: #cccccc; padding: 4px; background-color: #2d2d2d;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    # ------------------------------------------------------------------ #
    #                        Логирование                                 #
    # ------------------------------------------------------------------ #
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {"INFO": "[i]", "OK": "[✓]", "ERROR": "[✗]", "WARN": "[!]"}.get(level, "[i]")
        self.log_text.append(f"{timestamp} {prefix} {message}")
        self.status_label.setText(message)

    # ------------------------------------------------------------------ #
    #                     Управление парами (CRUD)                       #
    # ------------------------------------------------------------------ #
    def add_pair(self):
        source_path, _ = QFileDialog.getOpenFileName(
            self, "Шаг 1/2 — Выберите ваш новый файл (источник)"
        )
        if not source_path:
            return

        initial_dir = os.path.dirname(source_path)
        target_path, _ = QFileDialog.getOpenFileName(
            self, "Шаг 2/2 — Выберите файл, который нужно ЗАМЕНИТЬ (назначение)", initial_dir
        )
        if not target_path:
            return

        self.pairs.append({"source": source_path, "target": target_path})
        self._append_row(source_path, target_path)
        self.log(f"Добавлена пара: {os.path.basename(source_path)} -> {target_path}", "OK")
        self.save_config(silent=True)

    def _append_row(self, source, target):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(source))
        self.table.setItem(row, 1, QTableWidgetItem(target))

    def remove_pair(self):
        selected_rows = sorted({idx.row() for idx in self.table.selectedIndexes()}, reverse=True)
        if not selected_rows:
            QMessageBox.information(self, "Удаление", "Сначала выберите строку(и) в таблице.")
            return

        for row in selected_rows:
            source = self.table.item(row, 0).text()
            target = self.table.item(row, 1).text()
            self.pairs = [
                p for p in self.pairs
                if not (p["source"] == source and p["target"] == target)
            ]
            self.table.removeRow(row)

        self.log(f"Удалено связок: {len(selected_rows)}", "WARN")
        self.save_config(silent=True)

    # ------------------------------------------------------------------ #
    #                     Сохранение / загрузка config.json               #
    # ------------------------------------------------------------------ #
    def save_config(self, silent=False):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump({"pairs": self.pairs}, f, ensure_ascii=False, indent=2)
            if not silent:
                self.log(f"Профиль сохранён в {CONFIG_FILE}", "OK")
        except Exception as e:
            self.log(f"Не удалось сохранить профиль: {e}", "ERROR")

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            self.log("Файл config.json не найден — начинаем с пустого списка.", "WARN")
            return

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.pairs = data.get("pairs", [])

            self.table.setRowCount(0)
            for p in self.pairs:
                self._append_row(p.get("source", ""), p.get("target", ""))

            self.log(f"Загружено связок: {len(self.pairs)}", "OK")
        except Exception as e:
            self.log(f"Ошибка чтения config.json: {e}", "ERROR")

    # ------------------------------------------------------------------ #
    #                      Основная логика патчинга                      #
    # ------------------------------------------------------------------ #
    def run_patch(self):
        if not self.pairs:
            QMessageBox.information(self, "Патчинг", "Список связок пуст. Добавьте хотя бы одну пару.")
            return

        confirm = QMessageBox.question(
            self, "Подтверждение",
            f"Будет обработано {len(self.pairs)} файл(ов).\n"
            "Оригиналы будут сохранены как .bak перед заменой.\n\n"
            "Продолжить?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        self.patch_button.setEnabled(False)
        self.log("=" * 50)
        self.log(f"Запуск патчинга ({len(self.pairs)} связок)...")

        success_count = 0
        error_count = 0

        for pair in self.pairs:
            source = pair.get("source", "")
            target = pair.get("target", "")
            ok = self._process_pair(source, target)
            if ok:
                success_count += 1
            else:
                error_count += 1

        self.log("=" * 50)
        self.log(f"Патчинг завершён. Успешно: {success_count}, Ошибок: {error_count}",
                  "OK" if error_count == 0 else "WARN")

        self.patch_button.setEnabled(True)

        if error_count == 0:
            QMessageBox.information(self, "Готово", f"Патчинг успешно завершён!\nОбработано файлов: {success_count}")
        else:
            QMessageBox.warning(
                self, "Готово с ошибками",
                f"Успешно: {success_count}\nОшибок: {error_count}\nПодробности смотрите в логе."
            )

    def _process_pair(self, source, target) -> bool:
        """Обрабатывает одну связку: проверка, бэкап, копирование. Возвращает True при успехе."""
        short_name = os.path.basename(target) if target else "???"

        if not source or not os.path.isfile(source):
            self.log(f"[{short_name}] Источник не найден: {source}", "ERROR")
            return False

        target_dir = os.path.dirname(target)
        if target_dir and not os.path.isdir(target_dir):
            self.log(f"[{short_name}] Папка назначения недоступна: {target_dir}", "ERROR")
            return False

        try:
            if os.path.isfile(target):
                backup_path = target + ".bak"
                if not os.path.isfile(backup_path):
                    shutil.copy2(target, backup_path)
                    self.log(f"[{short_name}] Бэкап создан: {os.path.basename(backup_path)}")
                else:
                    self.log(f"[{short_name}] Бэкап уже существует, пропускаем создание.", "WARN")
            else:
                self.log(f"[{short_name}] Оригинал отсутствует, бэкап не требуется.", "WARN")

            shutil.copy2(source, target)
            self.log(f"[{short_name}] Успешно заменён.", "OK")
            return True

        except PermissionError:
            self.log(f"[{short_name}] Ошибка доступа (файл занят или нет прав).", "ERROR")
            return False
        except Exception as e:
            self.log(f"[{short_name}] Ошибка: {e}", "ERROR")
            return False
