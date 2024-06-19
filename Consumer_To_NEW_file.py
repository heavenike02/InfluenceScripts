import csv
import re
import os

# Specify the path to your CSV file
csv_file_path = r"C:\Users\I586445\Downloads\17-06 Model Update\FPA34 17_06.csv"
# Construct the output file path
output_folder = os.path.dirname(csv_file_path)
output_file_path = os.path.join(output_folder, "Consumer Foreign keys.csv")

# Open the CSV file for reading and the output file for writing
with open(csv_file_path, 'r', encoding='utf-8-sig') as file, open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    # Create a CSV writer object
    csv_writer = csv.writer(output_file)
    
    # Write the header row with selected columns
    csv_writer.writerow(["ISSUEKEY", "CONSUMER"])
    
    # Process the header row to get the column indices
    header = next(csv_reader)
    column_indices = {}
    for column_name in ["ISSUEKEY", "CONSUMER"]:
        try:
            column_indices[column_name] = header.index(column_name)
        except ValueError:
            # Handle the case if any of the required columns are not found in the header
            print(f"Column '{column_name}' not found in the CSV file.")
            exit(1)

    # Process each row and write selected columns to the output file
    for row in csv_reader:
        issue_key = row[column_indices["ISSUEKEY"]]
        consumer_digits = row[column_indices["CONSUMER"]]
        
    
        # Extract the "Consumer Digits" from the "Custom field (Consumer)" column using regex
        matches_consumer = re.findall(r"\bhttps://influence.sap.com.*?(\d{6})", consumer_digits)
        
        # If matches are found, create a new row for each match
        if matches_consumer:
            for match in matches_consumer:
                # Create a new row with details from the original row and the corresponding match
                new_row = [issue_key, match]
                csv_writer.writerow(new_row)
        else:
            # If no matches found, create a new row with details from the original row and an empty "Consumer Digits"
            new_row = [issue_key, ""]
            csv_writer.writerow(new_row)

print("Code executed successfully.")
