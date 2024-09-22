
import pandas as pd
from PyQt5.QtWidgets import (
    QMainWindow, QTableView, QAction, QVBoxLayout, QWidget, QLineEdit,
    QPushButton, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QSplitter,
    QDockWidget, QFileDialog, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager
from .data_import_dialog import DataImportDialog
from .observable_dataframe import ObservableDataFrame
from .dataframe_model import DataFrameModel
from .themes import light_theme, dark_theme, solarized_dark_theme, solarized_light_theme, monokai_theme, shades_of_purple_theme, vue_theme
from IPython import get_ipython
from PyQt5.QtGui import QIcon
import os

class DataViewer(QMainWindow):
    def __init__(self, df=None):
        super().__init__()
        
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
        self.setWindowIcon(QIcon(icon_path))
        
        if df is not None:
            if not isinstance(df, ObservableDataFrame):
                df = ObservableDataFrame(df)
        else:
            df = ObservableDataFrame(pd.DataFrame())

        self.df = df
        self.df.register_change_callback(self.on_dataframe_changed)
        self.filtered_df = self.df
        
        self.model = DataFrameModel(self.df)
        self.view = QTableView()
        self.view.setModel(self.model)
        self.search_results = []
        self.current_search_index = -1

        self.setWindowTitle("My DataViewer")
        self.setGeometry(100, 100, 800, 600)

        self.add_console_dock()
        self.apply_theme(light_theme)
        self.create_import_menu()
        self.create_console_menu()

        self.theme_menu = self.menuBar().addMenu("Themes")
        self.create_theme_menu()

        self.font_menu = self.menuBar().addMenu("Fonts")
        self.create_font_menu()

        self.variable_table = QTableWidget()
        self.variable_table.setColumnCount(2)
        self.variable_table.setHorizontalHeaderLabels(["Variable", "Type"])
        self.update_variable_table()

        self.sidebar_label = QLabel("", self)
        self.sidebar_label.setAlignment(Qt.AlignCenter)
        self.sidebar_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(self.sidebar_label)
        sidebar_layout.addWidget(self.variable_table)

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)

        self.search_bar = QLineEdit(self)
        self.search_button = QPushButton("Search", self)
        self.reset_button = QPushButton("Reset", self)

        self.search_button.clicked.connect(self.search_data)
        self.search_bar.returnPressed.connect(self.navigate_or_search)  
        self.reset_button.clicked.connect(self.reset_search)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.reset_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.view)
        main_layout.addLayout(search_layout)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(sidebar_widget)  
        splitter.addWidget(main_widget)     
        splitter.setSizes([200, 800]) 

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.addWidget(splitter)
        container.setLayout(container_layout)
        self.setCentralWidget(container)

        self.apply_styles()
        self.view.viewport().installEventFilter(self)
        self.view.verticalScrollBar().valueChanged.connect(self.handle_scrollbar_position)

        header = self.view.horizontalHeader()
        header.sectionClicked.connect(self.on_header_click)

    def create_theme_menu(self):
        light_action = QAction("Light Theme", self)
        dark_action = QAction("Dark Theme", self)
        solarized_action = QAction("Solarized Dark", self)
        solarized_light_action = QAction("Solarized Light Theme", self)  
        monokai_action = QAction("Monokai Theme", self) 
        shades_of_purple_action = QAction("Shades of Purple Theme", self)  
        vue_action = QAction("Vue Theme", self)  


        light_action.triggered.connect(lambda: self.apply_theme(light_theme))
        dark_action.triggered.connect(lambda: self.apply_theme(dark_theme))
        solarized_action.triggered.connect(lambda: self.apply_theme(solarized_dark_theme))
        solarized_light_action.triggered.connect(lambda: self.apply_theme(solarized_light_theme)) 
        monokai_action.triggered.connect(lambda: self.apply_theme(monokai_theme))  
        shades_of_purple_action.triggered.connect(lambda: self.apply_theme(shades_of_purple_theme))  
        vue_action.triggered.connect(lambda: self.apply_theme(vue_theme))  

        self.theme_menu.addAction(light_action)
        self.theme_menu.addAction(dark_action)
        self.theme_menu.addAction(solarized_action)
        self.theme_menu.addAction(solarized_light_action) 
        self.theme_menu.addAction(monokai_action)
        self.theme_menu.addAction(shades_of_purple_action) 
        self.theme_menu.addAction(vue_action) 

    def create_font_menu(self):
        arial_action = QAction("Arial", self)
        courier_action = QAction("Courier New", self)
        times_action = QAction("Times New Roman", self)
        georgia_action = QAction("Georgia", self)  
        verdana_action = QAction("Verdana", self)  
        consolas_action = QAction("Consolas", self)  

        arial_action.triggered.connect(lambda: self.change_font("Arial"))
        courier_action.triggered.connect(lambda: self.change_font("Courier New"))
        times_action.triggered.connect(lambda: self.change_font("Times New Roman"))
        georgia_action.triggered.connect(lambda: self.change_font("Georgia")) 
        verdana_action.triggered.connect(lambda: self.change_font("Verdana")) 
        consolas_action.triggered.connect(lambda: self.change_font("Consolas"))  

        self.font_menu.addAction(arial_action)
        self.font_menu.addAction(courier_action)
        self.font_menu.addAction(times_action)
        self.font_menu.addAction(georgia_action)  
        self.font_menu.addAction(verdana_action)  
        self.font_menu.addAction(consolas_action) 

    def apply_theme(self, theme):
        self.setStyleSheet(theme)
        if hasattr(self, 'console_widget'):
            self.console_widget.setStyleSheet(theme)


    def change_font(self, font_name):
        font = QFont(font_name)
        self.view.setFont(font)
        self.variable_table.setFont(font)
        self.search_bar.setFont(font)
        self.search_button.setFont(font)
        self.reset_button.setFont(font)
        self.sidebar_label.setFont(font)
        self.update_view()

    def apply_styles(self):
        self.view.setStyleSheet("""
            QHeaderView::section {
                background-color: lightblue;
                color: black;
                font-weight: bold;
                border: 1px solid #6c6c6c;
                padding: 4px;
            }
        """)

        self.variable_table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                font-weight: bold;
                background-color: #f0f0f0;
                padding: 4px;
            }
        """)

        self.variable_table.setStyleSheet("""
            QTableWidget::item {
                padding: 5px;
            }
        """)

    def on_header_click(self, logicalIndex):
        order = self.view.horizontalHeader().sortIndicatorOrder()
        self.model.sort(logicalIndex, order)

    def update_variable_table(self):
        self.variable_table.setRowCount(len(self.df.columns))
        for row, (col, dtype) in enumerate(self.df.dtypes.items()):
            col_item = QTableWidgetItem(col)
            dtype_item = QTableWidgetItem(str(dtype))
            col_item.setTextAlignment(Qt.AlignLeft)
            dtype_item.setTextAlignment(Qt.AlignRight)
            self.variable_table.setItem(row, 0, col_item)
            self.variable_table.setItem(row, 1, dtype_item)

    def search_data(self):
        search_term = self.search_bar.text().strip()
        if not search_term:
            return

        self.view.clearSelection()
        self.search_results = []
        self.current_search_index = -1

        try:
            search_numeric = float(search_term)
            is_numeric = True
        except ValueError:
            is_numeric = False

        rows_to_keep = []
        for row in range(len(self.df)):
            row_has_match = False
            for col in range(len(self.df.columns)):
                cell_value = self.df.iloc[row, col]

                if is_numeric and pd.api.types.is_numeric_dtype(cell_value):
                    if cell_value == search_numeric:
                        row_has_match = True
                        if (row, col) not in self.search_results:
                            self.search_results.append((row, col))
                else:
                    if str(cell_value) == search_term:
                        row_has_match = True
                        if (row, col) not in self.search_results:
                            self.search_results.append((row, col))

            if row_has_match:
                rows_to_keep.append(row)

        self.filtered_df = self.df.iloc[rows_to_keep]
        self.filtered_df = ObservableDataFrame(self.filtered_df)  
        self.filtered_df.register_change_callback(self.on_dataframe_changed)
        self.update_view()

        if self.search_results:
            self.current_search_index = 0
            self.highlight_current_result()
        else:
            print("No matches found.")

    def navigate_or_search(self):
        if self.current_search_index == -1:
            self.search_data()
        else:
            self.next_search_result()

    def reset_search(self):
        self.filtered_df = self.df
        self.update_view()
        self.search_results = []
        self.current_search_index = -1

    def update_view(self):
        self.model = DataFrameModel(self.filtered_df)
        self.view.setModel(self.model)

    def highlight_current_result(self):
        if self.search_results and 0 <= self.current_search_index < len(self.search_results):
            row, col = self.search_results[self.current_search_index]
            index = self.model.index(row % self.model.page_size, col)
            self.view.scrollTo(index)
            self.view.setCurrentIndex(index)
            self.view.selectionModel().select(index, self.view.selectionModel().Select)

    def next_search_result(self):
        if self.search_results:
            self.current_search_index = (self.current_search_index + 1) % len(self.search_results)
            self.highlight_current_result()

    def eventFilter(self, source, event):
        if event.type() == event.Wheel:
            if event.angleDelta().y() > 0:
                self.model.previousPage()
            else:
                self.model.nextPage()
            return True
        return super().eventFilter(source, event)

    def handle_scrollbar_position(self, value):
        scrollbar = self.view.verticalScrollBar()
        if value == scrollbar.minimum():
            self.model.goToFirstPage()
        elif value == scrollbar.maximum():
            self.model.goToLastPage()

    def on_dataframe_changed(self):
        self.model.invalidate_cache()
        self.update_variable_table()


    def create_import_menu(self):
        self.file_menu = self.menuBar().addMenu("Import data")

        import_action = QAction("Import dataframe", self)
        import_action.triggered.connect(self.import_data)

        self.file_menu.addAction(import_action)

    def import_data(self):
        try:
            dialog = DataImportDialog()
            if dialog.exec_() == QDialog.Accepted:
                new_df = dialog.get_dataframe()
                if new_df is not None:

                    self.df.unregister_change_callback(self.on_dataframe_changed)
                    self.df = ObservableDataFrame(new_df)
                    self.df.register_change_callback(self.on_dataframe_changed)

                    self.model = DataFrameModel(self.df)
                    self.view.setModel(self.model)
                    self.update_variable_table()

                    ipython = get_ipython()
                    if ipython is not None and 'ZMQInteractiveShell' in str(type(ipython)):
                        print("Running inside Jupyter. Updating the Jupyter namespace.")
                        ipython.push({'df': self.df})  
                    elif hasattr(self, 'kernel'):
                        print("Updating embedded console namespace.")
                        self.kernel.shell.push({'df': self.df})
                    else:
                        print("Kernel not found. Unable to update console namespace.")

                    QMessageBox.information(self, "Success", "Data loaded successfully.")
                else:
                    QMessageBox.warning(self, "No Data", "No data was loaded.")
            else:
                print("Data import canceled.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")
            import traceback
            traceback.print_exc()
            

    def add_console_dock(self):
        kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel()
        kernel = kernel_manager.kernel
        kernel.gui = 'qt'  
        kernel.shell.push({'df': self.df})

        kernel_client = kernel_manager.client()
        kernel_client.start_channels()

        console_widget = RichJupyterWidget()
        console_widget.kernel_manager = kernel_manager
        console_widget.kernel_client = kernel_client

        console_widget.exit_requested.connect(self.close)

        console_dock = QDockWidget("Interactive Console", self)
        console_dock.setWidget(console_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, console_dock)

        self.kernel_manager = kernel_manager
        self.kernel_client = kernel_client
        self.kernel = kernel
        self.console_widget = console_widget
        self.console_dock = console_dock
        
    def create_console_menu(self):
        self.console_menu = self.menuBar().addMenu("Console")
        restart_console_action = QAction("Restart Console", self)
        restart_console_action.triggered.connect(self.restart_console)
        self.console_menu.addAction(restart_console_action)
        
    def restart_console(self):

        if hasattr(self, 'console_dock') and self.console_dock:
            self.removeDockWidget(self.console_dock)
            self.console_dock.setWidget(None)
            self.console_dock.deleteLater()
            self.console_dock = None

        if hasattr(self, 'kernel_client') and self.kernel_client:
            self.kernel_client.stop_channels()
            self.kernel_client = None
        if hasattr(self, 'kernel_manager') and self.kernel_manager:
            self.kernel_manager.shutdown_kernel()
            self.kernel_manager = None
        if hasattr(self, 'kernel') and self.kernel:
            self.kernel = None

        if hasattr(self, 'console_widget') and self.console_widget:
            self.console_widget.close()
            self.console_widget.deleteLater()
            self.console_widget = None

        self.add_console_dock()
