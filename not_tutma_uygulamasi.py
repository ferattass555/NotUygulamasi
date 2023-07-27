import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox, QCalendarWidget, QTimeEdit, QListWidget, QDialog, QLineEdit, QListWidgetItem, QInputDialog, QVBoxLayout, QGroupBox, QFileDialog

from PyQt5.QtCore import QDateTime, QDate, Qt, QTimer, QTime, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette

class NoteTakingApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        self.notes = {}
        self.load_notes()  # Load saved notes
        self.init_ui()

        # Start timer to check for reminders every minute
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_reminders)
        self.timer.start(60000)  # Check every minute, you can adjust this frequency if needed

        # Create a widget instance to show notes
        self.notes_widget = NotesWidget(self.notes)
        self.notes_widget.update_signal.connect(self.populate_notes_listwidget)
        self.notes_widget.delete_signal.connect(self.populate_notes_listwidget)

    def init_ui(self):
        self.setWindowTitle('Note Taking Application')
        self.setGeometry(100, 100, 600, 400)

        # Set colors
        palette = self.palette()
        bg_color = QColor(120, 168, 240)  # Dark blue background color (RGB color code: 120, 168, 240)
        text_color = QColor(240, 240, 240)  # White text color
        button_color = QColor(83, 102, 84)  # Green button color
        palette.setColor(QPalette.Window, bg_color)
        palette.setColor(QPalette.WindowText, text_color)
        palette.setColor(QPalette.Base, QColor(70, 80, 96))  # Dark blue text area color
        palette.setColor(QPalette.Button, button_color)
        palette.setColor(QPalette.ButtonText, text_color)
        self.setPalette(palette)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.input_layout = QVBoxLayout()
        self.layout.addLayout(self.input_layout)

        self.note_label = QLabel('Note:')
        self.note_label.setStyleSheet("font-weight: bold; color: white;")
        self.input_layout.addWidget(self.note_label)

        self.note_edit = QTextEdit()
        self.input_layout.addWidget(self.note_edit)

        self.datetime_layout = QHBoxLayout()
        self.input_layout.addLayout(self.datetime_layout)

        self.date_label = QLabel('Date:')
        self.date_label.setStyleSheet("font-weight: bold; color: white;")
        self.datetime_layout.addWidget(self.date_label)

        self.calendar = QCalendarWidget()
        self.datetime_layout.addWidget(self.calendar)

        self.time_label = QLabel('Time:')
        self.time_label.setStyleSheet("font-weight: bold; color: white;")
        self.datetime_layout.addWidget(self.time_label)

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat('HH:mm')
        self.datetime_layout.addWidget(self.time_edit)

        self.save_button = QPushButton('Save')
        self.save_button.setStyleSheet("font-weight: bold; color: black;")
        self.save_button.clicked.connect(self.save_note)
        self.layout.addWidget(self.save_button)

        self.show_notes_button = QPushButton('Show Notes')
        self.show_notes_button.setStyleSheet("font-weight: bold; color: black;")
        self.show_notes_button.clicked.connect(self.show_notes)
        self.layout.addWidget(self.show_notes_button)

        self.update_file_button = QPushButton('Update File')
        self.update_file_button.setStyleSheet("font-weight: bold; color: black;")
        self.update_file_button.clicked.connect(self.update_file)
        self.layout.addWidget(self.update_file_button)

        # Create a list widget to show notes
        self.notes_listwidget = QListWidget()
        self.notes_listwidget.itemDoubleClicked.connect(self.open_file)
        self.layout.addWidget(self.notes_listwidget)

    def save_note(self):
        note = self.note_edit.toPlainText()
        date = self.calendar.selectedDate()
        time = self.time_edit.time()
        datetime = QDateTime(date, time)

        note_index = len(self.notes) + 1
        self.notes[note_index] = {'datetime': datetime, 'note_content': note}

        self.note_edit.clear()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.time_edit.setTime(QTime.currentTime())

        print("Note successfully saved!")
        self.populate_notes_listwidget()

    def populate_notes_listwidget(self):
        self.notes_listwidget.clear()
        for note_index, note_data in self.notes.items():
            datetime = note_data['datetime']
            note_content = note_data['note_content']
            item = QListWidgetItem(f"{note_index}.note | {note_content} | {datetime.toString('dd.MM.yyyy HH:mm')}")
            self.notes_listwidget.addItem(item)

    def delete_note(self):
        selected_item = self.notes_listwidget.currentItem()
        if not selected_item:
            return

        response = QMessageBox.question(self, "Delete Note", "Are you sure you want to delete the selected note?", QMessageBox.Yes | QMessageBox.No)

        if response == QMessageBox.Yes:
            selected_text = selected_item.text()
            note_index_str, _, _ = selected_text.partition('|')
            note_index = int(note_index_str.strip()[:-4])

            if note_index in self.notes:
                self.notes.pop(note_index)
                self.populate_notes_listwidget()

    def save_notes(self):
        file_path = os.path.join(os.path.dirname(__file__), "notes.txt")
        with open(file_path, 'w') as file:
            for note_index, note_data in self.notes.items():
                datetime = note_data['datetime']
                note_content = note_data['note_content']
                file.write(f"{note_index}|{datetime.toString('dd.MM.yyyy HH:mm')}|{note_content}\n")

    def load_notes(self):
        file_path = os.path.join(os.path.dirname(__file__), "notes.txt")
        if not os.path.exists(file_path):
            # Create an empty file if it doesn't exist
            with open(file_path, 'w'):
                pass

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines
                    note_index_str, datetime_str, note = line.split('|')
                    note_index = int(note_index_str)
                    datetime = QDateTime.fromString(datetime_str, 'dd.MM.yyyy HH:mm')
                    self.notes[note_index] = {'datetime': datetime, 'note_content': note}
        except FileNotFoundError:
            pass
        except Exception as e:
            print("Error:", str(e))

    def check_reminders(self):
        current_datetime = QDateTime.currentDateTime()

        future_reminder_exists = False
        reminder_exists = False

        for note_data in self.notes.values():
            datetime = note_data['datetime']
            if current_datetime >= datetime:
                reminder_exists = True
            else:
                future_reminder_exists = True

        if reminder_exists and future_reminder_exists:
            self.setWindowTitle('Note Taking Application - Reminder!')
        elif reminder_exists:
            self.setWindowTitle('Note Taking Application - Reminder Approaching!')
        else:
            self.setWindowTitle('Note Taking Application')

    def show_reminder_popup(self, datetime, note):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Reminder')
        msg.setText(f"Your note for {datetime.toString('dd.MM.yyyy HH:mm')}:")
        msg.setInformativeText(note)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def show_notes(self):
        dialog = NotesWidget(self.notes)
        dialog.update_signal.connect(self.populate_notes_listwidget)
        dialog.delete_signal.connect(self.populate_notes_listwidget)

        palette = self.palette()
        bg_color = QColor(120, 168, 240)
        text_color = QColor(240, 240, 240)
        button_color = QColor(83, 102, 84)
        palette.setColor(QPalette.Window, bg_color)
        palette.setColor(QPalette.WindowText, text_color)
        palette.setColor(QPalette.Base, QColor(70, 80, 96))
        palette.setColor(QPalette.Button, button_color)
        palette.setColor(QPalette.ButtonText, text_color)
        dialog.setPalette(palette)

        dialog.exec_()

    def populate_notes_listwidget(self):
        self.notes_listwidget.clear()
        for note_index, note_data in self.notes.items():
            datetime = note_data['datetime']
            note_content = note_data['note_content']
            item = QListWidgetItem(f"{note_index}.note | {note_content} | {datetime.toString('dd.MM.yyyy HH:mm')}")
            self.notes_listwidget.addItem(item)

    def update_file(self):
        self.save_notes()
        print("Notes have been updated in the file!")

    def open_file(self, item):
        selected_text = item.text()
        note_index_str, _, _ = selected_text.partition('|')
        note_index = int(note_index_str.strip()[:-4])

        if note_index in self.notes:
            note_data = self.notes[note_index]
            datetime = note_data['datetime']
            note_content = note_data['note_content']
            file_name = f"{datetime.toString('yyyyMMdd_HHmmss')}.txt"

            with open(file_name, 'w') as file:
                file.write(note_content)

            print(f"File created: {file_name}")
            os.startfile(file_name)

class NotesWidget(QDialog):
    update_signal = pyqtSignal()
    delete_signal = pyqtSignal()

    def __init__(self, notes):
        super().__init__()

        self.notes = notes
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Notes')
        self.setGeometry(200, 200, 600, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.notes_listwidget = QListWidget()
        self.layout.addWidget(self.notes_listwidget)

        self.groupbox = QGroupBox("Options")
        self.groupLayout = QVBoxLayout()
        self.groupbox.setLayout(self.groupLayout)

        self.update_button = QPushButton('Update')
        self.update_button.setStyleSheet("font-weight: bold; color: black;")
        self.update_button.clicked.connect(self.update_note)
        self.groupLayout.addWidget(self.update_button)

        self.delete_button = QPushButton('Delete')
        self.delete_button.setStyleSheet("font-weight: bold; color: black;")
        self.delete_button.clicked.connect(self.delete_note)
        self.groupLayout.addWidget(self.delete_button)

        self.layout.addWidget(self.groupbox)

        self.populate_notes_listwidget()

    def populate_notes_listwidget(self):
        self.notes_listwidget.clear()
        for note_index, note_data in self.notes.items():
            datetime = note_data['datetime']
            note_content = note_data['note_content']
            item = QListWidgetItem(f"{note_index}.note | {note_content} | {datetime.toString('dd.MM.yyyy HH:mm')}")
            self.notes_listwidget.addItem(item)

    def update_note(self):
        selected_item = self.notes_listwidget.currentItem()
        if not selected_item:
            return

        selected_text = selected_item.text()
        note_index_str, _, _ = selected_text.partition('|')
        note_index = int(note_index_str.strip()[:-4])

        if note_index in self.notes:
            note_data = self.notes[note_index]
            datetime = note_data['datetime']
            note_content = note_data['note_content']
            new_note, ok_pressed = QInputDialog.getText(self, "Update Note", "New note:", QLineEdit.Normal, note_content)

            if ok_pressed and new_note.strip():
                self.notes[note_index]['note_content'] = new_note.strip()
                self.update_signal.emit()
                self.populate_notes_listwidget()

    def delete_note(self):
        selected_item = self.notes_listwidget.currentItem()
        if not selected_item:
            return

        response = QMessageBox.question(self, "Delete Note", "Are you sure you want to delete the selected note?", QMessageBox.Yes | QMessageBox.No)

        if response == QMessageBox.Yes:
            selected_text = selected_item.text()
            note_index_str, _, _ = selected_text.partition('|')
            note_index = int(note_index_str.strip()[:-4])

            if note_index in self.notes:
                self.notes.pop(note_index)
                self.delete_signal.emit()
                self.populate_notes_listwidget()

# Main part creating the main application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = NoteTakingApplication()
    application.show()
    sys.exit(app.exec_())
