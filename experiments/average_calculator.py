import pandas as pd

# Path to Excel file
csv_path = "experiments\FinalResults\LLMs\mistral.csv"

# Read Excel directly into DataFrame
df = pd.read_csv(csv_path)

df = df.drop(columns=["query_id"])

# Calculate averages
col_avg = df.mean(numeric_only=True)
row_avg = df.mean(axis=1, numeric_only=True)

# Add "Average" row
df.loc["Average"] = col_avg

# Add "Average" column
df["Average"] = list(row_avg) + [row_avg.mean()]

# Save back to Excel
output_path = "experiments/FinalResults/averages_output.xlsx"
df.to_excel(output_path, index=True)

print("Averages calculated!")




