import sys, random, json, os.path
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout, \
    QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QGroupBox, QSpinBox, \
    QMessageBox
from PyQt5.QtCore import pyqtSlot


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.inputs = []

        self.setWindowTitle("Natural Password Generator")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.grid_layout = QGridLayout()
        central_widget.setLayout(self.grid_layout)

        self.create_buttons()
        self.create_input()
        self.create_output()

        self.grid_layout.setRowStretch(0, 0)
        self.grid_layout.setRowStretch(1, 0)
        self.grid_layout.setRowStretch(2, 1)
        self.grid_layout.setRowStretch(3, 1)
        self.grid_layout.setRowStretch(4, 1)

        if os.path.isfile("input.current"):
            self.restore()
        else:
            self.create_default()

    def closeEvent(self, _):
        self.save()

    def create_buttons(self):
        generate_password_btn = QPushButton("Generate Password", self)
        help_btn = QPushButton("Help && Tips", self)
        clear_output_btn = QPushButton("Clear Output", self)
        add_words_btn = QPushButton("Add Words Field", self)
        add_digits_btn = QPushButton("Add Digit(s) Field", self)
        add_characters_btn = QPushButton("Add Character(s) Field", self)

        generate_password_btn.clicked.connect(self.generate_password)
        help_btn.clicked.connect(self.help)
        clear_output_btn.clicked.connect(self.clear_output)
        add_words_btn.clicked.connect(self.create_words_field)
        add_digits_btn.clicked.connect(self.create_digits_field)
        add_characters_btn.clicked.connect(self.create_characters_field)

        self.grid_layout.addWidget(generate_password_btn, 0, 0, QtCore.Qt.AlignTop)
        self.grid_layout.addWidget(help_btn, 0, 1, QtCore.Qt.AlignTop)
        self.grid_layout.addWidget(clear_output_btn, 0, 2, QtCore.Qt.AlignTop)
        self.grid_layout.addWidget(add_words_btn, 1, 0, QtCore.Qt.AlignTop)
        self.grid_layout.addWidget(add_digits_btn, 1, 1, QtCore.Qt.AlignTop)
        self.grid_layout.addWidget(add_characters_btn, 1, 2, QtCore.Qt.AlignTop)
        
    def create_output(self):
        group = QGroupBox("Output:", self)
        layout = QVBoxLayout()
        group.setLayout(layout)
        group.setMinimumWidth(200)
        self.output = QTextEdit(self)
        layout.addWidget(self.output)
        self.grid_layout.addWidget(group, 0, 3, 8, 1)

    def create_input(self):
        widget = QWidget(self)
        self.inputWidget = QHBoxLayout()
        self.inputWidget.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(self.inputWidget)
        self.grid_layout.addWidget(widget, 2, 0, 6, 3)

    @pyqtSlot()
    def create_words_field(self):
        self.inputs.append(WordInput(self.inputWidget))

    @pyqtSlot()
    def create_digits_field(self):
        self.inputs.append(DigitsInput(self.inputWidget))

    @pyqtSlot()
    def create_characters_field(self):
        self.inputs.append(CharactersInput(self.inputWidget))

    @pyqtSlot()
    def generate_password(self):
        password = ""
        for x in self.inputs:
            password += x.get_string()
        self.output.append(password)
        self.output.repaint()

    @pyqtSlot()
    def clear_output(self):
        self.output.clear()
        self.output.repaint()

    @pyqtSlot()
    def help(self):
        msg_box = QMessageBox()
        msg_box.setMinimumSize(500, 1000)
        msg_box.setWindowTitle("Natural Password Generator")
        msg_box.setText("<h2>Help & Tips</h2>")
        msg_box.setInformativeText(
            """
                <h3>Words input</h3>
                TDB<br/>
                <h3>Digits input</h3>
                TDB<br/>
                <h3>Character input</h3>
                TDB<br/>
                <br/>
                Please report any issues at: <br/>
                TDB<br/>
            """
            )
        msg_box.setTextFormat(QtCore.Qt.RichText)
        msg_box.setStandardButtons(QMessageBox.Close)
        msg_box.setDefaultButton(QMessageBox.Close)
        msg_box.exec()

    def save(self):
        data = {}
        data['inputs'] = []
        for x in self.inputs:
            data['inputs'].append(x.serialize())
        with open('input.current', 'w') as outfile:
            json.dump(data, outfile, sort_keys=False, indent=4, separators=(',', ': '))

    def restore(self):
        with open('input.current') as json_file:
            data = json.load(json_file)
            for i in data['inputs']:
                if i['type'] == "words":
                    self.create_words_field()
                elif i['type'] == "digits":
                    self.create_digits_field()
                elif i['type'] == "characters":
                    self.create_characters_field()
                self.inputs[-1].deserialize(i)

    def create_default(self):
        self.create_words_field()
        self.create_words_field()
        self.create_digits_field()

class WordInput:
    def __init__(self, parent):
        group = QGroupBox("Words")
        layout = QGridLayout()
        group.setLayout(layout)
        group.setFixedWidth(170)

        self.words_field = QTextEdit()
        layout.addWidget(self.words_field, 0, 0)

        remove_btn = QPushButton("Remove")
        layout.addWidget(remove_btn, 1, 0)

        parent.addWidget(group, QtCore.Qt.AlignTop)

    def clean_up(self):
        pass

    def get_string(self):
        texts = self.words_field.toPlainText().splitlines()
        texts = [text.strip() for text in texts] # remove whitespace
        texts = [text for text in texts if text] # remove empty

        if len(texts) == 0:
            return ""

        return random.choice(texts)

    def serialize(self):
        return {
            'type': 'words',
            'input': self.words_field.toPlainText()
        }

    def deserialize(self, data):
        self.words_field.setPlainText(data['input'])


class DigitsInput:
    def __init__(self, parent):
        group = QGroupBox("Digit(s)")
        layout = QVBoxLayout()
        group.setLayout(layout)
        group.setFixedWidth(170)

        num_label = QLabel("Number of digits:")
        layout.addWidget(num_label, QtCore.Qt.AlignBottom)

        self.spin = QSpinBox()
        self.spin.setRange(1, 100)
        layout.addWidget(self.spin, QtCore.Qt.AlignTop)

        layout.addStretch(2000)

        remove_btn = QPushButton("Remove")
        layout.addWidget(remove_btn, QtCore.Qt.AlignBottom)

        parent.addWidget(group, QtCore.Qt.AlignTop)

    def clean_up(self):
        pass

    def get_string(self):
        text = ""
        num = self.spin.value()
        for _ in range(num):
            text += str(random.randint(0, 9))
        return text

    def serialize(self):
        return {
            'type': 'digits',
            'input': self.spin.value()
        }

    def deserialize(self, data):
        self.spin.setValue(data['input'])

class CharactersInput:
    def __init__(self, parent):
        group = QGroupBox("Character(s)")
        layout = QVBoxLayout()
        group.setLayout(layout)
        group.setFixedWidth(170)

        num_label = QLabel("Number of characters:")
        layout.addWidget(num_label, QtCore.Qt.AlignBottom)

        self.spin = QSpinBox()
        self.spin.setRange(1, 100)
        layout.addWidget(self.spin, QtCore.Qt.AlignTop)

        layout.addStretch(2000)

        remove_btn = QPushButton("Remove")
        layout.addWidget(remove_btn, QtCore.Qt.AlignBottom)

        parent.addWidget(group, QtCore.Qt.AlignTop)

    def clean_up(self):
        pass

    def get_string(self):
        chars = ['!', '#', '_', '-', '&', '%']

        text = ""
        num = self.spin.value()
        for _ in range(num):
            text += random.choice(chars)

        return text

    def serialize(self):
        return {
            'type': 'characters',
            'input': self.spin.value()
        }

    def deserialize(self, data):
        self.spin.setValue(data['input'])


if __name__ == "__main__":
    APP = QtWidgets.QApplication(sys.argv)
    WIN = MainWindow()
    WIN.show()
    sys.exit(APP.exec_())