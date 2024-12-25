### Program Overview
This program reads ADIF files containing QSO (contact) records and generates custom SVG and PNG files for each record. It maps fields from the ADIF file to placeholders in an SVG template, processes the fields, and saves the modified SVG files. Additionally, it converts these SVG files into PNG files using Inkscape. The program logs the process and outputs the call signs and email information to CSV files.

### Requirements
To run this program, you'll need:
1. **Python**: Make sure you have Python installed on your system. Download from [python.org](https://www.python.org).
2. **Inkscape**: Used to convert SVG files to PNG. Download from the [official website](https://inkscape.org).  Until I get the PNG conversion worked out with the python libraries, I am going to use inkscape commands from the command line to generate the PNG.  You will want to add your inkscape directory to your path
3. **Python Libraries**: You'll need the `Pillow` library for image processing, `xml.etree.ElementTree` for parsing SVG content, `re` for regular expressions, and `subprocess` for running external commands.

Install the required Python libraries using pip:
I recommend installing this into a python virtual environment to avoid conflicts with other programs
You can do that by creating a directory where you want to run this 

For example:
mkdir adif2qsl 
cd into that directory
paste the files from GitHub repo

Then create your Python virtual environment wih the command:
Python3 -m venv nameofyourvirtualenvironment


You must then activate that virtual environment (you will see parenthesis in front of prompt after activating)
Activate your virtual env with <venvname>\Scripts\Activate

Use the command
pip install -r requirements. txt

The required libraries will load.

When you finish you can type: venvname\Scripts\Deactivate

For a primer on Python Virtual Environments go to https://realpython.com/python-virtual-environments-a-primer/

### Input Files
1. **ADIF File**: Contains QSO records.
2. **SVG Template**: An SVG file with placeholders for the fields you want to replace.
   Variables/Placeholders will be in the form of $VAR_fieldname in input.adif

### Output Files
1. **SVG Files**: Modified SVG files for each QSO record.
2. **PNG Files**: Converted PNG files for each QSO record, generated using Inkscape.
3. **CSV Logs**:
   - `NOEMAIL.CSV`: Call signs with no email.
   - `SUCCESS.CSV`: Successfully created SVG and PNG files.
   - `YESEMAIL.CSV`: Call signs with email, including the full path of the corresponding PNG files.

### Program Steps

1. **Read ADIF File**: 
   - The `read_adif` function reads the ADIF file and parses its content into a list of dictionaries, each representing a record.
2. **Read SVG Template**: 
   - The `read_svg` function reads the SVG template file.
3. **Map Fields**: 
   - The `map_fields` function replaces placeholders in the SVG template with values from the ADIF records and processes specific fields.
4. **Save SVG Files**: 
   - The `save_svg` function writes the modified SVG content to a file.
5. **Convert SVG to PNG**: 
   - The `convert_svg_to_png` function uses Inkscape's command line interface to convert SVG files to PNG.
6. **Log and Save Records**: 
   - The program appends the call signs and emails to appropriate CSV log files and saves them in the output directory.

### How to Use the Program

1. **Prepare Input Files**:
   - Ensure you have an ADIF file (`input.adif`) containing your QSO records.
   - Create an SVG template file (`template.svg`) with placeholders for the fields you want to replace.
   - I have provided an example input.adif and template.svg for you to test how it works.  Make your own QSL template.

2. **Script Setup**:
   - Place the script in the same directory as your input ADIF file and SVG template.

3. **Run the Script**:
   - Run the script using Python:
   ```sh
   python your_script_name.py
   ```

4. **Check Outputs**:
   - **Output Directory**: The script creates an `output_files` directory and saves the generated SVG and PNG files there.
   - **CSV Logs**: Check the `NOEMAIL.CSV` for call signs with no email, `SUCCESS.CSV` for successfully created SVG and PNG files, and `YESEMAIL.CSV` for call signs with email.
   - **Debugging Logs**: Review the `debug.txt` file for detailed debugging information.