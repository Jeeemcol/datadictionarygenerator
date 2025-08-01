<img width="65" height="21" alt="image" src="https://github.com/user-attachments/assets/c11ed4e7-2d8e-4ce6-a95d-909336549fd0" /># datadictionarygenerator
Generates an Excel file of columns, data types and NULL status from CREATE TABLE statement. Uses pre-existing columns and descriptions if supplied as well.

Simple tool that when supplied with SQL as in the example, hard-coded in generate_data_dictionary.py:

        # Within the triple apostrophes paste in the entire CREATE TABLE statement
        create_statement = '''CREATE TABLE DatabaseOne.schemaOne.TableOne

        .... etc.

and a CSV of pre-existing columns we don't want to have to manually add:

        # Load column descriptions from an external CSV file and sanitize input
        description_file = "column_descriptions.csv"

| Name         	| Description           	|
|--------------	|-----------------------	|
| Title        	| Person title          	|
| Firstname    	| Person firstname      	|
| Surname      	| Person surname        	|
| AddressLine1 	| Person address line 1 	|
| AddressLine2 	| Person address line 2 	|

will, when run, output "data_dictionary.csv" (if fails you may need to close this file/ delete it if pre-existing, icr rn):

        # Write to final data dictionary CSV file
        csv_filename = "data_dictionary.csv"

This will output in this format in the CSV file:

| Name         	| Data Type    	| Nullable 	| Description           	|
|--------------	|--------------	|----------	|-----------------------	|
| Title        	| VARCHAR(25)  	| Yes      	| Person title          	|
| Firstname    	| VARCHAR(150) 	| Yes      	| Person firstname      	|
| Surname      	| VARCHAR(150) 	| Yes      	| Person surname        	|
| AddressLine1 	| VARCHAR(250) 	| Yes      	| Person address line 1 	|
| AddressLine2 	| VARCHAR(250) 	| Yes      	| Person address line 2 	|

you can then copy that table format directly into a Data Dictionary
