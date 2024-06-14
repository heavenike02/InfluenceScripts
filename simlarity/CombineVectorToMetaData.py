import pandas as pd


# Paths to the CSV files
full_similar_features_csv = 'full_similar_product_features.csv'
sap_analytics_csv = 'SAP Analytics Cloud & SAP Digital Boardroom.csv'

try:
    # Load CSV files into Pandas DataFrames
    full_similar_features = pd.read_csv(full_similar_features_csv)
    sap_analytics = pd.read_csv(sap_analytics_csv, usecols=['Request_ID', 'Idea_Title', 'Description','Status'])
except FileNotFoundError:
    print(f"Error: One or more CSV files not found. Please check the file paths.")
    exit(1)
except pd.errors.ParserError:
    print(f"Error: Failed to parse the CSV files. Please check the file format.")
    exit(1)

try:
    # Merge the metadata for both feature_id and similar_feature_id
    merged_data = pd.merge(full_similar_features, sap_analytics, left_on='Feature_ID', right_on='Request_ID')
    merged_data = pd.merge(merged_data, sap_analytics, left_on='Similar_Feature_ID', right_on='Request_ID')
except KeyError:
    print(f"Error: One or more columns not found in the CSV files. Please check the column names.")
    exit(1)

try:
    # Drop the duplicate columns
    merged_data = merged_data.drop_duplicates(subset=['Feature_ID', 'Similar_Feature_ID'], keep='first')
except ValueError:
    print(f"Error: Failed to drop duplicate rows. Please check the data.")
    exit(1)

try:
    # Save the merged data to a new CSV file
    merged_data.to_csv('merged_data.csv', index=False)
except PermissionError:
    print(f"Error: Failed to write to the output CSV file. Please check the file permissions.")
    exit(1)
except IOError:
    print(f"Error: Failed to write to the output CSV file. Please check the file path.")
    exit(1)

print("Data merging completed successfully!")