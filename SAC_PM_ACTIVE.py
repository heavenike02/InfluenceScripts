import csv
import os

# Specify the path to your CSV file
csv_file_path = r"C:\Users\I586445\Downloads\model refresh\SAPJIRA without influence.csv"
# Construct the output file path
output_folder = os.path.dirname(csv_file_path)
output_file_path = os.path.join(output_folder, "SAC_PM_ACTIVE_NO_INFLUENCE.csv")

# Open the CSV file for reading and the output file for writing
with open(csv_file_path, 'r', encoding='utf-8') as file, open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    # Create a CSV writer object
    csv_writer = csv.writer(output_file)
    
    # Write the header row with selected columns
    csv_writer.writerow(["Issue key", "Issue id", "SAC_PM_ACTIVE", "Consumer Digits"])
    
    # Process the header row to get the column indices
    header = next(csv_reader)
    column_indices = {}
    for column_name in ["Issue key", "Issue id"]:
        try:
            column_indices[column_name] = header.index(column_name)
        except ValueError:
            # Handle the case if any of the required columns are not found in the header
            print(f"Column '{column_name}' not found in the CSV file.")
            exit(1)

    # Process each row and write selected columns to the output file
    for row in csv_reader:
        issue_key = row[column_indices["Issue key"]]
        issue_id = row[column_indices["Issue id"]]
    
        
        # Check if "SAC_PM_ACTIVE" is found in any field of the row
        sac_pm_active = any("SAC_PM_ACTIVE" in field for field in row)
        
        new_row = [issue_key, issue_id, sac_pm_active, ""]
        csv_writer.writerow(new_row)
        

print("Code executed successfully.")
