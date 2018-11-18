import openpyxl
from . import crawler

class study_plan(object):
    """
    Study plan class

    TODO: реализовать все алгоритмы поиска отдельно. 
    Привести координаты к единому виду
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
            disciplines.append([sheet.cell(row = i[0], column = 2).value, 
                sheet.cell(row = i[0], column = 3).value]) 
        
        return disciplines


class discipline(object):

    def __init__(self, study_plan, index):
        
        self.STUDY_PLAN = study_plan
        self.INDEX = index
        self.NAME = ''.join(i[1] for i in self.STUDY_PLAN.list_avail_disciplines() if i[0] == index)
        
        if index.rsplit('.')[1] == 'Б': 
            self.PART = True  # базовая
        elif index.rsplit('.')[1] == 'В':
            self.PART = False  # вариативная 

        if index.rsplit('.')[2] == 'ДВ':
            self.OBLIGATION = False  # по выбору
        else:
            self.OBLIGATION = True

        self.COMPETENCIES = self.__get_competencies__()
        self.STUDY_HOURS = self.__get_hours__()  

    def __get_competencies__(self):
        '''
        Возвращает список компетенций, изучаемых дисциплиной, и их описаний
        Returns dictionary of competencies and theirs descriptions
        '''
        
        competencies = []
        sheet = self.STUDY_PLAN.BOOK['Компетенции(2)']
        
        r = crawler.range_search(sheet, 'C4', 'D85', self.INDEX)[0][0]

        for i in sheet.cell(row = r, column = 6).value.rsplit('; '):
            sheet = self.STUDY_PLAN.BOOK['Компетенции']
            cont = sheet.cell(row = crawler.range_search(sheet, 'B3', 'B177', i)[0][0],
                column = 4).value
            competencies.append([i, cont])

        return competencies

    def __get_semesters__(self):
        """
        Нет, это полная хуйня.
        Но в принципе работает. 
        """

        semesters = []  # список семестров, в которые читается дисциплина

        sheet = self.STUDY_PLAN.BOOK['ПланСвод']

        dicp_cell = crawler.range_search(sheet, 'B6', 'B104', self.INDEX)  # поиск ячейки с дисциплиной 

        # задаем диапазон для поиска значений по найденной ячейке
        search_cell_start = crawler.coord_to_letter(dicp_cell[0][0], dicp_cell[0][1] + 14)
        search_cell_stop = crawler.coord_to_letter(dicp_cell[0][0], dicp_cell[0][1] + 21)

        # по тем ячейкам, где было найдено значение, поднимаемся наверх и смотрим номер семестра
        for i in crawler.range_search(sheet, search_cell_start, search_cell_stop, None, False):
            semesters.append(int(sheet.cell(row = 2, column = i[1]).value.rsplit('. ', 1)[1]))

        return semesters

    def __get_hours__(self):

        sem = self.__get_semesters__()
        sheet = self.STUDY_PLAN.BOOK['План']

        for i in range(len(sem)):
            h = {}
            dicp_cell = crawler.range_search(sheet, 'B6', 'B104', self.INDEX)
            sem_cell = crawler.range_search(sheet, 'P2', 'BT2', 'Сем. ' + str(sem[i]))
            h['zach_ed'] = crawler.int_eater(sheet.cell(row = dicp_cell[0][0], column = sem_cell[0][1]).value)
            h['total'] = crawler.int_eater(sheet.cell(row = dicp_cell[0][0], column = sem_cell[0][1] + 1).value)
            h['lect'] = crawler.int_eater(sheet.cell(row = dicp_cell[0][0], column = sem_cell[0][1] + 2).value)
            h['lab'] = crawler.int_eater(sheet.cell(row = dicp_cell[0][0], column = sem_cell[0][1] + 3).value)
            h['pract'] = crawler.int_eater(sheet.cell(row = dicp_cell[0][0], column = sem_cell[0][1] + 4).value)
            h['sam'] = crawler.int_eater(sheet.cell(row = dicp_cell[0][0], column = sem_cell[0][1] + 5).value)
            h['krpa'] = crawler.int_eater(sheet.cell(row = dicp_cell[0][0], column = sem_cell[0][1] + 6).value)
            h['control'] = crawler.int_eater(sheet.cell(row = dicp_cell[0][0], column = sem_cell[0][1] + 7).value)
            sem[i] = [sem[i], h]

        return sem