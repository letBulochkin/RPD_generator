from docx import Document
from docx.shared import Pt

class rpd(object):

	def __init__(self, file):

		self.DOC = Document(file)
		self.PREFIX = 'РАБОЧАЯ_ПРОГРАММА_'
		self.TABLES = self.DOC.tables
		self.PARS = [x for x in self.DOC.paragraphs if x.text != '']  # получить все не пустые параграфы

	def get_marked_cells(self, table):

		res = []

		for i in range(len(table.rows)):
			for k in range(len(table.row_cells(i))):
				if table.cell(i, k).text == '<>':  # marker
					res.append([i, k])
					break

		return res

	def write_to_cell(self, table, row, col, text):

		table.cell(row, col).paragraphs[0].text = text


	def write_file(self, path, title):
		"""
		TODO: exceptions!
		"""
		
		self.DOC.save(path + self.PREFIX + title + '.docx')
