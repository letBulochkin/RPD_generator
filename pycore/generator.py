from docx import Document
from docx.shared import Pt
from copy import deepcopy

class rpd(object):

	def __init__(self, file):

		self.DOC = Document(file)
		self.PREFIX = 'РАБОЧАЯ_ПРОГРАММА_'
		self.TABLES = self.DOC.tables
		self.PARS = [[x] for x in self.DOC.paragraphs if x.text != '']  # получить все не пустые параграфы
		for i in range(len(self.PARS)):  # добавляем к параграфам каретки с маркерами
			self.PARS[i].append([k for k in self.PARS[i][0].runs if "<>" in k.text]) 
	
	def get_marked_cells(self, table):

		res = []

		for i in range(len(table.rows)):
			for k in range(len(table.row_cells(i))):
				if table.cell(i, k).text == '<>':  # marker
					res.append([i, k])
					break

		return res

	def copy_table_after(self, table, paragraph):
		"""https://github.com/python-openxml/python-docx/issues/156"""

		tbl, p = table._tbl, paragraph._p
		new_tbl = deepcopy(tbl)
		p.addnext(new_tbl)

	def seq_write_to_table(self, table, data):
		"""
		Последовательная запись данных вложенного списка в таблицу с добавлением новых ячеек. Метод опеределяет 
		маркированные в таблице ячейки, затем последовательно вставляет в маркированные ячейки соответственно 
		идущие элементы списка. Под каждый новый список создается новая строка в таблице.

		Sequential writing to self-created table. 
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
					table.cell(markers[i][0] + k, markers[i][1]).paragraphs[0].add_run(data[k][i], markers[i][2])  # добавляем в параграф каретку с текстом и применяем стиль
				else:  # если существует, то просто добавляем текст
					table.cell(markers[i][0] + k, markers[i][1]).paragraphs[0].add_run(data[k][i], markers[i][2])

	def write_to_cell(self, table, row, col, text):

		table.cell(row, col).paragraphs[0].runs[0].text = text

	def write_to_par(self, par, pos, text):
		"""
		TODO: this has a major flaw! 
		"""

		self.PARS[par][1][pos].text = text

	def write_file(self, path, title):
		"""
		TODO: exceptions!
		"""
		
		self.DOC.save(path + self.PREFIX + title + '.docx')
