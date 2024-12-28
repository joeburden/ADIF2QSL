Program Overview
This program reads ADIF files containing QSO (contact) records and generates custom SVG and PNG files for each record. It maps fields from the ADIF file to placeholders in an SVG template, processes the fields, and saves the modified SVG files. Additionally, it converts these SVG files into PNG files using CairoSVG. The program logs the process and outputs the call signs and email information to CSV files.

Requirements
To run this program, you'll need:

Python: Make sure you have Python installed on your system. Download from python.org.

Python Libraries: You'll need the Pillow library for image processing, xml.etree.ElementTree for parsing SVG content, re for regular expressions, and cairosvg for converting SVG to PNG.

Install the required Python libraries using pip: I recommend installing this into a Python virtual environment to avoid conflicts with other programs.

You can do that by creating a directory where you want to run this:

sh
mkdir adif2qsl 
cd adif2qsl
Paste the files from GitHub repo or use Git to clone the repo per GitHub Guide.

Then create your Python virtual environment with the command:

sh
python3 -m venv nameofyourvirtualenvironment
You must then activate that virtual environment (you will see parentheses in front of the prompt after activating):

sh
venvname\Scripts\Activate
Use the command:

sh
pip install -r requirements.txt
The required libraries will load.

When you finish, you can deactivate the virtual environment:

sh
venvname\Scripts\Deactivate
For a primer on Python Virtual Environments, go to Real Python Guide.

Input Files
ADIF File: Contains QSO records.

SVG Template: An SVG file with placeholders for the fields you want to replace. Variables/Placeholders will be in the form of $VAR_fieldname in input.adif.

Output Files
SVG Files: Modified SVG files for each QSO record.

PNG Files: Converted PNG files for each QSO record, generated using CairoSVG.

CSV Logs:

NOEMAIL.CSV: Call signs with no email.

SUCCESS.CSV: Successfully created SVG and PNG files. Use this file for print and postal mailing in the future.

YESEMAIL.CSV: Call signs with email, including the full path of the corresponding PNG files. Use this file for email merge.

Program Steps
Read ADIF File:

The read_adif function reads the ADIF file and parses its content into a list of dictionaries, each representing a record.

Read SVG Template:

The read_svg function reads the SVG template file.

Map Fields:

The map_fields function replaces placeholders in the SVG template with values from the ADIF records and processes specific fields.

Save SVG Files:

The save_svg function writes the modified SVG content to a file.

Convert SVG to PNG:

The convert_svg_to_png function uses CairoSVG to convert SVG files to PNG.

Log and Save Records:

The program appends the call signs and emails to appropriate CSV log files and saves them in the output directory.

How to Use the Program
Prepare Input Files:

Ensure you have an ADIF file (input.adif) containing your QSO records.

Create an SVG template file (template.svg) with placeholders for the fields you want to replace.

I have provided an example input.adif and template.svg for you to test how it works. Create your own QSL template.

Script Setup:

Place the script in the same directory as your input ADIF file and SVG template.

Run the Script:

Run the script using Python:

sh
python adif2qsl.py
Check Outputs:

Output Directory: The script creates an output_files directory and saves the generated SVG and PNG files there.

CSV Logs: Check the NOEMAIL.CSV for call signs with no email, SUCCESS.CSV for successfully created SVG and PNG files, and YESEMAIL.CSV for call signs with email.

Debugging Logs: Review the debug.txt file for detailed debugging information.