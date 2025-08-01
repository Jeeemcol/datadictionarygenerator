'''
Populates a csv with a data dictionary table that can be
copied from Excel and pasted into a data dictionary.
Takes from the CREATE TABLE statement string and a csv file of
pre-existing name/description pairs to auto-fill where possible.
'''
import re
import csv

def sanitize_input(text):
    '''Ensure input from csv is sanitized'''
    # Remove any characters that are not alphanumeric, spaces, or common punctuation
    text = re.sub(r'[^\x20-\x7E]', '', text)  # Only allow printable ASCII characters
    return text.strip()

# Load column descriptions from an external CSV file and sanitize input
description_file = "existing_column_descriptions.csv"
column_descriptions = {}
try:
    with open(description_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 2:
                # Sanitize both the name and the description
                name = sanitize_input(row[0])
                description = sanitize_input(row[1])
                column_descriptions[name] = description
except FileNotFoundError:
    print(f"""Warning: {description_file} not found.
          It needs to be located in the same folder as this script.""")

# Within the triple apostrophes paste in the entire CREATE TABLE statement
create_statement = '''CREATE TABLE DatabaseOne.schemaOne.TableOne
(
 TableOne_ID NVARCHAR(50) NOT NULL,

 ------------------------- External IDs ----------------------------

 ExternalID1 NVARCHAR(25),
 ExternalID2 INT,

 ------------------------- Name details ----------------------------

 Title VARCHAR(25),
 Firstname VARCHAR(150),
 Surname VARCHAR(150),

 ------------------------- Address details ----------------------------

 AddressLine1 VARCHAR(250),
 AddressLine2 VARCHAR(250),
 AddressLine3 VARCHAR(250),
 AddressLine4 VARCHAR(250),
 AddressLine5 VARCHAR(250),
 AddressLine6 VARCHAR(250),
 Postcode VARCHAR(25),

 ------------------------- Email ----------------------------

 Email VARCHAR(255)
)
'''

# Parse the CREATE TABLE statement
columns = []
for line in create_statement.splitlines():
    line = line.strip()  # Strips white space
    if not line or line.startswith("--") or line.lower().startswith("create table") or line.startswith("(") or line.startswith(")"):
        continue  # Ignore comments, irrelevant lines, and lines with only whitespace
    
    # Remove inline comments (anything after --)
    line = re.split(r'\s*--', line)[0].strip()
    
    match = re.match(r"(\w+)\s+(\w+(?:\(\d+(?:,\d+)?\))?)\s*(NOT NULL)?", line, re.IGNORECASE)
    if match:
        name, data_type, not_null = match.groups()
        nullable = "No" if not_null else "Yes"
        description = re.sub(r'[^\x00-\x7F]+', ' ', column_descriptions.get(name, "")) # remove chars outside ASCII range
        columns.append([name, data_type, nullable, description])

# Write to final data dictionary CSV file
csv_filename = "data_dictionary.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Data Type", "Nullable", "Description"])
    writer.writerows(columns)

print(f"CSV file '{csv_filename}' has been generated successfully.")
