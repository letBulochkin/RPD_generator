from docx import Document
from docx.shared import Pt
from copy import deepcopy

def get_marked_cells(table):
	"""Returns docx table cells that marked with special marker.

	Args:
		table (...): docx table object

	Returns:
		list: list of lists containing marked cell coordinate [row, column]
	"""

	res = []

	for i in range(len(table.rows)):
		for k in range(len(table.row_cells(i))):
			if table.cell(i, k).text == '<>':  # marker
				res.append([i, k])
				break  # но зачем??

	return res

def insert_table_after(table, paragraph):
	"""Inserts table after paragraph.

	Credits: https://github.com/python-openxml/python-docx/issues/156
	ATTENTION: This method modifies list of paragraphs. 

	Args:
		table (...): docx table to copy
		paragraph (...): docx paragraph to paste table after
	"""

	tbl, p = table._tbl, paragraph._p
	p.addnext(tbl)

def copy_table_after(table, paragraph):
	"""Copies table after paragraph.

	Credits: https://github.com/python-openxml/python-docx/issues/156
	ATTENTION: This method modifies list of paragraphs. 

	Args:
		table (...): docx table to copy
		paragraph (...): docx paragraph to paste table after
	"""

	tbl, p = table._tbl, paragraph._p
	new_tbl = deepcopy(tbl)
	p.addnext(new_tbl)

def remove_table(table):
	"""Removes table. Credit: https://stackoverflow.com/questions/47716792/python-docx-delete-table-from-document#comment82455626_47743738"""

	table._element.getparent().remove(table._element)

def seq_write_to_table(table, data):
	"""Sequential writing to self-created table.
	
	Последовательная запись данных вложенного списка в таблицу с добавлением новых ячеек. Метод опеределяет 
	маркированные в таблице ячейки, затем последовательно вставляет в маркированные ячейки соответственно 
	идущие элементы списка. Под каждый новый список создается новая строка в таблице.

	Args:
		table (...): table to overwrite
		data (list): list of lists of the same size
	"""

	markers = []  # список маркеров в заготовке таблицы

	for i in range(len(table.rows)):
		for k in range(len(table.row_cells(i))):
			if table.cell(i, k).text == '<>':  # marker
				markers.append([i, k, table.cell(i, k).paragraphs[0].runs[0].style])  # записываем координаты клетки с маркером
				table.cell(i, k).text = ''  #и стиль каретки. Ячейку с маркером обнуляем

	for i in range(len(data[0])):  # идем сначала по списку вглубь
		for k in range(len(data)):  # потом вширь
			try:
				table.cell(markers[i][0] + k, markers[i][1])  #ячейка существует?
			except IndexError:
				row = table.add_row()  # если нет, добавляем ряд
				[i.add_paragraph() for i in row.cells]  # вставляем в каждую ячейку нового ряда по параграфу
				# добавляем в параграф каретку с текстом и применяем стиль
				table.cell(markers[i][0] + k, markers[i][1]).paragraphs[0].add_run(data[k][i], markers[i][2])
			else:  # если существует, то просто добавляем текст
				table.cell(markers[i][0] + k, markers[i][1]).paragraphs[0].add_run(data[k][i], markers[i][2])

def write_to_cell(table, row, col, text):
	"""Writing text to cell of the table"""

	table.cell(row, col).paragraphs[0].runs[0].text = text

def write_to_par(par, pos, text):
	"""Overwrites marked run in a paragraph.

	TODO: This approach has a major flaw!

	Args:
		par (list): list containing paragraph object and list of marked runs,
			included in it
		pos (int): position of marker to overwrite, 0-based
		text (str): text to write to marker 
	"""

	par[1][pos].text = text
