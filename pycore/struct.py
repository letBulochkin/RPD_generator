import openpyxl
from . import crawler

class study_plan(object):
    """
    Study plan class
    """

    def __init__(self, file):
        '''
        Инициализация полей класса
        Class attributes initialization

        TODO: oh we need mapper
        '''

        self.BOOK = openpyxl.load_workbook(file)
        sheet = self.BOOK['Титул']
        
        self.MINISTRY = sheet['B1'].value
        self.UNIVERCITY = sheet['B10'].value.rsplit('\n', 1)[0]
        self.INSTITUTE = sheet['B10'].value.rsplit('\n', 1)[1]
        self.RECTOR = sheet['X12'].value
        self.FIELD_OF_KNOW = sheet['B18'].value.rsplit('Направление ', 1)[1]
        self.PROFILE = sheet['B19'].value
        self.CATHEDRA = sheet['B26'].value
        self.QUALI_LEVEL = sheet['A29'].value.rsplit('Квалификация: ', 1)[1]
        self.EDU_PROG = sheet['A30'].value.rsplit('Программа подготовки: ', 1)[1]
        self.EDU_FORMAT = sheet['A31'].value.rsplit('Форма обучения: ', 1)[1]
        self.EDU_TIME = sheet['A32'].value.rsplit('Срок обучения: ', 1)[1]  # поправить, убрать приписку г
        self.START_YEAR = sheet['T29'].value

    def data_parse(self):
        pass

    def list_avail_disciplines(self):
        '''
        Возвращает список изучаемых на кафедре дисцпилин
        Returns list of available disciplines
        '''

        disciplines = []
        sheet = self.BOOK['ПланСвод']

        for i in crawler.range_search(sheet, 'Y6', 'Y104', self.CATHEDRA):
            disciplines.append(sheet.cell(row = i[0], column = 2).value)
        
        return disciplines


class discipline(object):

    def __init__(self, study_plan, index):
        
        self.STUDY_PLAN = study_plan
        self.INDEX = index
        self.NAME = None
        self.PART = None
        self.OBLIGATION = None
        self.COMPETENCIES = self.__get_competencies__()

    def __get_competencies__(self):
        '''
        Возвращает словарь компетенций, изучаемых дисциплиной, и их описаний
        Returns dictionary of competencies and theirs descriptions

        '''
        
        competencies = {}
        sheet = self.STUDY_PLAN.BOOK['Компетенции(2)']
        
        r = crawler.range_search(sheet, 'C4', 'D85', self.INDEX)[0][0]

        for i in sheet.cell(row = r, column = 6).value.rsplit('; '):
            sheet = self.STUDY_PLAN.BOOK['Компетенции']
            cont = sheet.cell(row = crawler.range_search(sheet, 'B3', 'B177', i)[0][0],
                column = 4).value
            competencies[i] = cont

        return competencies

