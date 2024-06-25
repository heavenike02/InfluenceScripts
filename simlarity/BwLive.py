import pandas as Pd

# Paths to the CSV files
Influence_CSV = r"C:\Users\I586445\OneDrive - National University of Ireland, Galway\Documents\InfluenceScripts\simlarity\SAP Analytics Cloud & SAP Digital Boardroom.csv"
# Initialize influence to None or an empty DataFrame
influence = None

# Load CSV files into Pandas DataFrames
try:
    influence = Pd.read_csv(Influence_CSV, usecols=['Request_ID', 'Idea_Title', 'Description', 'Status','Voting Score'])
except Exception as e:
    print(f"Error reading the CSV file: {e}")

# Proceed only if influence is not None
if influence is not None:
    # Search for text in the description column LIKE% BW Live or BW or LIVE or Business Warehouse
    search = influence[influence['Description'].str.contains('BW Live|BW|Business Warehouse', case=False, na=False)]

    # Save the filtered data to a new CSV file
    search.to_csv('search.csv', index=False)

    print("Data search completed successfully!")
else:
    print("Failed to load data. Please check the CSV file and column names.")
