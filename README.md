
```markdown
### Program Overview
This program reads ADIF files containing QSO (contact) records and generates custom SVG and PNG files for each record. It maps fields from the ADIF file to placeholders in an SVG template, processes the fields, and saves the modified SVG files. Additionally, it converts these SVG files into PNG files using CairoSVG. The program logs the process and outputs the call signs and email information to CSV files.

### Requirements
To run this program, you'll need:
1. **Python**: Make sure you have Python installed on your system. Download from [python.org](https://www.python.org).
2. **Python Libraries**: You'll need the `CairoSVG` library for SVG to PNG conversion, the `Pillow` library for image processing, `xml.etree.ElementTree` for parsing SVG content, and `re` for regular expressions.

Install the required Python libraries using pip:
I recommend installing this into a Python virtual environment to avoid conflicts with other programs. You can do that by creating a directory where you want to run this.

For example:
```sh
mkdir adif2qsl 
cd adif2qsl
```
Then, paste the files from the GitHub repo or use Git to clone the repo per [GitHub Documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

Next, create your Python virtual environment with the command:
```sh
python3 -m venv nameofyourvirtualenvironment
```

Activate your virtual environment (you will see parentheses in front of the prompt after activating):
```sh
venvname\Scripts\Activate
```

Use the command:
```sh
pip install -r requirements.txt
```
** Note **
For your required libraries to load from the requirements file you must be in the same directory as the requirements.txt file.  

The required libraries will load.

When you finish, you can type:
```sh
venvname\Scripts\Deactivate
```

For a primer on Python Virtual Environments, go to [Real Python Virtual Environments Primer](https://realpython.com/python-virtual-environments-a-primer/).

### Input Files
1. **ADIF File**: Contains QSO records.
2. **SVG Template**: An SVG file with placeholders for the fields you want to replace. Variables/Placeholders will be in the form of `$VAR_fieldname` in `input.adif`.

### Output Files
1. **SVG Files**: Modified SVG files for each QSO record.
2. **PNG Files**: Converted PNG files for each QSO record, generated using CairoSVG.
3. **CSV Logs**:
   - `NOEMAIL.CSV`: Call signs with no email.
   - `SUCCESS.CSV`: Successfully created SVG and PNG files. Use this file for print and postal mailing in the future.
   - `YESEMAIL.CSV`: Call signs with email, including the full path of the corresponding PNG files. Use this file for email merge.

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
   - The `convert_svg_to_png` function uses CairoSVG to convert SVG files to PNG.
6. **Log and Save Records**: 
   - The program appends the call signs and emails to appropriate CSV log files and saves them in the output directory.

### How to Use the Program

1. **Prepare Input Files**:
   - Ensure you have an ADIF file (`input.adif`) containing your QSO records.
   - Create an SVG template file (`template.svg`) with placeholders for the fields you want to replace.
   - I have provided an example `input.adif` and `template.svg` for you to test how it works. Make your own QSL template.

2. **Script Setup**:
   - Place the script in the same directory as your input ADIF file and SVG template.

3. **Run the Script**:
   - Run the script using Python:
   ```sh
   python adif2qsl.py
   ```

4. **Check Outputs**:
   - **Output Directory**: The script creates an `output_files` directory and saves the generated SVG and PNG files there.
   - **CSV Logs**: Check the `NOEMAIL.CSV` for call signs with no email, `SUCCESS.CSV` for successfully created SVG and PNG files, and `YESEMAIL.CSV` for call signs with email.
   - **Debugging Logs**: Review the `debug.txt` file for detailed debugging information.
```
** If your outputted PNG files do not look correct **
You might have embedded files in your svg that should be converted to PATH so they are native to SVG format.
Try one of the example files provided and if that works it is more than likely a problem with your SVG file having issues.

Other issues that have poppped up is that this code does not handle netlogger adif files very well because fields are not correct in the netlogger ADIF files.
This program works great with Log4OM ADIF files.