import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                           QSpinBox, QMessageBox, QGroupBox, QFrame, QStyle,
                           QToolButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from rekap_kolase_pdf import create_pdf_collage

class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Title and menu section
        left_section = QHBoxLayout()
        title = QLabel("Kolase PDF Generator")
        title.setStyleSheet("font-weight: bold; color: white; padding: 5px;")
        left_section.addWidget(title)
        
        # Help button
        help_btn = QToolButton()
        help_btn.setText("?")
        help_btn.setToolTip("Cara Penggunaan")
        help_btn.clicked.connect(self.show_help)
        
        # About button
        about_btn = QToolButton()
        about_btn.setText("i")
        about_btn.setToolTip("Tentang Aplikasi")
        about_btn.clicked.connect(self.show_about)
        
        # Style the menu buttons
        menu_style = """
            QToolButton {
                color: #0078D4;
                background: transparent;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
            QToolButton:hover {
                background: white;
                color: #0078D4;
            }
            QToolButton::tooltip {
                background-color: white;
                color: #0078D4;
                border: 1px solid #0078D4;
                padding: 5px;
            }
            QToolTip {
                background-color: white;
                color: #0078D4;
                border: 1px solid #0078D4;
                padding: 5px;
                font-weight: bold;
            }
            
        """
        help_btn.setStyleSheet(menu_style)
        about_btn.setStyleSheet(menu_style)
        
        left_section.addWidget(help_btn)
        left_section.addWidget(about_btn)
        left_section.addStretch()
        
        layout.addLayout(left_section)
        layout.addStretch()

        # Window control buttons
        self.minimize_button = QToolButton()
        self.minimize_button.setIcon(parent.style().standardIcon(QStyle.SP_TitleBarMinButton))
        self.minimize_button.clicked.connect(parent.showMinimized)
        
        self.maximize_button = QToolButton()
        self.maximize_button.setIcon(parent.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.maximize_button.clicked.connect(self.maximize_restore)
        
        self.close_button = QToolButton()
        self.close_button.setIcon(parent.style().standardIcon(QStyle.SP_TitleBarCloseButton))
        self.close_button.clicked.connect(parent.close)

        # Style the buttons
        button_style = """
            QToolButton {
                background: transparent;
                padding: 5px;
                border: none;
            }
            QToolButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            QToolButton:pressed {
                background: rgba(255, 255, 255, 0.1);
            }
        """
        self.minimize_button.setStyleSheet(button_style)
        self.maximize_button.setStyleSheet(button_style)
        self.close_button.setStyleSheet(button_style)

        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #0078D4;")

    def maximize_restore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.maximize_button.setIcon(self.parent.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        else:
            self.parent.showMaximized()
            self.maximize_button.setIcon(self.parent.style().standardIcon(QStyle.SP_TitleBarNormalButton))

    def show_help(self):
        QMessageBox.information(self.parent, "Cara Penggunaan",
            "1. Klik 'Pilih Folder Input' untuk memilih folder berisi gambar\n"
            "2. Klik 'Pilih File Output' untuk menentukan file PDF output\n"
            "3. Atur jumlah kolom dan baris sesuai kebutuhan\n"
            "4. Atur margin dan jarak antar gambar jika perlu\n"
            "5. Klik 'Generate PDF' untuk membuat kolase PDF"
        )

    def show_about(self):
        QMessageBox.about(self.parent, "Tentang Aplikasi",
            "Kolase PDF Generator\n\n"
            "Dibuat oleh COREX\n"
            "by Nur Dwi Priyambodo\n\n"
            "© 2024 All rights reserved"
        )

class KolasePDFGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kolase PDF Generator")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.input_folder = ""
        self.output_file = ""
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add title bar
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # File Selection Group
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()
        file_group.setLayout(file_layout)

        # Input folder selection
        input_layout = QHBoxLayout()
        self.input_label = QLabel("Input folder belum dipilih")
        input_btn = QPushButton("Pilih Folder Input")
        input_btn.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        input_btn.clicked.connect(self.choose_input_folder)
        input_layout.addWidget(self.input_label, stretch=1)
        input_layout.addWidget(input_btn)
        file_layout.addLayout(input_layout)

        # Output file selection
        output_layout = QHBoxLayout()
        self.output_label = QLabel("Output file belum dipilih")
        output_btn = QPushButton("Pilih File Output")
        output_btn.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        output_btn.clicked.connect(self.choose_output_file)
        output_layout.addWidget(self.output_label, stretch=1)
        output_layout.addWidget(output_btn)
        file_layout.addLayout(output_layout)

        content_layout.addWidget(file_group)

        # Layout Settings Group
        layout_group = QGroupBox("Layout Settings")
        settings_layout = QVBoxLayout()
        layout_group.setLayout(settings_layout)

        # Grid settings
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(10)
        
        col_layout = QHBoxLayout()
        col_layout.addWidget(QLabel("Kolom:"))
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, 10)
        self.cols_spin.setValue(2)
        col_layout.addWidget(self.cols_spin)
        grid_layout.addLayout(col_layout)

        row_layout = QHBoxLayout()
        row_layout.addWidget(QLabel("Baris:"))
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, 10)
        self.rows_spin.setValue(3)
        row_layout.addWidget(self.rows_spin)
        grid_layout.addLayout(row_layout)
        
        grid_layout.addStretch()
        settings_layout.addLayout(grid_layout)

        # Spacing settings
        spacing_layout = QHBoxLayout()
        spacing_layout.setSpacing(10)
        
        margin_layout = QHBoxLayout()
        margin_layout.addWidget(QLabel("Margin (mm):"))
        self.margin_spin = QSpinBox()
        self.margin_spin.setRange(0, 50)
        self.margin_spin.setValue(10)
        margin_layout.addWidget(self.margin_spin)
        spacing_layout.addLayout(margin_layout)

        gap_layout = QHBoxLayout()
        gap_layout.addWidget(QLabel("Gap (mm):"))
        self.gap_spin = QSpinBox()
        self.gap_spin.setRange(0, 50)
        self.gap_spin.setValue(5)
        gap_layout.addWidget(self.gap_spin)
        spacing_layout.addLayout(gap_layout)
        
        spacing_layout.addStretch()
        settings_layout.addLayout(spacing_layout)

        content_layout.addWidget(layout_group)

        # Generate button
        generate_btn = QPushButton("Generate PDF")
        generate_btn.setMinimumHeight(40)
        generate_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        generate_btn.clicked.connect(self.generate_pdf)
        content_layout.addWidget(generate_btn)

        main_layout.addWidget(content_widget)
        self.setCentralWidget(main_widget)

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,
                 (screen.height() - size.height()) // 2)

    def choose_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Pilih Folder Input")
        if folder:
            self.input_folder = folder
            self.input_label.setText(f"Input: {os.path.basename(folder)}")

    def choose_output_file(self):
        file, _ = QFileDialog.getSaveFileName(self, "Pilih File Output",
                                            filter="PDF files (*.pdf)")
        if file:
            if not file.lower().endswith('.pdf'):
                file += '.pdf'
            self.output_file = file
            self.output_label.setText(f"Output: {os.path.basename(file)}")

    def generate_pdf(self):
        if not self.input_folder or not self.output_file:
            QMessageBox.warning(self, "Error", 
                              "Pilih folder input dan file output terlebih dahulu!")
            return

        try:
            create_pdf_collage(
                self.input_folder,
                self.output_file,
                cols=self.cols_spin.value(),
                rows=self.rows_spin.value(),
                margin=self.margin_spin.value(),
                gap=self.gap_spin.value()
            )
            QMessageBox.information(self, "Sukses", 
                                  f"PDF berhasil dibuat: {self.output_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() < self.title_bar.height():
            self.drag_start_position = event.globalPos()
            self.window_position = self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_start_position'):
            if event.buttons() & Qt.LeftButton:
                delta = event.globalPos() - self.drag_start_position
                self.move(self.window_position + delta)
                event.accept()

    def mouseReleaseEvent(self, event):
        if hasattr(self, 'drag_start_position'):
            delattr(self, 'drag_start_position')
            delattr(self, 'window_position')
            event.accept()

def main():
    app = QApplication(sys.argv)
    window = KolasePDFGui()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()