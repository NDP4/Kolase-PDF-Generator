# Kolase PDF Generator

A modern GUI application to create PDF collages from multiple images with configurable layouts.

## Features

- Modern and intuitive graphical user interface
- Drag-and-drop window movement
- Customizable grid layout (rows and columns)
- Adjustable margins and gaps between images
- Maintains image aspect ratios
- Supports JPG, JPEG, and PNG images
- Generates clean PDF output
- Cross-platform compatibility (Windows, Linux, macOS)

## Requirements

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/NDP4/Kolase-PDF-Generator.git
cd kolase-pdf-generator
```

2. Install required dependencies:

```bash
pip install PyQt5 fpdf pillow
```

## Usage

1. Start the application:

```bash
python rekap_kolase_gui.py
```

2. Using the application:
   - Click "Pilih Folder Input" to select a folder containing your images
   - Click "Pilih File Output" to choose where to save the PDF
   - Adjust layout settings:
     - Columns (default: 2)
     - Rows (default: 3)
     - Margin in mm (default: 10)
     - Gap between images in mm (default: 5)
   - Click "Generate PDF" to create the collage

## Configuration Options

### Grid Layout

- Columns: 1-10
- Rows: 1-10
- Default: 2x3 grid

### Spacing

- Margin: 0-50mm (border around the page)
- Gap: 0-50mm (space between images)

## File Support

Supported image formats:

- JPG/JPEG
- PNG

## Features in Detail

### Window Controls

- Minimalize button
- Maximize/Restore button
- Close button
- Draggable window (click and drag title bar)

### Help & Information

- Help button (?) - Shows usage instructions
- About button (i) - Shows application credits

## Command Line Interface

The application also supports command-line usage:

```bash
python rekap_kolase_pdf.py --input <input_folder> --output <output_pdf> [options]

Options:
  --cols N     Number of columns (default: 2)
  --rows N     Number of rows (default: 3)
  --margin N   Page margin in mm (default: 10)
  --gap N      Gap between images in mm (default: 5)
```

## Error Handling

The application includes error handling for:

- Missing input folder
- No images in input folder
- Invalid output location
- Image processing errors

## Credits

Created by COREX
by Nur Dwi Priyambodo
© 2025 All rights reserved

## License

All rights reserved. For use permissions, please contact the author.
