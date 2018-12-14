from sys import argv as args
import pyexcel as pe
import os

# Check if any argument is missing
if len(args) != 3:
	print("Arguments missing!")
	exit(0)

input_path, output_path = args[1:]

files = []
if os.path.isfile(input_path):
	files.append(input_path)
else:
	if not input_path.endswith('/'):
		input_path += '/'

	files = os.listdir(input_path)

if not output_path.endswith('/'):
	output_path += '/'

for file in files:
	file_path = input_path + file
	workbook = pe.get_book(file_name=file_path)
	sheets = workbook.sheet_names()
	
	for sheet in sheets:
		content = workbook[sheet].get_array()
		# table_name comes from the sheet name if there's more than one in the workbook
		# or from the filename, if there's just one sheet
		table_name = sheet if len(sheets) > 1 else file.split('.')[0]

		columns = ','.join(content[0])
		query_file = open('%s%s.sql' % (output_path, table_name), 'w')

		for line in content[1:]:
			# If the value is not an int or float, it'll be treated as a string
			values = ','.join([str(col) if type(col) in [int, float] else '\'%s\'' % col for col in line])
			query_file.write('INSERT INTO %s (%s) VALUES (%s)\n' % (table_name, columns, values))

		query_file.close()
		print('File \'%s.sql\' created successfully!' % table_name)
