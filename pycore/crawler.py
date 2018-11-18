import openpyxl

def int_eater(val):

	if val is None:
		return 0
	else:
		try:
			return int(val)  # oh God why
		except ValueError:
			return float(val)

def coord_to_letter(row, col):
	"""Transforms Excel cell coordinate to letter-coordinate (e.g. 15,1 -> A15)

	Args:
		row (int): Excel spreadsheet row number (starting from 1)
		col (int): Excel spreadsheet column number (starting from 1)

	Returns:
		str: Cell coordinate (e.g. 'A15')
	"""

	res = ''
	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

	temp = col - 1

	def __inner__(t):
		nonlocal res
		if t//26 != 0:
			res = res + alphabet[t % 26]
			__inner__(t//26 - 1)
		else:
			res = res + alphabet[t % 26]

	__inner__(temp)
	res = res[::-1] + str(row)

	return res

def letter_to_coord(letter):
	"""Transforms Excel letter-coordinate to numeric oordinate.

	Args:
		letter (str): Excel spreadsheet cell coordinate (e.g. 'A15')

	Returns:
		list: List containing row and column number of the cell.
	"""
	
	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

	row = int("".join(i for i in letter if i.isdigit()))  # разделить числовое обозначение ряда
	col = 0

	temp = "".join(i for i in letter if not i.isdigit())[::-1]  # и буквенное обозначение столбца

	for i in range(len(temp)):
		col += (alphabet.index(temp[i]) + 1) * (26**i)

	return [row, col]

def consq_search(sheet, row, col, direction, stopper, val):
	"""Consequtive search in the table cells starting from cell (row, col) until value-stopper is found
	
	Последовательный поиск в ячейках таблицы начиная с ячейки 
	(row, col) и до ячейки со значением stopper всех значений 
	val
	TODO: wrappers, errors
 
	Args:
		sheet (class 'openpyxl.worksheet.worksheet.Worksheet'): openpyxl Excel worksheet
		row (int): Excel spreadsheet row number (starting from 1)
		col (int): Excel spreadsheet column number (starting from 1)
		direction (str): 'lr' or 'tb' left to right or top to bottom search
		stopper (str): Value-stopper
		val (str): value to search for

	Returns:
		list: list of all matches
	"""
	
	res = []

	if direction == 'lr':  # left to right search
		i = col
	elif direction == 'tb':  # top to bottom search
		i = row
	
	while True:
		if direction == 'lr':
			cl = sheet.cell(row = row, column = i).value
			if cl == stopper:
				break
			elif cl == val:
				res.append([row, i, cl])
			i += 1
		elif direction == 'tb':
			cl = sheet.cell(row = i, column = col).value
			if cl == stopper:
				break
			elif cl == val:
				res.append([i, col, cl])
			i += 1

	return res	

def range_search(sheet, cell_start, cell_stop, val, match = True):
	"""Search in a range of cells [start, stop], where start, stop in letter format.
	
	Поиск по диапазону ячеек [cell_start, cell_stop]. Ячейки в 
	формате A15.

	Args:
		sheet (class 'openpyxl.worksheet.worksheet.Worksheet'): openpyxl Excel worksheet
		cell_start (str): left top cell of range in letter format (e.g. 'A15')
		cell_stop (str): right bottom cell of range in letter format
		val (str): value to search for
		match (bool): find all cells that match value or not
			(default is True)

	Returns:
		list: list of all matches, empty if nothing is found	
	"""

	res = []

	cells = sheet[cell_start: cell_stop]
	dim = len(cells[0])

	for c in cells:
		for d in range(dim):
			if match and c[d].value == val:
				res.append([c[d].row, c[d].col_idx, c[d].value])
			elif not match and not c[d].value == val:
				res.append([c[d].row, c[d].col_idx, c[d].value])

	return res
	