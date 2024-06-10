import pandas as pd

# Define the column name for the ID
id_col = "id"
id_col2 = "id"

# Read the first CSV file with UTF-8 encoding
df1 = pd.read_csv(r"C:\Users\I586445\Downloads\Influence Requests - Jira (Decision & Status).csv", encoding='unicode_escape')

# Read the second CSV file with UTF-8 encoding
df2 = pd.read_csv(r"C:\Users\I586445\Downloads\Influence Requests HANA - (Status_Decision).csv", encoding='unicode_escape')


# Find the missing IDs
missing_ids = set(df1[id_col]) - set(df2[id_col2])

# Print the missing IDs
print(missing_ids)
