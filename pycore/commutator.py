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

		self.RPD.write_file("C:\\Users\\Anton Firsov\\Documents\\Python\\RPD_generator\\data\\", self.DISCIPLINE.INDEX)
