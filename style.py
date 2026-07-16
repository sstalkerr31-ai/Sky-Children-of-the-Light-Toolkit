#!/usr/bin/env python3
"""
Общая тёмная тема (VS Code style) для всех вкладок Mod Kit.
"""

DARK_STYLE = """
    QMainWindow, QWidget {
        background-color: #1e1e1e;
        color: #d4d4d4;
        font-family: 'Consolas', 'Segoe UI', monospace;
    }
    QTabWidget::pane {
        border: 1px solid #3c3c3c;
        background-color: #1e1e1e;
    }
    QTabBar::tab {
        background-color: #2d2d2d;
        color: #969696;
        padding: 8px 18px;
        border: 1px solid #3c3c3c;
        border-bottom: none;
        font-size: 10pt;
    }
    QTabBar::tab:selected {
        background-color: #1e1e1e;
        color: #ffffff;
        border-top: 2px solid #0e639c;
    }
    QTabBar::tab:hover {
        background-color: #383838;
    }
    QPushButton {
        background-color: #0e639c;
        color: white;
        border: none;
        padding: 8px 15px;
        font-weight: bold;
        border-radius: 3px;
        font-size: 10pt;
    }
    QPushButton:hover { background-color: #1177bb; }
    QPushButton:disabled { background-color: #3c3c3c; color: #7a7a7a; }
    QPushButton:pressed { background-color: #0a4d7a; }
    QPlainTextEdit, QTextEdit {
        background-color: #1e1e1e;
        color: #d4d4d4;
        border: 1px solid #3c3c3c;
        font-size: 11pt;
    }
    QLabel { font-size: 10pt; color: #858585; }
    QLabel#previewLabel {
        background-color: #222222;
        color: #aaaaaa;
        border: 1px solid #3c3c3c;
    }
    QLineEdit {
        background-color: #3c3c3c;
        color: #d4d4d4;
        border: 1px solid #5a5a5a;
        padding: 5px;
        border-radius: 3px;
        font-size: 10pt;
    }
    QLineEdit:focus { border: 1px solid #0e639c; }
    QCheckBox { font-size: 9pt; color: #d4d4d4; }
    QTableWidget {
        background-color: #1e1e1e;
        color: #d4d4d4;
        gridline-color: #3c3c3c;
        border: 1px solid #3c3c3c;
        font-size: 10pt;
        selection-background-color: #0e639c;
        selection-color: #ffffff;
    }
    QHeaderView::section {
        background-color: #2d2d2d;
        color: #d4d4d4;
        padding: 6px;
        border: 1px solid #3c3c3c;
        font-weight: bold;
    }
    QStatusBar {
        background-color: #007acc;
        color: white;
        font-size: 9pt;
    }
    QScrollBar:vertical {
        background: #1e1e1e;
        width: 12px;
    }
    QScrollBar::handle:vertical {
        background: #4a4a4a;
        min-height: 20px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical:hover { background: #5a5a5a; }
    QSplitter::handle { background-color: #3c3c3c; }
"""
