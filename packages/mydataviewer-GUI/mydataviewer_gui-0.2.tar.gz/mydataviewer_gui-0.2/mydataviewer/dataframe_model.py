
from PyQt5.QtCore import QAbstractTableModel, Qt
import pandas as pd

class DataFrameModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), page_size=100):
        super().__init__()
        self._df = df  
        self.page_size = page_size
        self.current_page = 0
        self.sort_columns = []  
        self.sort_orders = []   
        self.sorted_df_cache = None  

    def rowCount(self, parent=None):
        start_row = self.current_page * self.page_size
        end_row = min(start_row + self.page_size, len(self._df))
        return end_row - start_row

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            start_row = self.current_page * self.page_size
            sorted_df = self.get_sorted_df()
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = sorted_df.iloc[start_row + index.row(), index.column()]
                if pd.isnull(value):
                    return ""
                return str(value)
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            try:
                start_row = self.current_page * self.page_size
                row = start_row + index.row()
                col = index.column()
                col_name = self._df.columns[col]
                idx = self._df.index[row]


                self._df.at[idx, col_name] = value

                self.dataChanged.emit(index, index, (Qt.DisplayRole,))
                return True
            except Exception as e:
                print(f"Error: {e}")
                return False
        return False

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._df.columns[section]
            if orientation == Qt.Vertical:
                start_row = self.current_page * self.page_size
                return str(self._df.index[start_row + section])
        return None

    def get_sorted_df(self):
        if self.sorted_df_cache is not None:
            return self.sorted_df_cache

        if self.sort_columns:
            ascending_list = [order == Qt.AscendingOrder for order in self.sort_orders]
            self.sorted_df_cache = self._df.sort_values(by=self.sort_columns, ascending=ascending_list)
        else:
            self.sorted_df_cache = self._df

        return self.sorted_df_cache

    def invalidate_cache(self):
        self.sorted_df_cache = None
        self.layoutChanged.emit()

    def sort(self, column, order):
        col_name = self._df.columns[column]
        if col_name in self.sort_columns:
            index = self.sort_columns.index(col_name)
            self.sort_orders[index] = order
        else:
            self.sort_columns.append(col_name)
            self.sort_orders.append(order)


        self.invalidate_cache()

    def nextPage(self):
        if (self.current_page + 1) * self.page_size < len(self._df):
            self.current_page += 1
            self.layoutChanged.emit()

    def previousPage(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.layoutChanged.emit()

    def goToFirstPage(self):
        self.current_page = 0
        self.layoutChanged.emit()

    def goToLastPage(self):
        self.current_page = len(self._df) // self.page_size
        self.layoutChanged.emit()
