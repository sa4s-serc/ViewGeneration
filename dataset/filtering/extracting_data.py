'''
This script reads a CSV file containing architectural data, filters the rows to include only those that mention "UML" in the "Architectural Notation" column, 
and writes the filtered data to a new CSV file. The input and output file paths can be specified as needed.
'''
import csv

def filter_uml_static(input_csv, output_csv):
    try:
        with open(input_csv, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile, delimiter=';')
            # Use the fieldnames from the input CSV for output
            fieldnames = reader.fieldnames
            filtered_rows = [
                row for row in reader 
                if "UML" in row.get('Architectural Notation', '').split(',')
            ]

        # Write the filtered rows to a new CSV file
        with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(filtered_rows)

        print(f"Filtered data written to {output_csv}")

    except FileNotFoundError:
        print(f"Error: File '{input_csv}' not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage:
filter_uml_static('Ground_truth_dataset.csv', 'filtered_output_uml.csv')
