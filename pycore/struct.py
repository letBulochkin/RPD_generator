import openpyxl

class study_plan(object):
    """
    Study plan class
    """

    def __init__(self, file):
        '''
        Инициализация полей класса
        Class attributes initialization
        '''

        self.BOOK = openpyxl.load_workbook(file)
        sheet = self.BOOK['Титул']
        
        self.MINISTRY = sheet['C8'].value
        self.UNIVERCITY = sheet['A10'].value.rsplit('\n', 1)[0]
        self.INSTITUTE = sheet['A10'].value.rsplit('\n', 1)[1]
        self.RECTOR = sheet['X12'].value
        self.FIELD_OF_KNOW = sheet['B17'].value.rsplit('Направление ', 1)[1]
        self.PROFILE = sheet['B18'].value.rsplit('Профиль: ', 1)[1]
        self.CATHEDRA = sheet['C26'].value
        self.QUALI_LEVEL = sheet['B30'].value.rsplit('Квалификация: ', 1)[1]
        self.EDU_PROG = sheet['B31'].value.rsplit('Программа подготовки: ', 1)[1]
        self.EDU_FORMAT = sheet['B32'].value.rsplit('Форма обучения: ', 1)[1]
        self.EDU_TIME = sheet['B33'].value.rsplit('Срок обучения: ', 1)[1]  # поправить, убрать приписку г
        self.START_YEAR = sheet['R30'].value

    def data_parse(self):
        pass

    def list_avail_disciplines(self):
        '''
        Возвращает список изучаемых на кафедре дисцпилин
        Returns list of available disciplines

        TODO: make it as separate function
        '''

        disciplines = []
        sheet = self.BOOK['ПланСвод']
        i = 6
        while True:
            col = sheet.cell(row = i, column = 48).value
            if col == None:
                break
            elif col == self.CATHEDRA:
                disciplines.append(sheet.cell(row = i, column = 3).value)
            i += 1
        
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

        TODO: make seacrh algorithm a separate function
        '''
        
        competencies = {}
        sheet = self.STUDY_PLAN.BOOK['Компетенции(2)']
        cells = sheet['C12': 'C305']

        for c in cells:
            if c[0].value == self.INDEX:
                i = 7
                while True:
                    col = sheet.cell(row = c[0].row, column = i).value
                    if col == None:
                        break
                    else:
                        sheet = self.STUDY_PLAN.BOOK['Компетенции']
                        diap = sheet['D1': 'D4222']
                        for d in diap:
                            if d[0].value == col:
                                content = sheet.cell(row = d[0].row,
                                    column = d[0].col_idx + 3).value  # сдвиг на три ячейки
                                competencies[col] = content
                        sheet = self.STUDY_PLAN.BOOK['Компетенции(2)']
                    i += 1

        return competencies













    