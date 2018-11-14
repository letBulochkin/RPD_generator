from . import struct, generator

class session(object):

	def __init__(self, source, sample):
		
		self.STUDY_PLAN = struct.study_plan(source)
		self.RPD = generator.rpd(sample)

	def create_discipline(self, index):

		self.DISCIPLINE = struct.discipline(self.STUDY_PLAN, index)

	def produce(self):
		
		self.RPD.write_to_cell(self.RPD.TABLES[2], 0, 0, self.DISCIPLINE.NAME)
		self.RPD.write_to_cell(self.RPD.TABLES[2], 2, 6, self.DISCIPLINE.STUDY_PLAN.FIELD_OF_KNOW)
		self.RPD.write_to_cell(self.RPD.TABLES[2], 4, 2, self.DISCIPLINE.STUDY_PLAN.PROFILE)
		self.RPD.write_to_cell(self.RPD.TABLES[2], 6, 3, self.DISCIPLINE.STUDY_PLAN.INSTITUTE)
		self.RPD.write_to_cell(self.RPD.TABLES[2], 8, 4, self.DISCIPLINE.STUDY_PLAN.EDU_FORMAT)
		self.RPD.write_to_cell(self.RPD.TABLES[2], 10, 5, self.DISCIPLINE.STUDY_PLAN.EDU_PROG)
		self.RPD.write_to_cell(self.RPD.TABLES[2], 12, 1, self.DISCIPLINE.STUDY_PLAN.CATHEDRA)

		self.RPD.write_to_par(4, 0, self.DISCIPLINE.NAME)
		self.RPD.write_to_par(4, 1, ', '.join([i[0] for i in self.DISCIPLINE.COMPETENCIES]))
		self.RPD.write_to_par(4, 2, self.STUDY_PLAN.FIELD_OF_KNOW)
		self.RPD.write_to_par(4, 3, self.STUDY_PLAN.PROFILE)

		self.RPD.write_to_par(6, 0, self.DISCIPLINE.NAME)
		if not self.DISCIPLINE.OBLIGATION:
			self.RPD.write_to_par(6, 1, 'по выбору')
		else:
			self.RPD.write_to_par(6, 1, '')
		if self.DISCIPLINE.PART:
			self.RPD.write_to_par(6, 2, 'базовой части')
		else:
			self.RPD.write_to_par(6, 2, 'вариативной части')

		self.RPD.write_to_par(6, 3, self.STUDY_PLAN.FIELD_OF_KNOW)

		self.RPD.seq_write_to_table(self.RPD.TABLES[6], self.DISCIPLINE.COMPETENCIES)

		self.RPD.write_file("C:\\Users\\Anton Firsov\\Documents\\Python\\RPD_generator\\data\\", self.DISCIPLINE.INDEX)
