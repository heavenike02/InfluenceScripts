import csv
import re
import tempfile
import shutil

# Specify the path to your CSV file
csv_file_path = r"C:\Users\I586445\Downloads\SAPJIRA 2024-03-23T22_45_44+0000.csv"

# Create a temporary file to write the modified data
temp_file_path = tempfile.mktemp()

# Open the CSV file for reading and the temporary file for writing
with open(csv_file_path, 'r', encoding='utf-8') as file, open(temp_file_path, 'w', newline='', encoding='utf-8') as temp_file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    # Create a CSV writer object
    csv_writer = csv.writer(temp_file)
    
    # Process the header row
    header = next(csv_reader)
    column_index_consumer = header.index("Custom field (Consumer)")
    header.insert(column_index_consumer + 1, "Consumer Digits")
    
    # Add a new boolean column "SAC_PM_ACTIVE" after "Consumer Digits"
    column_index_active = column_index_consumer + 2
    header.insert(column_index_active, "SAC_PM_ACTIVE")
    
    csv_writer.writerow(header)
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        value_consumer = row[column_index_consumer]
        
        # Check if the value starts with "https://influence.sap.com" and extract consumer digits
        # Using regex pattern 
        # \b represents a word boundary. This ensures that the link is preceded by a word boundary,
        # accommodating for spaces before the link. This should prevent data from being missed when extracting consumer digits.
        matches_consumer = re.findall(r"\bhttps://influence.sap.com.*?(\d{6})", value_consumer)
        if matches_consumer:
            # Insert consumer digits into the row
            row.insert(column_index_consumer + 1, ','.join(matches_consumer))
        else:
            row.insert(column_index_consumer + 1, "")
        
        # Check if "SAC_PM_ACTIVE" is found in any field of the row
        if any("SAC_PM_ACTIVE" in field for field in row):
            row.insert(column_index_active, True)
        else:
            row.insert(column_index_active, False)
        
        # Write the updated row to the temporary file
        # Iterate over each row in the CSV file
        for row in csv_reader:
            value_consumer = row[column_index_consumer]
            
            # Check if the value starts with "https://influence.sap.com" and extract consumer digits
            # Using regex pattern 
            # \b represents a word boundary. This ensures that the link is preceded by a word boundary,
            # accommodating for spaces before the link. This should prevent data from being missed when extracting consumer digits.
            matches_consumer = re.findall(r"\bhttps://influence.sap.com.*?(\d{6})", value_consumer)
            if matches_consumer:
                # Insert consumer digits into the row
                row.insert(column_index_consumer + 1, ','.join(matches_consumer))
            else:
                row.insert(column_index_consumer + 1, "")
            
            # Check if "SAC_PM_ACTIVE" is found in any field of the row
            if any("SAC_PM_ACTIVE" in field for field in row):
                row.insert(column_index_active, True)
            else:
                row.insert(column_index_active, False)
            
            
            # Write the updated row to the temporary file
            csv_writer.writerow(row)


# Replace the original file with the modified data
shutil.move(temp_file_path, csv_file_path)
Print("code executed successfully")