import sys
import json
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QPushButton, QFileDialog, QMessageBox, QVBoxLayout
from PyQt5.QtCore import Qt

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if not data:
                print("The JSON file is empty.")
                return None
            return data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

class ResultsWindow(QMainWindow):
    def __init__(self, data, identity_threshold):
        super().__init__()
        self.setWindowTitle("Results of Antimicrobial Resistant Genes Analysis")
        self.setGeometry(100, 100, 1500, 800)
        self.identity_threshold = float(identity_threshold)

        # Main widget and layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        if data:
            self.create_table(data)
        else:
            self.display_no_data_message()

        self.export_button = QPushButton("Export to Excel", self)
        self.export_button.clicked.connect(self.export_to_excel)
        self.layout.addWidget(self.export_button)  # Add the export button to the layout

    def create_table(self, data):
        self.tableWidget = QTableWidget()
        self.layout.addWidget(self.tableWidget)  # Add the table to the layout
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        headers = ["RGI Criteria", "ARO Term", "Detection Criteria", "AMR Gene Family", "Drug Class", "Resistance Mechanism", "% Identity"]
        self.tableWidget.setHorizontalHeaderLabels(headers)
        found_data = False

        for key, value in data.items():
            for sub_key, sub_value in value.items():
                if (sub_value.get("type_match", "N/A") in ["Perfect", "Strict", "Loose"] and sub_value.get("partial", "1") == "0" and float(sub_value.get("perc_identity", 0)) >= self.identity_threshold):
                    found_data = True
                    row_position = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_position)
                    self.tableWidget.setItem(row_position, 0, QTableWidgetItem(sub_value.get("type_match", "N/A")))
                    self.tableWidget.setItem(row_position, 1, QTableWidgetItem(sub_value.get("model_name", "N/A")))
                    self.tableWidget.setItem(row_position, 2, QTableWidgetItem(sub_value.get("model_type", "N/A")))
                    self.tableWidget.setItem(row_position, 3, QTableWidgetItem(", ".join([v.get("category_aro_name", "N/A") for k, v in sub_value.get("ARO_category", {}).items() if "AMR Gene Family" in v.get("category_aro_class_name", "")])))
                    self.tableWidget.setItem(row_position, 4, QTableWidgetItem(", ".join([v.get("category_aro_name", "N/A") for k, v in sub_value.get("ARO_category", {}).items() if "Drug Class" in v.get("category_aro_class_name", "")])))
                    self.tableWidget.setItem(row_position, 5, QTableWidgetItem(", ".join([v.get("category_aro_name", "N/A") for k, v in sub_value.get("ARO_category", {}).items() if "Resistance Mechanism" in v.get("category_aro_class_name", "")])))
                    self.tableWidget.setItem(row_position, 6, QTableWidgetItem(str(sub_value.get("perc_identity", "N/A"))))

        if not found_data:
            self.display_no_data_message()
        else:
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def export_to_excel(self):
        filename = QFileDialog.getSaveFileName(self, 'Save File', '', 'Excel files (*.xlsx)')[0]
        if filename:
            if not filename.endswith('.xlsx'):
                filename += '.xlsx'
            column_headers = [self.tableWidget.horizontalHeaderItem(i).text() for i in range(self.tableWidget.columnCount())]
            df = pd.DataFrame(columns=column_headers)
            for row in range(self.tableWidget.rowCount()):
                row_data = [self.tableWidget.item(row, column).text() if self.tableWidget.item(row, column) else '' for column in range(self.tableWidget.columnCount())]
                df.loc[row] = row_data
            df.to_excel(filename, index=False)
            QMessageBox.information(self, "Export Successful", "The data was exported successfully to " + filename)

    def display_no_data_message(self):
        self.label = QLabel("No antimicrobial resistant genes found!", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)  # Add the label to the layout

def main():
    app = QApplication(sys.argv)
    if len(sys.argv) > 2:
        rgi_output_json_path = sys.argv[1]
        identity_threshold = sys.argv[2]
    else:
        print("Usage: python results.py <path_to_json> <identity_threshold>")
        sys.exit(1)

    data = load_json(rgi_output_json_path)
    ex = ResultsWindow(data, identity_threshold)
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
