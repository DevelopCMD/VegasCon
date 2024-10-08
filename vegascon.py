import sys
import os
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, 
    QFileDialog, QLineEdit, QComboBox, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from qt_material import apply_stylesheet

class VegConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon("Res/icon.png"))
        self.setWindowTitle('VegasCon 1.0')
        self.setGeometry(300, 300, 400, 250)

        layout = QVBoxLayout()

        # File selection components
        self.file_label = QLabel('Select .veg or .vf file:')
        layout.addWidget(self.file_label)

        self.file_input = QLineEdit(self)
        self.file_input.setReadOnly(True)
        layout.addWidget(self.file_input)

        self.file_button = QPushButton('Browse', self)
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        # Format selection components
        self.format_label = QLabel('Select format to convert to:')
        layout.addWidget(self.format_label)

        self.format_combo = QComboBox(self)
        self.format_combo.addItem("VEGAS Pro (.veg)")
        self.format_combo.addItem("Movie Studio (.vf)")
        self.format_combo.currentIndexChanged.connect(self.update_version_combo)  # Update version options based on format
        layout.addWidget(self.format_combo)

        # Version selection components
        self.version_label = QLabel('Select target version:')
        layout.addWidget(self.version_label)

        self.version_combo = QComboBox(self)
        self.add_version_options_with_icons()  # Initialize with VEGAS Pro versions
        layout.addWidget(self.version_combo)

        # Convert button
        self.convert_button = QPushButton('Convert', self)
        self.convert_button.clicked.connect(self.start_conversion)
        layout.addWidget(self.convert_button)

        # Set layout
        self.setLayout(layout)

    def add_version_options_with_icons(self):
        """Add version options with icons and program names based on the selected format."""
        # Clear previous items
        self.version_combo.clear()

        format_selected = self.format_combo.currentText()
        
        if "VEGAS Pro" in format_selected:
            versions = range(9, 22)  # VEGAS Pro supports 9 to 21
            for version in versions:
                if version < 14:
                    program_name = f"Vegas Pro {version}"
                else:
                    program_name = f"VEGAS Pro {version}"
                icon_path = f'Res/vegas/{version}.png'  # Use VEGAS Pro icons
                icon = QIcon(icon_path)
                self.version_combo.addItem(icon, program_name)

        elif "Movie Studio" in format_selected:
            versions = range(9, 18)  # Movie Studio supports 9 to 17
            for version in versions:
                if version < 14:
                    program_name = f"Movie Studio {version}"
                else:
                    program_name = f"VEGAS Movie Studio {version}"
                icon_path = f'Res/movie/{version}.png'  # Use Movie Studio icons
                icon = QIcon(icon_path)
                self.version_combo.addItem(icon, program_name)

    def select_file(self):
        file_filter = "VEG Files (*.veg);;VF Files (*.vf)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Select .veg or .vf file", "", file_filter)
        if file_path:
            self.file_input.setText(file_path)

    def update_version_combo(self):
        """Update the version combo box options when the format is changed."""
        self.add_version_options_with_icons()

    def start_conversion(self):
        input_file = self.file_input.text()
        target_version = self.version_combo.currentText()
        format_selected = self.format_combo.currentText()
        version_number = self.extract_version_number(target_version)

        if not input_file:
            QMessageBox.critical(self, "Error", "Please select a .veg or .vf file.")
            return
        if not target_version:
            QMessageBox.critical(self, "Error", "Please select a target version.")
            return

        # Extract only the version number from the selected version
        version_number = self.extract_version_number(target_version)

        # Determine output format and output filename based on the selected format
        if "VEGAS Pro" in format_selected:
            output_extension = "veg"
        else:
            output_extension = "vf"

        # Create output file name based on input file name
        base_name = os.path.splitext(input_file)[0]  # Remove extension
        output_file = f"{base_name}_V{version_number}{output_extension}"  # New output file name

        # Command to run the external tool using os.system
        command = f"msvpvf.exe --input \"{input_file}\" --version {version_number} --type {output_extension}"

        # Running the command using os.system
        result = os.system(command)

        if result == 0:
            print("Successfully!")
            print("Target version is", target_version)
            print("Selected format is", format_selected)
            QMessageBox.information(self, "Success", f"File converted successfully.")
        else:
            QMessageBox.critical(self, "Error", "Conversion failed.")

    def extract_version_number(self, version_string):
        """Extracts the numeric version from a string like 'MAGIX Vegas 17'."""
        match = re.search(r'(\d+)', version_string)
        if match:
            return match.group(1)  # Returns only the version number (e.g., '17')
        return "0"  # Fallback to 0 if no version number is found

def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')
    converter = VegConverterApp()
    converter.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
