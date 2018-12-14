# Sheet To SQL

An easy way to create SQL inserts from an excel sheet.

I needed to insert in SQL database a bunch of data stored in excel files.
Got tired of manually convert all files to CSV and make a specifical code for each file and I made a script that treat'em all.

# Requirements

You'll need *pyexcel* (`pip install pyexcel`) to execute the code.

The sheets should have a header with the columns names.

# Table names

If there's more than one sheet in the workbook, then the table name will be the sheet's name, otherwise it'll be the filename.

# Arguments

sheet_to_sql.py *input_path* *output_path*

- *input_path*: folder with excel files or a single workbook with one or more sheets with data;
- *output_path*: directory where all the SQL files will be stored.
