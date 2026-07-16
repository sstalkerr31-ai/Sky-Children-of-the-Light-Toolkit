#!/usr/bin/env python3
"""
Виджеты продвинутого текстового редактора (в стиле VS Code):
- CodeEditor / LineNumberArea — нумерация строк
- StringsHighlighter — подсветка синтаксиса игровых тегов локализации
- FindBar — панель поиска (Ctrl+F)

Вынесено в отдельный модуль, чтобы переиспользовать в разных вкладках Mod Kit.
"""
import re
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import (QColor, QPainter, QTextFormat, QFont, QSyntaxHighlighter,
                          QTextCharFormat, QTextDocument, QKeySequence, QShortcut)
from PyQt6.QtWidgets import (QPlainTextEdit, QWidget, QHBoxLayout, QPushButton,
                              QLabel, QLineEdit, QCheckBox)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)

    def lineNumberAreaWidth(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num /= 10
            digits += 1
        space = 15 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#2d2d2d"))
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(QColor("#858585"))
                painter.drawText(0, top, self.lineNumberArea.width() - 5, self.fontMetrics().height(),
                                  Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            blockNumber += 1


class StringsHighlighter(QSyntaxHighlighter):
    """Подсветка тегов игровой локализации: ключи, значения, <теги>, {{переменные}}, \\n."""

    def __init__(self, parent):
        super().__init__(parent)
        self.rules = []

        key_format = QTextCharFormat()
        key_format.setForeground(QColor("#9cdcfe"))
        self.rules.append((r'^\s*"[^"]*"', key_format))

        val_format = QTextCharFormat()
        val_format.setForeground(QColor("#ce9178"))
        self.rules.append((r'=\s*"[^"]*"', val_format))

        tag_format = QTextCharFormat()
        tag_format.setForeground(QColor("#569cd6"))
        self.rules.append((r'<[^>]+>', tag_format))

        var_format = QTextCharFormat()
        var_format.setForeground(QColor("#4ec9b0"))
        self.rules.append((r'\{\{[^\}]+\}\}', var_format))

        slash_format = QTextCharFormat()
        slash_format.setForeground(QColor("#d7ba7d"))
        self.rules.append((r'\\n', slash_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for match in re.finditer(pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), fmt)


class FindBar(QWidget):
    """Панель поиска, вызывается по Ctrl+F, как в VS Code."""

    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        self.hide()

        layout = QHBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Найти...")
        self.input.textChanged.connect(self.on_text_changed)
        self.input.returnPressed.connect(self.find_next)

        self.case_checkbox = QCheckBox("Учитывать регистр")

        self.count_label = QLabel("")
        self.count_label.setFixedWidth(90)

        self.btn_prev = QPushButton("▲")
        self.btn_prev.setFixedWidth(32)
        self.btn_prev.clicked.connect(self.find_prev)

        self.btn_next = QPushButton("▼")
        self.btn_next.setFixedWidth(32)
        self.btn_next.clicked.connect(self.find_next)

        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedWidth(32)
        self.btn_close.clicked.connect(self.hide_bar)

        layout.addWidget(self.input)
        layout.addWidget(self.count_label)
        layout.addWidget(self.btn_prev)
        layout.addWidget(self.btn_next)
        layout.addWidget(self.case_checkbox)
        layout.addWidget(self.btn_close)
        layout.addStretch()
        self.setLayout(layout)

        close_shortcut = QShortcut(QKeySequence("Escape"), self.input)
        close_shortcut.activated.connect(self.hide_bar)

        prev_shortcut = QShortcut(QKeySequence("Shift+Return"), self.input)
        prev_shortcut.activated.connect(self.find_prev)

    def show_bar(self):
        self.show()
        self.input.setFocus()
        self.input.selectAll()
        if self.input.text():
            self.on_text_changed(self.input.text())

    def hide_bar(self):
        self.hide()
        self.editor.setFocus()

    def _flags(self, backward=False):
        flags = QTextDocument.FindFlag(0)
        if self.case_checkbox.isChecked():
            flags |= QTextDocument.FindFlag.FindCaseSensitively
        if backward:
            flags |= QTextDocument.FindFlag.FindBackward
        return flags

    def on_text_changed(self, text):
        self._update_count(text)
        if not text:
            return
        cursor = self.editor.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        self.editor.setTextCursor(cursor)
        self._do_find(text, backward=False)

    def _update_count(self, text):
        if not text:
            self.count_label.setText("")
            return
        plain = self.editor.toPlainText()
        haystack = plain if self.case_checkbox.isChecked() else plain.lower()
        needle = text if self.case_checkbox.isChecked() else text.lower()
        count = haystack.count(needle) if needle else 0
        self.count_label.setText(f"{count} совпад.")

    def _do_find(self, text, backward):
        found = self.editor.find(text, self._flags(backward))
        if not found:
            cursor = self.editor.textCursor()
            cursor.movePosition(
                cursor.MoveOperation.End if backward else cursor.MoveOperation.Start
            )
            self.editor.setTextCursor(cursor)
            self.editor.find(text, self._flags(backward))

    def find_next(self):
        text = self.input.text()
        if text:
            self._do_find(text, backward=False)

    def find_prev(self):
        text = self.input.text()
        if text:
            self._do_find(text, backward=True)
