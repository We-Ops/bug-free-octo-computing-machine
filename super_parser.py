import os
import csv
from datetime import datetime
import sys

# Locate the CSV file with the latest creation time in the current directory
def find_latest_csv_file():
    # Locate all CSV files in the current directory, excluding those starting with "OUTPUT"
    csv_files = [file for file in os.listdir('.') if file.endswith('.csv') and not file.startswith('OUTPUT')]
    if not csv_files:
        return None
    # Get the file with the latest creation time
    latest_file = max(csv_files, key=os.path.getctime)
    return latest_file

# Filter rows containing any of the specified keywords
def filter_csv_content(input_file, output_file, keywords):
    with open(input_file, mode='r') as csv_file, open(output_file, mode='w', newline='') as output_csv:
        reader = csv.reader(csv_file)
        writer = csv.writer(output_csv)
        
        # Check if the input file has any rows
        try:
            header = next(reader)  # Read the header
            writer.writerow(header)  # Write the header to the output file
        except StopIteration:
            print(f"The input file '{input_file}' is empty. No output file generated.")
            return
        
        # Write rows containing any of the specified keywords
        for row in reader:
            if any(keyword in ','.join(row) for keyword in keywords):
                writer.writerow(row)

# Main logic
if __name__ == "__main__":
    # Use default keywords if no arguments are passed
    if len(sys.argv) < 2:
        print("No keywords provided. Using default keywords: ['CR;1', 'CR,2']")
        keywords = ["CR;1", "CR,2"]
    else:
        # Get the list of keywords from command-line arguments
        keywords = sys.argv[1:]

    # Find the latest CSV file
    latest_csv_file = find_latest_csv_file()
    if not latest_csv_file:
        print("No CSV files found in the current directory.")
    else:
        # Generate the output file name with the current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        output_file_name = f"OUTPUT_{current_date}.csv"

        # Filter and write to the output file
        filter_csv_content(latest_csv_file, output_file_name, keywords)
        print(f"Filtered content written to {output_file_name}")