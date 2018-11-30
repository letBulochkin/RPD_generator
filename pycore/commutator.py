from docx import Document
from . import struct, generator

class rpd(object):

	def __init__(self, source, sample):

		self.STUDY_PLAN = struct.study_plan(source)
		self.DOC = Document(sample)
		self.PREFIX = 'РАБОЧАЯ_ПРОГРАММА_'

		self.__get_paragraphs__()

	def __get_paragraphs__(self):

		self.TEXT = [[x] for x in self.DOC.paragraphs if x.text != '']  # получить все не пустые параграфы
		for i in range(len(self.TEXT)):  # добавляем к параграфам каретки с маркерами
			self.TEXT[i].append([k for k in self.TEXT[i][0].runs if "<>" in k.text])

	def create_discipline(self, index):

		self.DISCIPLINE = struct.discipline(self.STUDY_PLAN, index)

	def __write_file__(self, path, title):

		self.DOC.save(path + self.PREFIX + title + '.docx')

	def produce(self, path):
		
		generator.write_to_cell(self.DOC.tables[2], 0, 0, self.DISCIPLINE.NAME)
		generator.write_to_cell(self.DOC.tables[2], 2, 6, self.DISCIPLINE.STUDY_PLAN.FIELD_OF_KNOW)
		generator.write_to_cell(self.DOC.tables[2], 4, 2, self.DISCIPLINE.STUDY_PLAN.PROFILE)
		generator.write_to_cell(self.DOC.tables[2], 6, 3, self.DISCIPLINE.STUDY_PLAN.INSTITUTE)
		generator.write_to_cell(self.DOC.tables[2], 8, 4, self.DISCIPLINE.STUDY_PLAN.EDU_FORMAT)
		generator.write_to_cell(self.DOC.tables[2], 10, 5, self.DISCIPLINE.STUDY_PLAN.EDU_PROG)
		generator.write_to_cell(self.DOC.tables[2], 12, 1, self.DISCIPLINE.STUDY_PLAN.CATHEDRA)

		generator.write_to_par(self.TEXT[4], 0, self.DISCIPLINE.NAME)
		generator.write_to_par(self.TEXT[4], 1, ', '.join([i[0] for i in self.DISCIPLINE.COMPETENCIES]))
		generator.write_to_par(self.TEXT[4], 2, self.STUDY_PLAN.FIELD_OF_KNOW)
		generator.write_to_par(self.TEXT[4], 3, self.STUDY_PLAN.PROFILE)

		generator.write_to_par(self.TEXT[6], 0, self.DISCIPLINE.NAME)
		if not self.DISCIPLINE.OBLIGATION:
			generator.write_to_par(self.TEXT[6], 1, 'по выбору')
		else:
			generator.write_to_par(self.TEXT[6], 1, '')
		if self.DISCIPLINE.PART:
			generator.write_to_par(self.TEXT[6], 2, 'базовой части')
		else:
			generator.write_to_par(self.TEXT[6], 2, 'вариативной части')

		generator.write_to_par(self.TEXT[6], 3, self.STUDY_PLAN.FIELD_OF_KNOW)

		sum_zach, sum_total = 0, 0
		for i in self.DISCIPLINE.STUDY_HOURS:
			sum_zach += i[1]['zach_ed']
			sum_total += i[1]['total']
		generator.write_to_par(self.TEXT[7], 0, str(sum_zach))
		generator.write_to_par(self.TEXT[7], 1, str(sum_total))

		generator.seq_write_to_table(self.DOC.tables[6], self.DISCIPLINE.COMPETENCIES)

		for i in range(len(self.DISCIPLINE.STUDY_HOURS)):
			print('opa!')
			t = self.DOC.tables[7]
			base_par = [i for i in self.DOC.paragraphs if '4.2' in i.text]
			parg = base_par[0].insert_paragraph_before('4.1.' + str(i+1) + 
				' Семестр ' + str(self.DISCIPLINE.STUDY_HOURS[i][0]))
			generator.copy_table_after(t, parg)
			t = self.DOC.tables[7 + i + 1]
			queue_list = []
			for k in self.DISCIPLINE.SEMESTERS:
				if k[0] == self.DISCIPLINE.STUDY_HOURS[i][0]:
					for l in k[1].MODULES:
						queue_list.append([str(l['num']),
							str(l['lect'] + l['lab'] + l['pract'] + l['sam']),
							str(l['lect']),
							str(l['lab']),
							str(l['pract']),
							str(l['sam'])
						])
			queue_list.append(['Всего: ', 
				str(self.DISCIPLINE.STUDY_HOURS[i][1]['total']), 
				str(self.DISCIPLINE.STUDY_HOURS[i][1]['lect']),
				str(self.DISCIPLINE.STUDY_HOURS[i][1]['lab']),
				str(self.DISCIPLINE.STUDY_HOURS[i][1]['pract']),
				str(self.DISCIPLINE.STUDY_HOURS[i][1]['sam'])
			])
			generator.seq_write_to_table(t, queue_list)
		generator.remove_table(self.DOC.tables[7])

		#self.__write_file__("C:\\Users\\Anton Firsov\\Documents\\Python\\RPD_generator\\data\\", self.DISCIPLINE.INDEX)
		self.__write_file__(path, self.DISCIPLINE.INDEX)
