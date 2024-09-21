
import pandas as pd
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox, QFormLayout, QMessageBox
)
from sqlalchemy import create_engine
import requests

class DataImportDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import Data")
        self.setGeometry(100, 100, 400, 200)
        self.df = None

        self.layout = QVBoxLayout()

        self.data_source_label = QLabel("Select Data Source Type:")
        self.data_source_type = QComboBox()
        self.data_source_type.addItems(["csv", "excel", "json", "sql", "api", "dta"])
        self.data_source_type.currentIndexChanged.connect(self.on_data_source_change)

        self.file_path_label = QLabel("File Path:")
        self.file_path_input = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)

        self.delimiter_label = QLabel("Delimiter (for CSV):")
        self.delimiter_input = QLineEdit(";")

        self.sql_connection_label = QLabel("SQL Connection String:")
        self.sql_connection_input = QLineEdit()

        self.sql_query_label = QLabel("SQL Query:")
        self.sql_query_input = QLineEdit()

        self.api_url_label = QLabel("API URL:")
        self.api_url_input = QLineEdit()

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.load_data)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow(self.data_source_label, self.data_source_type)
        form_layout.addRow(self.file_path_label, self.file_path_input)
        form_layout.addRow("", self.browse_button)
        form_layout.addRow(self.delimiter_label, self.delimiter_input)
        form_layout.addRow(self.sql_connection_label, self.sql_connection_input)
        form_layout.addRow(self.sql_query_label, self.sql_query_input)
        form_layout.addRow(self.api_url_label, self.api_url_input)

        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)
        self.setLayout(self.layout)

        self.on_data_source_change(0) 

    def on_data_source_change(self, index):
        data_source = self.data_source_type.currentText()

        self.file_path_input.setVisible(False)
        self.browse_button.setVisible(False)
        self.delimiter_label.setVisible(False)
        self.delimiter_input.setVisible(False)
        self.sql_connection_label.setVisible(False)
        self.sql_connection_input.setVisible(False)
        self.sql_query_label.setVisible(False)
        self.sql_query_input.setVisible(False)
        self.api_url_label.setVisible(False)
        self.api_url_input.setVisible(False)

        if data_source in ['csv', 'excel', 'json', 'dta']:
            self.file_path_input.setVisible(True)
            self.browse_button.setVisible(True)
            if data_source == 'csv':
                self.delimiter_label.setVisible(True)
                self.delimiter_input.setVisible(True)
        elif data_source == 'sql':
            self.sql_connection_label.setVisible(True)
            self.sql_connection_input.setVisible(True)
            self.sql_query_label.setVisible(True)
            self.sql_query_input.setVisible(True)
        elif data_source == 'api':
            self.api_url_label.setVisible(True)
            self.api_url_input.setVisible(True)

    def browse_file(self):

        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            self.file_path_input.setText(file_path)

    def load_data(self):
        data_source = self.data_source_type.currentText()

        try:
            if data_source == 'csv':
                file_path = self.file_path_input.text()
                delimiter = self.delimiter_input.text()
                self.df = pd.read_csv(file_path, delimiter=delimiter)
            elif data_source == 'excel':
                file_path = self.file_path_input.text()
                self.df = pd.read_excel(file_path)
            elif data_source == 'json':
                file_path = self.file_path_input.text()
                self.df = pd.read_json(file_path)
            elif data_source == 'dta':
                file_path = self.file_path_input.text()
                self.df = pd.read_stata(file_path)
            elif data_source == 'sql':
                connection_string = self.sql_connection_input.text()
                query = self.sql_query_input.text()
                engine = create_engine(connection_string)
                self.df = pd.read_sql(query, engine)
            elif data_source == 'api':
                api_url = self.api_url_input.text()
                response = requests.get(api_url)
                self.df = pd.DataFrame(response.json())  
            else:
                raise ValueError("Unsupported data source type.")

            self.accept()  

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def get_dataframe(self):
        return self.df
