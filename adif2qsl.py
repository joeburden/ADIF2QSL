import os
import csv
import logging
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
import re
import subprocess

# Ensure the output_files directory exists
output_dir = 'output_files'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Configure logging
logging.basicConfig(filename=os.path.join(output_dir, 'debug.txt'),
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

def append_to_csv(file_path, call_sign, email=None, png_path=None, address=None, qth=None, state=None, zip_code=None, country=None):
    with open(file_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([call_sign, email, png_path, address, qth, state, zip_code, country])

def write_headers(csv_file, headers):
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)

def extract_state_and_country(address):
    parts = address.split(',')
    state = parts[-2].split()[-1].strip() if len(parts) >= 2 else ''
    country = parts[-1].strip() if len(parts) >= 1 else ''
    return state, country

def extract_zip_from_address(address):
    match = re.search(r'\b\d{5}(?:-\d{4})?\b', address)
    if match:
        zip_code = match.group(0)
        address = address.replace(zip_code, '').strip()
        return address, zip_code
    return address, ''

# Define file paths
adif_file = 'input.adif'  # Input ADIF file path
svg_file = 'template.svg'  # Template SVG file path
output_dir = 'output_files'  # Output directory for SVG and PNG files
csv_file_no_email = os.path.join(output_dir, 'NOEMAIL.CSV')  # CSV file path for call signs with no email
csv_file_success = os.path.join(output_dir, 'SUCCESS.CSV')  # CSV file path for successfully created SVG and PNG files
csv_file_yes_email = os.path.join(output_dir, 'YESEMAIL.CSV')  # CSV file path for call signs with email

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Write headers to CSV files
write_headers(csv_file_no_email, ["CALL_SIGN"])
write_headers(csv_file_success, ["CALL_SIGN", "EMAIL", "PNG_PATH", "ADDRESS", "QTH", "STATE", "ZIP_CODE", "COUNTRY"])
write_headers(csv_file_yes_email, ["CALL_SIGN", "EMAIL", "PNG_PATH"])

# Initialize counters for summary
total_callsigns = 0
callsigns_with_email = 0
callsigns_without_email = 0

# Read ADIF records
adif_records = read_adif(adif_file)
svg_template = read_svg(svg_file)

# Process each record and save as SVG and PNG files
for record in adif_records:
    total_callsigns += 1
    adif_data = record  # Directly use the parsed record
    call_sign = adif_data.get('CALL', 'unknown')
    email = adif_data.get('EMAIL')
    address = adif_data.get('ADDRESS')
    qth = adif_data.get('QTH')
    zip_code = adif_data.get('ZIP')
    
    if address:
        address, extracted_zip_code = extract_zip_from_address(address)
        state, country = extract_state_and_country(address)
        zip_code = extracted_zip_code or zip_code
        state = state.upper()  # Convert state to upper case
    
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
    
    if email:
        callsigns_with_email += 1
        # Append the call sign, email, PNG file path, address, qth, state, zip code, and country to the success CSV
        append_to_csv(csv_file_success, call_sign, email, full_png_path, address, qth, state, zip_code, country)
        append_to_csv(csv_file_yes_email, call_sign, email, full_png_path)
    else:
        callsigns_without_email += 1
        # Even if there's no email, still append to the success CSV with empty email
        append_to_csv(csv_file_success, call_sign, '', full_png_path, address, qth, state, zip_code, country)
        append_to_csv(csv_file_no_email, call_sign)

# Print summary to console
summary = (f"Total call signs processed: {total_callsigns}\n"
           f"Call signs with email addresses: {callsigns_with_email}\n"
           f"Call signs without email addresses: {callsigns_without_email}")

print(summary)

# Write summary to summary.txt file
summary_file_path = os.path.join(output_dir, 'summary.txt')
with open(summary_file_path, 'w') as summary_file:
    summary_file.write(summary)

logging.info("All records processed. Check NOEMAIL.CSV for call signs with no email address, YESEMAIL.CSV for call signs with email, and SUCCESS.CSV for successfully created SVG and PNG files.")
logging.info(summary)

# Comment by joe
