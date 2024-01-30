import pandas as pd

# Path to the input and output CSV files
input_csv = 'reqs.csv'
output_csv = 'iver.csv'

# Read the CSV content from file
df = pd.read_csv(input_csv)

# Filter the rows where "JifUniversal" is present in any column
filtered_df = df[df.apply(lambda row: row.astype(str).str.contains('JifUniversal').any(), axis=1)]

# Write the filtered content to a new CSV file
filtered_df.to_csv(output_csv, index=False)

print(f"Filtered data has been written to {output_csv}")
