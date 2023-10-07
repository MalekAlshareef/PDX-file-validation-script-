import os
import xml.etree.ElementTree as ET

# Define the directory containing PDX files
# Adjust this path based on your machine
pdx_directory = 'path/to/pdx/files'

# Define a dictionary of required elements and attributes
required_elements = {
    'diagnostic_definition': ['id', 'version'],
    'diagnostic_item': ['name', 'description'],
}

# Define data type checks for specific elements
data_type_checks = {
    'diagnostic_item': {'duration': int, 'threshold': float},
}

# Initialize counters for statistics
total_files = 0
valid_files = 0
invalid_files = 0

# Create a test report file
report_filename = 'pdx_validation_report.txt'
with open(report_filename, 'w') as report_file:
    report_file.write("PDX Validation Report\n\n")

    # Iterate through PDX files in the directory
    for pdx_file in os.listdir(pdx_directory):
        if pdx_file.endswith('.xml'):
            pdx_file_path = os.path.join(pdx_directory, pdx_file)

            # Increment the total file count
            total_files += 1

            # Define a list to store validation errors
            validation_errors = []

            try:
                # Parse the PDX file
                tree = ET.parse(pdx_file_path)
                root = tree.getroot()

                # Validate required elements and attributes
                for element, attributes in required_elements.items():
                    if root.tag == element:
                        for attribute in attributes:
                            if attribute not in root.attrib:
                                validation_errors.append(f"Missing attribute '{attribute}' in {element} element")

                # Validate data types of specific elements
                for element, data_types in data_type_checks.items():
                    for child in root.findall(element):
                        for attribute, expected_type in data_types.items():
                            if attribute in child.attrib:
                                attribute_value = child.attrib[attribute]
                                try:
                                    expected_type(attribute_value)
                                except ValueError:
                                    validation_errors.append(
                                        f"Invalid data type for '{attribute}' in {element} element")

                # Check for additional validation criteria

                if not validation_errors:
                    valid_files += 1
                    report_file.write(f"File: {pdx_file}\nStatus: Valid\n\n")
                else:
                    invalid_files += 1
                    report_file.write(f"File: {pdx_file}\nStatus: Invalid\n")
                    for error in validation_errors:
                        report_file.write(f"  - {error}\n")
                    report_file.write("\n")

            except ET.ParseError as e:
                invalid_files += 1
                report_file.write(f"File: {pdx_file}\nStatus: Invalid\n")
                report_file.write(f"  - XML parsing error: {str(e)}\n\n")

            except Exception as e:
                invalid_files += 1
                report_file.write(f"File: {pdx_file}\nStatus: Invalid\n")
                report_file.write(f"  - Validation error: {str(e)}\n\n")

# Generate a summary report
with open(report_filename, 'a') as report_file:
    report_file.write("\nSummary:\n")
    report_file.write(f"Total Files: {total_files}\n")
    report_file.write(f"Valid Files: {valid_files}\n")
    report_file.write(f"Invalid Files: {invalid_files}\n")

print(f"Validation report generated: {report_filename}")
