import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QWidget, QHBoxLayout

class JsonEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('JSON Editor')
        self.setGeometry(100, 100, 800, 600)

        self.table_widget = QTableWidget()
        self.load_button = QPushButton('Load JSON')
        self.save_button = QPushButton('Save JSON')
        self.new_button = QPushButton('Create New JSON')

        self.load_button.clicked.connect(self.load_json)
        self.save_button.clicked.connect(self.save_json)
        self.new_button.clicked.connect(self.create_new_json)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.new_button)

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_json(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r',encoding="utf-8") as file:
                    self.json_data = json.load(file)
                    self.populate_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not load file: {e}")

    def populate_table(self):
        if not isinstance(self.json_data, list) or not all(isinstance(item, dict) for item in self.json_data):
            QMessageBox.critical(self, "Error", "Invalid JSON format")
            return

        keys = set().union(*(d.keys() for d in self.json_data))
        self.table_widget.setColumnCount(len(keys))
        self.table_widget.setRowCount(len(self.json_data))
        self.table_widget.setHorizontalHeaderLabels(keys)

        for row, item in enumerate(self.json_data):
            for col, key in enumerate(keys):
                value = item.get(key, "")
                self.table_widget.setItem(row, col, QTableWidgetItem(str(value)))

    def save_json(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save JSON File", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            try:
                keys = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]
                data = []
                for row in range(self.table_widget.rowCount()):
                    item = {keys[col]: self.table_widget.item(row, col).text() for col in range(self.table_widget.columnCount())}
                    data.append(item)
                with open(file_name, 'w',encoding="utf-8") as file:
                    json.dump(data, file, indent=4)
                QMessageBox.information(self, "Success", "File saved successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {e}")

    def create_new_json(self):
        self.json_data = []
        self.populate_table_with_template()

    def populate_table_with_template(self):
        keys = ["机器码", "任务名", "标志", "最晚执行时间"]  # 可扩展的初始属性
        self.table_widget.setColumnCount(len(keys))
        self.table_widget.setRowCount(0)
        self.table_widget.setHorizontalHeaderLabels(keys)

        # 添加一行空白数据
        self.table_widget.insertRow(0)
        for col, key in enumerate(keys):
            self.table_widget.setItem(0, col, QTableWidgetItem(""))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = JsonEditor()
    editor.show()
    sys.exit(app.exec_())
