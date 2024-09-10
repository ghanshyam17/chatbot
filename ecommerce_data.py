import pandas as pd
from sqlalchemy import create_engine
import openpyxl
import warnings

# Function to get data from a named range in Excel
def get_named_range_data(workbook, named_range_name):
    named_range = workbook.defined_names[named_range_name]
    sheet_name, cell_range = list(named_range.destinations)[0]  # Extract the sheet name and range
    sheet = workbook[sheet_name]
    return [[cell.value for cell in row] for row in sheet[cell_range]] 

# Suppress specific warnings from openpyxl
warnings.filterwarnings("ignore", category=UserWarning, module='openpyxl')

# Step 1: Load the Excel file using openpyxl
workbook = openpyxl.load_workbook(r'C:\Users\Gsutar\ghanshyam\excel_tool\coverage\Krylon 09-09-2024.xlsx', data_only=True)
# Step 2: Extract data from the named range "analysis_data"
analysis_data = get_named_range_data(workbook, 'analysis_data')

# Step 2: Extract data from the named range "analysis_data"
analysis_data = get_named_range_data(workbook, 'analysis_data')

# Step 3: Convert the extracted data into a pandas DataFrame
# Assuming the first row contains headers
analysis_data_df = pd.DataFrame(analysis_data[1:], columns=analysis_data[0])

# Step 4: Handle unnamed columns by assigning default names
# This will replace 'None' or empty column headers with 'Unnamed_X'
analysis_data_df.columns = [
    f"Unnamed_{i}" if col is None or col == '' else col for i, col in enumerate(analysis_data_df.columns)
]

# Print the DataFrame columns to verify that unnamed columns are handled
print(analysis_data_df.columns)

# Step 5: Create the SQLite database using SQLAlchemy and pandas `to_sql`
# SQLite database path and engine creation
engine = create_engine('sqlite:///analysis.db', echo=True)

# Step 6: Write the DataFrame to the SQLite database
# This will create a table named 'analysis' with the DataFrame columns and data
try:
    analysis_data_df.to_sql('analysis', con=engine, if_exists='replace', index=False)
    print("Data inserted successfully into the database.")
except Exception as e:
    print(f"An error occurred: {e}")
