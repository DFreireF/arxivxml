# arxivxml
Python script that creates the authors.xml file necessary for submission to arXiV for big collaborations.
For more information please check [https://github.com/inspirehep/author.xml](https://github.com/inspirehep/author.xml)

`arxivxml` is a Python tool designed to generate XML files from `.ods` (OpenDocument Spreadsheet) files containing author lists. It is particularly useful for academic and research purposes where author and affiliation data need to be converted into a standardized XML format.

## Features

- Reads author list from `.ods` file.
- Sorts authors based on a specified order.
- Generates XML files adhering to a specified schema.
- Validates the generated XML against a DTD file.
- Configurable publication reference through a `.toml` file.

## Installation

Before running `arxivxml`, ensure that Python is installed on your system along with the required libraries: `pandas` and `lxml`. You can install these libraries using pip:

```bash
pip install pandas lxml
```

## Usage

To use `arxivxml`, you need to provide:

+ Path to the .ods file containing the author list.
+ Path to the .toml configuration file for the publication reference.
+ Path to the .dtd file for XML validation.

Run the script from the command line as follows:

```bash
python main.py --ods path_to_ods_file.ods --toml path_to_toml_file.toml --dtd path_to_dtd_file.dtd
```

The script will generate an authors.xml file in the current directory and validate it against the provided DTD file.