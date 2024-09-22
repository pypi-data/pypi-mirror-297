
from .observable_dataframe import ObservableDataFrame
from .data_viewer import DataViewer
import pandas as pd
def view_dataframe(df=None, block=True):

    import sys
    from PyQt5.QtWidgets import QApplication

    if df is not None and not isinstance(df, ObservableDataFrame):
        df = ObservableDataFrame(df)
    elif df is None:
        df = ObservableDataFrame(pd.DataFrame())  

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    viewer = DataViewer(df)
    viewer.show()

    if block:
        sys.exit(app.exec_())
    else:
        app.exec_()
def main():
    """Main function for CLI usage."""
    view_dataframe()

if __name__ == "__main__":
    main()