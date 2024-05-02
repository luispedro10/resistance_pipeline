import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLabel, QHeaderView
from PyQt5.QtCore import Qt  # Importación faltante para usar Qt.AlignCenter


def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if not data:  # Verifica si el contenido del JSON está vacío
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
        self.identity_threshold = float(identity_threshold)  # Guarda el umbral como un atributo, convertido a float
        print("Received Identity Threshold in ResultsWindow:", self.identity_threshold)  # Confirmar el valor recibido
        if data:
            self.create_table(data)
        else:
            self.display_no_data_message()

    def create_table(self, data):
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        headers = ["RGI Criteria", "ARO Term", "Detection Criteria", "AMR Gene Family", "Drug Class", "Resistance Mechanism", "% Identity"]
        self.tableWidget.setHorizontalHeaderLabels(headers)
        found_data = False

        for key, value in data.items():
            for sub_key, sub_value in value.items():
                if (sub_value.get("type_match", "N/A") in ["Perfect", "Strict", "Loose"]
                    and sub_value.get("partial", "1") == "0"
                    and float(sub_value.get("perc_identity", 0)) >= self.identity_threshold):  # Usa el atributo de la clase
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

    def display_no_data_message(self):
        self.label = QLabel("No antimicrobial resistant genes found!", self)
        self.setCentralWidget(self.label)
        self.label.setAlignment(Qt.AlignCenter)  # Correctamente referenciado

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
