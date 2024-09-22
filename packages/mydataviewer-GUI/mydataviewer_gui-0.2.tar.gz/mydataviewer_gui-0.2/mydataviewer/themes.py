

light_theme = """
QWidget {
    background-color: #ffffff;
    color: #000000;
}

RichJupyterWidget {
    background-color: #ffffff;
    color: #000000;
}

QHeaderView::section {
    background-color: lightgray;
    color: black;
    font-weight: bold;
    border: 1px solid #6c6c6c;
    padding: 4px;
}

QTableWidget::item {
    padding: 5px;
    background-color: #f0f0f0;
}

QTableView {
    gridline-color: #d0d0d0;
}
"""

dark_theme = """
QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
}

RichJupyterWidget {
    background-color: #2b2b2b;
    color: #ffffff;
}

QHeaderView::section {
    background-color: #3c3c3c;
    color: white;
    font-weight: bold;
    border: 1px solid #5c5c5c;
    padding: 4px;
}

QTableWidget::item {
    padding: 5px;
    background-color: #3c3c3c;
    color: white;
}

QTableView {
    gridline-color: #5c5c5c;
}
"""

solarized_dark_theme = """
QWidget {
    background-color: #002b36;  /* Solarized base03 */
    color: #839496;  /* Solarized base0 */
}

RichJupyterWidget {
    background-color: #002b36;  /* Solarized base03 */
    color: #839496;  /* Solarized base0 */
}

QHeaderView::section {
    background-color: #073642;  /* Solarized base02 */
    color: #93a1a1;  /* Solarized base1 */
    font-weight: bold;
    border: 1px solid #586e75;  /* Solarized base01 */
    padding: 4px;
}

QTableWidget::item {
    padding: 5px;
    background-color: #073642;  /* Solarized base02 */
    color: #839496;  /* Solarized base0 */
}

QTableView {
    gridline-color: #586e75;  /* Solarized base01 */
}

QLineEdit, QComboBox, QSpinBox, QTextEdit {
    background-color: #073642;  /* Solarized base02 */
    color: #839496;  /* Solarized base0 */
    border: 1px solid #586e75;  /* Solarized base01 */
    padding: 2px;
}

QPushButton {
    background-color: #586e75;  /* Solarized base01 */
    color: #fdf6e3;  /* Solarized base3 */
    border: 1px solid #073642;  /* Solarized base02 */
    padding: 5px;
}

QPushButton:hover {
    background-color: #657b83;  /* Solarized base00 */
    border: 1px solid #586e75;  /* Solarized base01 */
}

QMenuBar {
    background-color: #002b36;  /* Solarized base03 */
    color: #839496;  /* Solarized base0 */
}

QMenu {
    background-color: #002b36;  /* Solarized base03 */
    color: #839496;  /* Solarized base0 */
}

QMenu::item:selected {
    background-color: #073642;  /* Solarized base02 */
}

QScrollBar:vertical, QScrollBar:horizontal {
    background: #073642;  /* Solarized base02 */
}

QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background: #586e75;  /* Solarized base01 */
}
"""

solarized_light_theme = """
QWidget {
    background-color: #fdf6e3;  /* Solarized base3 */
    color: #657b83;  /* Solarized base00 */
}

RichJupyterWidget {
    background-color: #fdf6e3;  /* Solarized base3 */
    color: #657b83;  /* Solarized base00 */
}

QHeaderView::section {
    background-color: #eee8d5;  /* Solarized base2 */
    color: #586e75;  /* Solarized base01 */
    font-weight: bold;
    border: 1px solid #93a1a1;  /* Solarized base1 */
    padding: 4px;
}

QTableWidget::item {
    padding: 5px;
    background-color: #eee8d5;  /* Solarized base2 */
    color: #657b83;  /* Solarized base00 */
}

QTableView {
    gridline-color: #93a1a1;  /* Solarized base1 */
}

QLineEdit, QComboBox, QSpinBox, QTextEdit {
    background-color: #eee8d5;  /* Solarized base2 */
    color: #657b83;  /* Solarized base00 */
    border: 1px solid #93a1a1;  /* Solarized base1 */
    padding: 2px;
}

QPushButton {
    background-color: #93a1a1;  /* Solarized base1 */
    color: #002b36;  /* Solarized base03 */
    border: 1px solid #eee8d5;  /* Solarized base2 */
    padding: 5px;
}

QPushButton:hover {
    background-color: #839496;  /* Solarized base0 */
    border: 1px solid #93a1a1;  /* Solarized base1 */
}
"""
monokai_theme = """
QWidget {
    background-color: #272822;
    color: #f8f8f2;
}

RichJupyterWidget {
    background-color: #272822;
    color: #f8f8f2;
}

QHeaderView::section {
    background-color: #49483e;
    color: #f8f8f2;
    font-weight: bold;
    border: 1px solid #75715e;
    padding: 4px;
}

QTableWidget::item {
    padding: 5px;
    background-color: #3e3d32;
    color: #f8f8f2;
}

QTableView {
    gridline-color: #75715e;
}

QLineEdit, QComboBox, QSpinBox, QTextEdit {
    background-color: #49483e;
    color: #f8f8f2;
    border: 1px solid #75715e;
    padding: 2px;
}

QPushButton {
    background-color: #75715e;
    color: #f8f8f2;
    border: 1px solid #49483e;
    padding: 5px;
}

QPushButton:hover {
    background-color: #66d9ef;  /* Monokai blue */
    border: 1px solid #49483e;
}

QMenuBar {
    background-color: #272822;
    color: #f8f8f2;
}

QMenu {
    background-color: #272822;
    color: #f8f8f2;
}

QMenu::item:selected {
    background-color: #49483e;
}
"""
shades_of_purple_theme = """
QWidget {
    background-color: #2d2b55;
    color: #f8f8f2;
}

RichJupyterWidget {
    background-color: #2d2b55;
    color: #f8f8f2;
}

QHeaderView::section {
    background-color: #393a83;
    color: #ff9d00;
    font-weight: bold;
    border: 1px solid #8179f9;
    padding: 4px;
}

QTableWidget::item {
    padding: 5px;
    background-color: #372f50;
    color: #f8f8f2;
}

QTableView {
    gridline-color: #8179f9;
}

QLineEdit, QComboBox, QSpinBox, QTextEdit {
    background-color: #393a83;
    color: #f8f8f2;
    border: 1px solid #8179f9;
    padding: 2px;
}

QPushButton {
    background-color: #8179f9;
    color: #f8f8f2;
    border: 1px solid #393a83;
    padding: 5px;
}

QPushButton:hover {
    background-color: #ff9d00;  /* Accent color */
    border: 1px solid #393a83;
}

QMenuBar {
    background-color: #2d2b55;
    color: #f8f8f2;
}

QMenu {
    background-color: #2d2b55;
    color: #f8f8f2;
}

QMenu::item:selected {
    background-color: #393a83;
}
"""
vue_theme = """
QWidget {
    background-color: #002b36;  /* Background */
    color: #e6e6e6;  /* Foreground */
}

RichJupyterWidget {
    background-color: #002b36;
    color: #e6e6e6;
}

QHeaderView::section {
    background-color: #46494d87;  /* Selection background */
    color: #000000;  /* Green/Active Border */
    font-weight: bold;
    border: 1px solid #19f9d8;  /* Green */
    padding: 4px;
}

QTableWidget::item {
    padding: 5px;
    background-color: #46494d87;  /* Selection background */
    color: #e6e6e6;  /* Foreground */
}

QTableView {
    gridline-color: #19f9d8;  /* Active Border */
}

QLineEdit, QComboBox, QSpinBox, QTextEdit {
    background-color: #002b36;  /* Background */
    color: #e6e6e6;  /* Foreground */
    border: 1px solid #19f9d8;  /* Green */
    padding: 2px;
}

QPushButton {
    background-color: #19f9d8;  /* Green */
    color: #002b36;  /* Background (contrast) */
    border: 1px solid #09cbdd;  /* Cyan */
    padding: 5px;
}

QPushButton:hover {
    background-color: #ff5622de;  /* Orange (hover effect) */
    border: 1px solid #002b36;  /* Background */
}

QMenuBar {
    background-color: #002b36;  /* Background */
    color: #e6e6e6;  /* Foreground */
}

QMenu {
    background-color: #002b36;  /* Background */
    color: #e6e6e6;  /* Foreground */
}

QMenu::item:selected {
    background-color: #46494d87;  /* Selection background */
}

QScrollBar:vertical {
    background-color: #002b36;
    border: 1px solid #19f9d8;
}

QScrollBar::handle:vertical {
    background-color: #09cbdd;  /* Cyan */
}

QToolTip {
    background-color: #ffcc95;  /* Yellow */
    color: #002b36;  /* Background */
    border: 1px solid #19f9d8;  /* Green */
}

QStatusBar {
    background-color: #002b36;
    color: #8a8787;  /* Comment */
}
"""
