import openpyxl

def consq_search(sheet, row, col, direction, stopper, val):
	"""
	Последовательный поиск в ячейках таблицы начиная с ячейки 
	(row, col) и до ячейки со значением stopper всех значений 
	val

	Consequtive search in the table cells starting from cell
	(row, col) until value-stopper is found

	TODO: wrappers maybe? 
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

def range_search(sheet, cell_start, cell_stop, val):
	"""
	Поиск по диапазону ячеек [cell_start, cell_stop]. Ячейки в
	формате A15.

	Search in a range of cells [cell_start, cell_stop], where
	cell_start, cell_stop - D7 format.
	"""

	res = []

	cells = sheet[cell_start: cell_stop]
	dim = len(cells[0])

	for c in cells:
		for d in range(dim):
			if c[d].value == val:
				res.append([c[d].row, c[d].col_idx, c[d].value])

	return res
	