import sys
import json

from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, \
    QFileDialog, QMessageBox, QWidget, QHBoxLayout, QDialog, QDateTimeEdit


class TimeModifyDialog(QDialog):

    def __init__(self, timestamp, parent=None):
        super(TimeModifyDialog, self).__init__(parent)

        self.timestamp = timestamp

        self.setWindowTitle("修改时间")

        # 将时间戳转换为QDateTime对象

        self.dateTime = QDateTime.fromMSecsSinceEpoch(timestamp)

        # 创建QDateTimeEdit并设置初始时间

        self.dateTimeEdit = QDateTimeEdit(self)

        self.dateTimeEdit.setDateTime(self.dateTime)

        self.dateTimeEdit.setCalendarPopup(True)

        # 布局

        layout = QVBoxLayout(self)

        layout.addWidget(self.dateTimeEdit)

        # 设置按钮

        self.okButton = QPushButton("确定", self)

        self.okButton.clicked.connect(self.accept)

        layout.addWidget(self.okButton)

        # 初始化对话框大小

        self.setLayout(layout)

    def getTimeStamp(self):
        # 获取修改后的时间并转换回时间戳
        return self.dateTimeEdit.dateTime().toMSecsSinceEpoch()


class JsonEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.that = self
        self.aa = []
        self.setWindowTitle('JSON Editor')
        self.setGeometry(100, 100, 800, 600)
        self.keys = ['机器码', '标志', '参数', '任务名', '最晚执行时间', "操作"]

        self.table_widget = QTableWidget()
        self.load_button = QPushButton('Load JSON')
        self.save_button = QPushButton('Save JSON')
        self.new_button = QPushButton('Create New JSON')
        self.add_row_button = QPushButton('Add Row')

        self.load_button.clicked.connect(self.load_json)
        self.save_button.clicked.connect(self.save_json)
        self.new_button.clicked.connect(self.create_new_json)
        self.add_row_button.clicked.connect(self.add_row)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.add_row_button)

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.load_json()

    def load_json(self):
        self.aa=[]
        # options = QFileDialog.Options()
        # file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json);;All Files (*)", options=options)
        file_name = "task.json"

        if file_name:
            try:
                with open(file_name, 'r', encoding="utf-8") as file:
                    self.json_data = json.load(file)
                    self.populate_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not load file: {e}")

    def populate_table(self):
        if not isinstance(self.json_data, list) or not all(isinstance(item, dict) for item in self.json_data):
            QMessageBox.critical(self, "Error", "Invalid JSON format")
            return

        self.table_widget.setColumnCount(len(self.keys))
        self.table_widget.setRowCount(len(self.json_data))
        print("keys", self.keys)
        self.table_widget.setHorizontalHeaderLabels(self.keys)

        for row, item in enumerate(self.json_data):
            # print(row,item)
            for col, key in enumerate(self.keys):
                # print(col, key)
                if key == "操作":
                    continue

                value = item.get(key, "")
                self.table_widget.setItem(row, col, QTableWidgetItem(str(value)))
                if key == "最晚执行时间":
                    index = len(self.aa)
                    self.aa.append([value, row, col])
                    button = QPushButton(f"修改时间", self)
                    button.clicked.connect(lambda checked, idx=index: self.openTimeModifyDialog(idx))
                    self.table_widget.setCellWidget(row, col + 1, button)
                    self.table_widget.setItem(row, col + 1, QTableWidgetItem(str("pass")))
                    pass

    def openTimeModifyDialog(self, index):
        value, row, col = self.aa[index]

        # 创建并显示时间修改对话框
        dialog = TimeModifyDialog(int(value), self)
        if dialog.exec_() == QDialog.Accepted:
            # 获取并更新时间戳
            timestamp = dialog.getTimeStamp()
            print(f"修改完毕:{timestamp}")
            print(row, col)
            self.table_widget.setItem(row, col, QTableWidgetItem(str(timestamp)))

    def save_json(self):
        # options = QFileDialog.Options()
        # file_name, _ = QFileDialog.getSaveFileName(self, "Save JSON File", "", "JSON Files (*.json);;All Files (*)", options=options)
        file_name = "task.json"
        if file_name:
            try:
                keys = [self.table_widget.horizontalHeaderItem(i).text() for i in
                        range(self.table_widget.columnCount())]
                data = []
                for row in range(self.table_widget.rowCount()):
                    item = {keys[col]: self.table_widget.item(row, col).text() for col in
                            range(self.table_widget.columnCount())}
                    data.append(item)
                with open(file_name, 'w', encoding="utf-8") as file:
                    json.dump(data, file, indent=4)
                QMessageBox.information(self, "Success", "File saved successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {e}")

    def create_new_json(self):
        self.json_data = []
        self.populate_table_with_template()

    def populate_table_with_template(self):
        self.table_widget.setColumnCount(len(self.keys))
        self.table_widget.setRowCount(0)
        self.table_widget.setHorizontalHeaderLabels(self.keys)

    def add_row(self):
        row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(row_count)
        for col in range(self.table_widget.columnCount()):
            self.table_widget.setItem(row_count, col, QTableWidgetItem(""))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = JsonEditor()
    editor.show()
    sys.exit(app.exec_())
