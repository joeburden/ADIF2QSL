import os
import csv
import logging
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
import re  # Import the re module
import subprocess

# Configure logging
logging.basicConfig(filename=os.path.join('output_files', 'debug.txt'),
                    filemode='w',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def read_adif(adif_file):
    with open(adif_file, 'r') as f:
        adif_content = f.read()
    
    if '<EOH>' in adif_content:
        records_content = adif_content.split('<EOH>')[1]
    else:
        records_content = adif_content  # If <EOH> is missing, assume everything is records
    
    records = records_content.split('<EOR>')
    
    def parse_adif_record(record):
        fields = {}
        for part in record.split('<'):
            if ':' in part and '>' in part:
                field, rest = part.split('>', 1)
                try:
                    name, length = field.split(':')
                    fields[name] = rest[:int(length)].strip()
                except ValueError:
                    logging.warning(f"Skipping invalid field: {field}")
                    continue
        return fields
    
    return [parse_adif_record(record) for record in records if record.strip()]

def read_svg(svg_file):
    with open(svg_file, 'r') as f:
        svg_content = f.read()
    return svg_content

def map_fields(adif_data, svg_content):
    for field, value in adif_data.items():
        placeholder = f'$VAR_{field}'
        if placeholder in svg_content:
            if value:
                if field in ['TIME_ON', 'TIME_OFF']:
                    # Insert colons between every two digits
                    value = ':'.join([value[i:i+2] for i in range(0, len(value), 2)])
                elif field == 'QSO_DATE':
                    # Format the date as YYYY/MM/DD
                    value = f"{value[:4]}/{value[4:6]}/{value[6:]}"
                svg_content = svg_content.replace(placeholder, value)
            else:
                # Remove the placeholder if there is no data to replace it
                svg_content = svg_content.replace(placeholder, '')
    
    # Remove any remaining placeholders that were not replaced
    svg_content = re.sub(r'\$VAR_[A-Z_]+', '', svg_content)
    
    return svg_content

def save_svg(svg_content, output_file):
    with open(output_file, 'w') as f:
        f.write(svg_content)

def convert_svg_to_png(svg_file, png_file):
    # Using Inkscape's command line interface to convert SVG to PNG
    command = f'inkscape {svg_file} --export-filename={png_file}'
    try:
        subprocess.run(command, shell=True, check=True)
        logging.info(f'Successfully converted {svg_file} to {png_file} using Inkscape.')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error converting {svg_file} to {png_file}: {e}')

def append_to_csv(file_path, call_sign, email=None, png_path=None):
    with open(file_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        if email and png_path:
            csv_writer.writerow([call_sign, email, png_path])
        elif email:
            csv_writer.writerow([call_sign, email])
        else:
            csv_writer.writerow([call_sign])

def write_headers(csv_file, headers):
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)

# Define file paths
adif_file = 'input.adif'  # Input ADIF file path
svg_file = 'template.svg'  # Template SVG file path
output_dir = 'output_files'  # Output directory for SVG and PNG files
csv_file_no_email = os.path.join(output_dir, 'NOEMAIL.CSV')  # CSV file path for call signs with no email
csv_file_success = os.path.join(output_dir, 'SUCCESS.CSV')  # CSV file path for successfully created SVG and PNG files
csv_file_yes_email = os.path.join(output_dir, 'YESEMAIL.CSV')  # CSV file path for call signs with email
svg_backup_file = os.path.join(output_dir, 'template_backup.svg')  # Backup SVG file path

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Write headers to CSV files
write_headers(csv_file_no_email, ["CALL_SIGN"])
write_headers(csv_file_success, ["CALL_SIGN", "EMAIL"])
write_headers(csv_file_yes_email, ["CALL_SIGN", "EMAIL", "PNG_PATH"])

# Create a backup of the original SVG file
if not os.path.exists(svg_backup_file):
    with open(svg_file, 'r') as original, open(svg_backup_file, 'w') as backup:
        backup.write(original.read())
        logging.info(f'Backup of SVG template created at {svg_backup_file}')

# Read ADIF records
adif_records = read_adif(adif_file)
svg_template = read_svg(svg_file)

# Process each record and save as SVG and PNG files
for record in adif_records:
    adif_data = record  # Directly use the parsed record
    call_sign = adif_data.get('CALL', 'unknown')
    email = adif_data.get('EMAIL')

    if email:
        output_svg_file = os.path.join(output_dir, f'{call_sign}.svg')
        output_png_file = os.path.join(output_dir, f'{call_sign}.png')
        full_png_path = os.path.abspath(output_png_file)
    
        # Map ADIF fields to SVG placeholders
        mapped_svg_content = map_fields(adif_data, svg_template)
    
        # Save the modified SVG content to a new file
        save_svg(mapped_svg_content, output_svg_file)
        logging.info(f'Successfully mapped fields and saved to {output_svg_file}')
    
        # Debugging: Log the mapped SVG content
        logging.debug(f"Mapped SVG Content: {mapped_svg_content}")
    
        # Convert SVG to PNG using Inkscape
        convert_svg_to_png(output_svg_file, output_png_file)
    
        # Append the call sign, email, and PNG file path to the success CSV
        append_to_csv(csv_file_success, call_sign, email)
        append_to_csv(csv_file_yes_email, call_sign, email, full_png_path)
    else:
        append_to_csv(csv_file_no_email, call_sign)

logging.info(f"All records processed. Check {csv_file_no_email} for call signs with no email address, {csv_file_yes_email} for call signs with email, and {csv_file_success} for successfully created SVG and PNG files.")
