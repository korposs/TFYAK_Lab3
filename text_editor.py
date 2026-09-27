"""
Текстовый редактор - лабораторная работа №1.
Тема: Объявление структуры на языке Java.
Автор: Башинов Арья Игоревич, группа АП-326.
"""

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence, QPalette, QColor, QBrush
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QPlainTextEdit, QSplitter, QStyleFactory, QToolBar, QTableWidget, QTableWidgetItem

from compiler.scanner import Scanner

APP_TITLE = "Текстовый редактор"
ICONS_DIR = Path(__file__).parent / "resources" / "icons"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_file = None

        self.setWindowTitle(APP_TITLE)
        self.resize(1000, 700)

        self._create_editor_area()
        self._create_actions()
        self._create_menus()
        self._create_toolbar()
        self._connect_actions()

    def _create_editor_area(self):
        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("Введите исходный текст...")

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Код", "Тип", "Лексема", "Местоположение"])
        self.result_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.result_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.itemClicked.connect(self._on_table_clicked)

        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.result_table)
        splitter.setSizes([400, 300])
        splitter.setChildrenCollapsible(False)

        self.setCentralWidget(splitter)

    def _create_actions(self):
        self.new_action = QAction("Создать", self)
        self.open_action = QAction("Открыть", self)
        self.save_action = QAction("Сохранить", self)
        self.save_as_action = QAction("Сохранить как", self)
        self.exit_action = QAction("Выход", self)

        self.undo_action = QAction("Отменить", self)
        self.redo_action = QAction("Повторить", self)
        self.cut_action = QAction("Вырезать", self)
        self.copy_action = QAction("Копировать", self)
        self.paste_action = QAction("Вставить", self)
        self.delete_action = QAction("Удалить", self)
        self.select_all_action = QAction("Выделить всё", self)

        self.task_action = QAction("Постановка задачи", self)
        self.grammar_action = QAction("Грамматика", self)
        self.classification_action = QAction("Классификация грамматики", self)
        self.method_action = QAction("Метод анализа", self)
        self.example_action = QAction("Тестовый пример", self)
        self.literature_action = QAction("Список литературы", self)
        self.source_action = QAction("Исходный код программы", self)

        self.run_action = QAction("Пуск", self)

        self.run_menu_action = QAction("Пуск", self)

        self.help_action = QAction("Вызов справки", self)
        self.about_action = QAction("О программе", self)

        self._setup_shortcuts()
        self._setup_icons()

    def _setup_shortcuts(self):
        self.new_action.setShortcut(QKeySequence.StandardKey.New)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        self.exit_action.setShortcut(QKeySequence("Alt+F4"))

        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        self.copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        self.paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        self.delete_action.setShortcut(QKeySequence("Delete"))
        self.select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)

        self.run_menu_action.setShortcut(QKeySequence("F5"))

        self.help_action.setShortcut(QKeySequence.StandardKey.HelpContents)

    def _setup_icons(self):
        icon_map = {
            self.new_action: "new.png",
            self.open_action: "open.png",
            self.save_action: "save.png",
            self.undo_action: "undo.png",
            self.redo_action: "redo.png",
            self.cut_action: "cut.png",
            self.copy_action: "copy.png",
            self.paste_action: "paste.png",
            self.delete_action: "delete.png",
            self.run_action: "run.png",
            self.help_action: "help.png",
            self.about_action: "about.png",
        }

        for action, filename in icon_map.items():
            path = ICONS_DIR / filename
            if path.exists():
                action.setIcon(QIcon(str(path)))
            else:
                print(f"[WARN] Иконка не найдена: {path}", file=sys.stderr)
            action.setIconVisibleInMenu(False)

    def _create_menus(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Файл")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        edit_menu = menu_bar.addMenu("Правка")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addAction(self.delete_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.select_all_action)

        text_menu = menu_bar.addMenu("Текст")
        text_menu.addAction(self.task_action)
        text_menu.addAction(self.grammar_action)
        text_menu.addAction(self.classification_action)
        text_menu.addAction(self.method_action)
        text_menu.addAction(self.example_action)
        text_menu.addAction(self.literature_action)
        text_menu.addAction(self.source_action)

        menu_bar.addAction(self.run_menu_action)

        help_menu = menu_bar.addMenu("Справка")
        help_menu.addAction(self.help_action)
        help_menu.addAction(self.about_action)

    def _create_toolbar(self):
        toolbar = QToolBar("Панель инструментов", self)
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)

        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.undo_action)
        toolbar.addAction(self.redo_action)
        toolbar.addSeparator()
        toolbar.addAction(self.cut_action)
        toolbar.addAction(self.copy_action)
        toolbar.addAction(self.paste_action)
        toolbar.addAction(self.delete_action)
        toolbar.addSeparator()
        toolbar.addAction(self.run_action)
        toolbar.addSeparator()
        toolbar.addAction(self.help_action)
        toolbar.addAction(self.about_action)

        self.addToolBar(toolbar)

    def _connect_actions(self):
        self.new_action.triggered.connect(self._on_new)
        self.open_action.triggered.connect(self._on_open)
        self.save_action.triggered.connect(self._on_save)
        self.save_as_action.triggered.connect(self._on_save_as)
        self.exit_action.triggered.connect(self.close)

        self.undo_action.triggered.connect(self.editor.undo)
        self.redo_action.triggered.connect(self.editor.redo)
        self.cut_action.triggered.connect(self.editor.cut)
        self.copy_action.triggered.connect(self.editor.copy)
        self.paste_action.triggered.connect(self.editor.paste)
        self.delete_action.triggered.connect(self._on_delete_selection)
        self.select_all_action.triggered.connect(self.editor.selectAll)

        self.task_action.triggered.connect(lambda: self._on_show_text_info("Постановка задачи", "Здесь будет постановка задачи."))
        self.grammar_action.triggered.connect(lambda: self._on_show_text_info("Грамматика", "Здесь будет описание грамматики."))
        self.classification_action.triggered.connect(lambda: self._on_show_text_info("Классификация грамматики", "Здесь будет классификация грамматики."))
        self.method_action.triggered.connect(lambda: self._on_show_text_info("Метод анализа", "Здесь будет описание метода анализа."))
        self.example_action.triggered.connect(lambda: self._on_show_text_info("Тестовый пример", "Здесь будет тестовый пример."))
        self.literature_action.triggered.connect(lambda: self._on_show_text_info("Список литературы", "Здесь будет список литературы."))
        self.source_action.triggered.connect(lambda: self._on_show_text_info("Исходный код программы", "Здесь будет информация об исходном коде."))

        self.run_action.triggered.connect(self._on_run)
        self.run_menu_action.triggered.connect(self._on_run)

        self.help_action.triggered.connect(self._on_show_help)
        self.about_action.triggered.connect(self._on_show_about)

    def _on_delete_selection(self):
        cursor = self.editor.textCursor()
        cursor.removeSelectedText()
        self.editor.setTextCursor(cursor)

    def _on_new(self):
        if not self._maybe_save():
            return
        self.editor.clear()
        self.current_file = None
        self._update_title()

    def _on_open(self):
        if not self._maybe_save():
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Текстовые файлы (*.txt);;Все файлы (*.*)")
        if not file_path:
            return

        try:
            text = Path(file_path).read_text(encoding="utf-8")
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{exc}")
            return

        self.editor.setPlainText(text)
        self.editor.document().setModified(False)
        self.current_file = file_path
        self._update_title()

    def _on_save(self):
        if self.current_file is None:
            return self._on_save_as()

        try:
            Path(self.current_file).write_text(self.editor.toPlainText(), encoding="utf-8")
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{exc}")
            return False

        self.editor.document().setModified(False)
        self._update_title()
        return True

    def _on_save_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", self.current_file or "", "Текстовые файлы (*.txt);;Все файлы (*.*)")
        if not file_path:
            return False

        self.current_file = file_path
        return self._on_save()

    def _maybe_save(self):
        if not self.editor.document().isModified():
            return True

        result = QMessageBox.question(self, "Сохранение изменений", "Сохранить изменения в текущем документе?", QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

        if result == QMessageBox.StandardButton.Save:
            return self._on_save()
        if result == QMessageBox.StandardButton.Cancel:
            return False
        return True

    def _update_title(self):
        if self.current_file:
            self.setWindowTitle(f"{APP_TITLE} - {self.current_file}")
        else:
            self.setWindowTitle(APP_TITLE)

    def _on_run(self):
        text = self.editor.toPlainText()
        scanner = Scanner()
        tokens, errors = scanner.scan(text)

        self.result_table.setRowCount(0)

        for token in tokens:
            if token.type == "UNKNOWN":
                continue
            row = self.result_table.rowCount()
            self.result_table.insertRow(row)
            self.result_table.setItem(row, 0, QTableWidgetItem(str(token.code)))
            self.result_table.setItem(row, 1, QTableWidgetItem(token.type))
            self.result_table.setItem(row, 2, QTableWidgetItem(self._display_lexeme(token)))
            self.result_table.setItem(row, 3, QTableWidgetItem(f"строка {token.line}, [{token.start}:{token.end}]"))

        red_bg = QColor(255, 220, 220)
        red_fg = QColor(180, 0, 0)

        for error in errors:
            row = self.result_table.rowCount()
            self.result_table.insertRow(row)

            code_item = QTableWidgetItem("99")
            type_item = QTableWidgetItem("ОШИБКА")
            lexeme = error.character
            if lexeme.isspace():
                lexeme = "(пробел)" if lexeme == " " else "(пробелы)"
            lexeme_item = QTableWidgetItem(lexeme)
            location_item = QTableWidgetItem(f"строка {error.line}, [{error.col}:{error.col}]")

            for item in (code_item, type_item, lexeme_item, location_item):
                item.setBackground(QBrush(red_bg))
                item.setForeground(QBrush(red_fg))

            self.result_table.setItem(row, 0, code_item)
            self.result_table.setItem(row, 1, type_item)
            self.result_table.setItem(row, 2, lexeme_item)
            self.result_table.setItem(row, 3, location_item)

        total_lexemes = len([t for t in tokens if t.type != "UNKNOWN"])
        total_errors = len(errors)

        row = self.result_table.rowCount()
        self.result_table.insertRow(row)
        summary = QTableWidgetItem(f"Итого: лексем - {total_lexemes}, ошибок - {total_errors}")
        font = summary.font()
        font.setBold(True)
        summary.setFont(font)
        summary.setBackground(QBrush(QColor(230, 230, 230)))
        self.result_table.setItem(row, 0, summary)
        self.result_table.setSpan(row, 0, 1, 4)

        self.statusBar().showMessage(f"Лексем: {total_lexemes}, ошибок: {total_errors}")

    def _display_lexeme(self, token):
        if token.type == "WHITESPACE":
            if "\t" in token.lexeme:
                return "(табуляция)"
            return "(пробел)"
        return token.lexeme

    def _on_table_clicked(self, item):
        row = item.row()
        location_item = self.result_table.item(row, 3)
        if not location_item:
            return

        text = location_item.text()
        import re
        m = re.match(r"строка (\d+), \[(\d+):(\d+)\]", text)
        if not m:
            return

        line_num = int(m.group(1))
        start_col = int(m.group(2))
        end_col = int(m.group(3))

        cursor = self.editor.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        for _ in range(line_num - 1):
            cursor.movePosition(cursor.MoveOperation.Down)

        cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveMode.MoveAnchor, start_col - 1)
        cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveMode.KeepAnchor, end_col - start_col + 1)

        self.editor.setTextCursor(cursor)
        self.editor.setFocus()

    def _on_show_text_info(self, title, text):
        QMessageBox.information(self, title, text)

    def _on_show_help(self):
        text = (
            "<b>Файл</b><br>"
            "Создать (Ctrl+N) - создание нового документа.<br>"
            "Открыть (Ctrl+O) - открытие текстового файла.<br>"
            "Сохранить (Ctrl+S) - сохранение текущего документа.<br>"
            "Сохранить как (Ctrl+Shift+S) - сохранение под новым именем.<br>"
            "Выход (Alt+F4) - завершение работы программы.<br><br>"
            "<b>Правка</b><br>"
            "Отменить (Ctrl+Z) - отмена последнего действия.<br>"
            "Повторить (Ctrl+Y) - повтор отменённого действия.<br>"
            "Вырезать (Ctrl+X) - удаление выделенного текста в буфер обмена.<br>"
            "Копировать (Ctrl+C) - копирование выделенного текста.<br>"
            "Вставить (Ctrl+V) - вставка текста из буфера обмена.<br>"
            "Удалить (Delete) - удаление выделенного текста.<br>"
            "Выделить всё (Ctrl+A) - выделение всего текста.<br><br>"
            "<b>Текст</b><br>"
            "Содержит информационные разделы, связанные с языковым процессором.<br><br>"
            "<b>Пуск (F5)</b><br>"
            "Запуск анализа исходного текста.<br><br>"
            "<b>Справка (F1)</b><br>"
            "Вызов этого руководства и сведений о программе."
        )
        QMessageBox.information(self, "Справка", text)

    def _on_show_about(self):
        text = (
            f"<b>{APP_TITLE}</b><br><br>"
            "Лабораторная работа №1<br>"
            "«Разработка пользовательского интерфейса (GUI) для языкового процессора»<br><br>"
            "<b>Тема:</b> Объявление структуры на языке Java<br><br>"
            "<b>Автор:</b> Башинов Арья Игоревич, группа АП-326"
        )
        QMessageBox.about(self, "О программе", text)

    def closeEvent(self, event):
        if self._maybe_save():
            event.accept()
        else:
            event.ignore()


def run():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, Qt.white)
    palette.setColor(QPalette.ColorRole.WindowText, Qt.black)
    palette.setColor(QPalette.ColorRole.Base, Qt.white)
    palette.setColor(QPalette.ColorRole.Text, Qt.black)
    palette.setColor(QPalette.ColorRole.Button, Qt.white)
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.black)
    palette.setColor(QPalette.ColorRole.Highlight, Qt.blue)
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.white)
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    return app.exec()