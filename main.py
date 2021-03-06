from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, 
	QFileDialog, QLabel, QLineEdit, QTextEdit, QGroupBox, 
	QFormLayout, QGridLayout, QVBoxLayout, QPushButton, QScrollArea,
	QSpinBox, QMessageBox)
from pycore import commutator, struct
from functools import partial
from inspect import isclass
from openpyxl.utils.exceptions import InvalidFileException
import os, sys, sip, ui_RPD

class RPD_Window(QMainWindow):
	"""Main Window class"""

	def __init__(self):
		"""Global fields initialization and elements' signals connection"""

		super(RPD_Window, self).__init__()

		self.ui = ui_RPD.Ui_MainWindow()
		self.ui.setupUi(self)

		self.PLAN_FNAME = None
		self.SAMPLE_FNAME = None
		self.RULE_FNAME = None
		self.RPD = None  # может не надо?
		self.RPD_PATH = None

		# list of QGroupBoxes to iterate over
		# [QGroupBox, QLabel - associated label from side panel, Bool - flag to make QGroupBox visible, Bool - flag to make forwButton disabled]
		self.BOXES = [[self.ui.uploadBox, self.ui.uploadBoxLabel, True, True],
			[self.ui.disciplineBox, self.ui.disciplineBoxLabel, False, True],
			[self.ui.competenciesBox, self.ui.competenciesBoxLabel, False, True],
			[self.ui.labBox, self.ui.labBoxLabel, False, True],
			[self.ui.practBox, self.ui.practBoxLabel, False, True],
			[self.ui.downloadBox, self.ui.label_15, False, True]]

		self.ui.backButton.clicked.connect(self.browseBox)  # можно перенести в handleCreateButtonClicked
		self.ui.forwButton.clicked.connect(self.browseBox)
		self.ui.study_planUploadButton.clicked.connect(self.handlePlanButtonClicked)
		self.ui.rpdUploadButton.clicked.connect(self.handleRpdButtonClicked)
		self.ui.ruleUploadButton.clicked.connect(self.handleRuleButtonClicked)
		self.ui.createButton.clicked.connect(self.handleCreateButtonClicked)
		self.ui.dispShowButton.clicked.connect(self.handleDispShowButtonClicked)
		self.ui.downloadPathButton.clicked.connect(self.handleDownloadPathButtonClicked)
		self.ui.downloadButton.clicked.connect(self.handleDownloadButtonClicked)

	"""== Navigation sidebar =="""

	def browseBox(self):
		"""Browses QGroupBox'es in response to button click."""

		for i in range(len(self.BOXES)):
			if self.BOXES[i][2] == True:
				if self.sender().text() == "Далее" and i != (len(self.BOXES) - 1):
					self.BOXES[i][2] = False
					self.BOXES[i][1].setFont(QtGui.QFont("MS Shell Dlg 2", 11, QtGui.QFont.Normal))
					self.BOXES[i][0].setVisible(False)
					self.BOXES[i+1][2] = True
					self.BOXES[i+1][1].setFont(QtGui.QFont("MS Shell Dlg 2", 11, QtGui.QFont.Bold))
					self.BOXES[i+1][0].setVisible(True)
					self.sender().setDisabled(self.BOXES[i+1][3])  # disable forwButton if set True
					break
				elif self.sender().text() == "Вернуться назад" and i != 0:
					self.BOXES[i][2] = False
					self.BOXES[i][1].setFont(QtGui.QFont("MS Shell Dlg 2", 11, QtGui.QFont.Normal))
					self.BOXES[i][0].setVisible(False)
					self.BOXES[i-1][2] = True
					self.BOXES[i-1][1].setFont(QtGui.QFont("MS Shell Dlg 2", 11, QtGui.QFont.Bold))
					self.BOXES[i-1][0].setVisible(True)
					self.ui.forwButton.setDisabled(self.BOXES[i-1][3])
					break
	
	"""== Upload screen =="""

	def handlePlanButtonClicked(self):
		"""Initialize QFileDialog in response to button click. Show chosen path via label."""
		
		self.PLAN_FNAME = QFileDialog.getOpenFileName(self, 'Открыть учебный план')[0]
		self.ui.study_planPathLabel.setText(self.PLAN_FNAME)

	def handleRpdButtonClicked(self):
		"""Initialize QFileDialog in response to button click. Show chosen path via label."""
		
		self.SAMPLE_FNAME = QFileDialog.getOpenFileName(self, 'Открыть шаблон')[0]
		self.ui.rpdPathLabel.setText(self.SAMPLE_FNAME)

	def handleRuleButtonClicked(self):

		self.RULE_FNAME = QFileDialog.getOpenFileName(self, 'Открыть файл конфигурации')[0]
		self.ui.rulePathLabel.setText(self.RULE_FNAME)

	def handleCreateButtonClicked(self):
		"""Create RPD instance with parameters set in the interface."""
		
		if self.PLAN_FNAME != None and self.SAMPLE_FNAME != None and self.RULE_FNAME != None:  # если оба файла заданы
			try:
				self.RPD = commutator.rpd(self.PLAN_FNAME, self.RULE_FNAME, self.SAMPLE_FNAME)  # создаем экземпляр
			except AssertionError as err:
				self.ui.uploadStatusLabel.setText(err.args[0])
			except InvalidFileException:
				self.ui.uploadStatusLabel.setText('Неверный формат файла учебного плана. Сохраните файл в формате .xlsx')
			except ValueError:
				self.ui.uploadStatusLabel.setText('Неверный формат файла шаблона. Загрузите файл в формате .docx')
			except Exception as err:
				warn = QMessageBox()
				warn.setIcon(QMessageBox.Critical)
				warn.setWindowTitle("Критическая ошибка")
				warn.setText("В ходе открытия файлов произошла ошибка.")
				warn.setInformativeText("Тип ошибки представлен внизу. Сообщите его системному администратору.")
				warn.setDetailedText(str(err))
				warn.setStandardButtons(QMessageBox.Ok)
				warn.exec_()
			else:
				self.ui.uploadStatusLabel.setText('Успешно!')
				self.ui.dispComboBox.addItems(  # добавляем в ComboBox доступные дисциплины, объединяя их в строку
					[i[0] + ' ' + i[1] for i in self.RPD.STUDY_PLAN.list_avail_disciplines()])
				self.ui.dispShowButton.setEnabled(True)
				self.sender().setDisabled(True)
				self.ui.forwButton.setEnabled(True)
				self.BOXES[0][3] = False
			# self.ui.dispComboBox.activated.connect(self.on_dispComboBox_activated)
			# self.ui.dispShowButton.clicked.connect(self.handleDispShowButtonClicked)
		else:
			self.ui.uploadStatusLabel.setText('Не выбраны файлы!')

	"""== Discipline info screen =="""

	def handleDispShowButtonClicked(self):
		"""Create discipline instance, fill the QLineEdits with information and add competency descriptions to the next box

		ATTENTION: does not work if called multiple times! 
		"""

		self.RPD.create_discipline(
			self.ui.dispComboBox.itemText(
				self.ui.dispComboBox.currentIndex()).rsplit(' ')[0])  # создаем дисциплину, забирая ее код из текста QComboBox
		self.ui.dispNameEdit.setText(self.RPD.DISCIPLINE.NAME)  # выгружаем информацию о дисциплине в поля формы
		self.ui.dispFieldEdit.setText(self.RPD.STUDY_PLAN.FIELD_OF_KNOW)
		self.ui.dispProfileEdit.setText(self.RPD.STUDY_PLAN.PROFILE)
		self.ui.dispInstituteEdit.setText(self.RPD.STUDY_PLAN.INSTITUTE)
		self.ui.dispFormEdit.setText(self.RPD.STUDY_PLAN.EDU_FORMAT)
		self.ui.dispProgEdit.setText(self.RPD.STUDY_PLAN.EDU_PROG)
		self.ui.dispCathEdit.setText(self.RPD.STUDY_PLAN.CATHEDRA)
		if self.RPD.DISCIPLINE.PART == True:  # выставляем радиокнопки в соотв с видами дисциплины
			self.ui.dispPartBaseButton.setChecked(True)
		else:
			self.ui.dispPartVarButton.setChecked(True)
		if self.RPD.DISCIPLINE.OBLIGATION == True:
			self.ui.dispObligTrueButton.setChecked(True)
		else:
			self.ui.dispObligFalseButton.setChecked(True)

		self.addBox(self.ui.compScrollAreaWidgetContents, ui_RPD.Ui_competencyBox, 
			len(self.RPD.DISCIPLINE.COMPETENCIES))  # добавление competencyBox в соотв с количеством компетенций дисциплины
		lineEdits = self.ui.compScrollAreaWidgetContents.findChildren(QLineEdit)  # получаем дочерние элементы типа
		textEdits = self.ui.compScrollAreaWidgetContents.findChildren(QTextEdit)
		for i in range(len(lineEdits)):  # это наверняка можно оптимизировать
			lineEdits[i].setText(self.RPD.DISCIPLINE.COMPETENCIES[i]['code'])  # вставляем все коды компетенций
		for i in range(0, len(textEdits), 5):
			textEdits[i].setText(self.RPD.DISCIPLINE.COMPETENCIES[i//5]['descrp'])  # вставляем все описания компетенций

		self.ui.compSaveButton.clicked.connect(partial(self.handleCompSaveButtonClicked, 
			self.ui.compScrollAreaWidgetContents))

		for i in range(len(self.RPD.DISCIPLINE.STUDY_HOURS)):  # добавление вкладок с описанием семестров дисциплины
			e = ui_RPD.Ui_semesterBox(self.ui.centralwidget)  # создаем объект класса с родителем - главным виджетом окна
			e.setGeometry(QtCore.QRect(250, 0, 551, 601))
			e.setVisible(False)
			self.BOXES.insert(3 + i, [e, self.ui.label_4, False, True])  # добавляем новый объект в список вкладок после конкретной позиции
			e.dicpNameLabel.setText(self.RPD.DISCIPLINE.NAME)  # заполнение информации об учебных часах в семестре
			e.semNoLabel.setText(str(self.RPD.DISCIPLINE.STUDY_HOURS[i][0]))
			e.lectLabel.setText(str(self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['lect']))
			e.labLabel.setText(str(self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['lab']))
			e.practLabel.setText(str(self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['pract']))
			e.samLabel.setText(str(self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['sam']))
			e.controlLabel.setText(str(self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['krpa'] 
				+ self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['control']))  # Контроль и КрПа складываем
			e.totalLabel.setText(str(self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['total']))
			e.createModuleButton.clicked.connect(partial(self.addBox_module,  
				e.moduleScrollAreaWidgetContents, ui_RPD.Ui_moduleBox, 1))  # partial для вызова метода-приемника сигнала с параметрами
			e.delModuleButton.clicked.connect(partial(self.deleteBox,
				e.moduleScrollAreaWidgetContents))
			e.saveModuleButton.clicked.connect(partial(
				self.handleSaveModuleButtonClicked, 
				e.moduleScrollAreaWidgetContents,
				int(e.semNoLabel.text())))

		self.ui.labCreateButton.clicked.connect(partial(self.addBox_lab,
			self.ui.labScrollAreaWidgetContents, ui_RPD.Ui_taskBox, 1))
		self.ui.labDeleteButton.clicked.connect(partial(self.deleteBox,
			self.ui.labScrollAreaWidgetContents))

		ls = 0
		for i in range(len(self.RPD.DISCIPLINE.STUDY_HOURS)):
			ls += self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['lab']

		self.ui.labTotalLabel.setText(str(ls))
		if ls != 0:
			self.ui.labSaveButton.clicked.connect(self.handleLabSaveButtonClicked)
		else:
			self.ui.labCreateButton.setDisabled(True)
			self.ui.labDeleteButton.setDisabled(True)
			self.ui.labSaveButton.setDisabled(True)
			self.BOXES[3 + len(self.RPD.DISCIPLINE.STUDY_HOURS)][3] = False
			#self.BOXES[3][3] = False

		self.ui.practCreateButton.clicked.connect(partial(self.addBox_pract,
			self.ui.practScrollAreaWidgetContents, ui_RPD.Ui_taskBox, 1))
		self.ui.practDeleteButton.clicked.connect(partial(self.deleteBox,
			self.ui.practScrollAreaWidgetContents))

		ps = 0
		for i in range(len(self.RPD.DISCIPLINE.STUDY_HOURS)):
			ps += self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['pract']

		self.ui.practTotalLabel.setText(str(ps))
		if ps != 0:
			self.ui.practSaveButton.clicked.connect(self.handlePractSaveButtonClicked)
		else:
			self.ui.practCreateButton.setDisabled(True)
			self.ui.practDeleteButton.setDisabled(True)
			self.ui.practSaveButton.setDisabled(True)
			self.BOXES[4 + len(self.RPD.DISCIPLINE.STUDY_HOURS)][3] = False
			#self.BOXES[4][3] = False

		self.sender().setDisabled(True)
		self.ui.forwButton.setEnabled(True)
		self.BOXES[1][3] = False

	"""== Competencies screen =="""

	def handleCompSaveButtonClicked(self, parent):
		
		for i in self.RPD.DISCIPLINE.COMPETENCIES:
			i['part'] = None
			i['to_know'] = None
			i['to_can'] = None
			i['to_be_able'] = None

		textEdits = parent.findChildren(QTextEdit)
		
		for i in range(0, len(textEdits), 5):
			self.RPD.DISCIPLINE.COMPETENCIES[i//5]['part'] = textEdits[i + 1].toPlainText()
			self.RPD.DISCIPLINE.COMPETENCIES[i//5]['to_know'] = textEdits[i + 2].toPlainText()
			self.RPD.DISCIPLINE.COMPETENCIES[i//5]['to_can'] = textEdits[i + 3].toPlainText()
			self.RPD.DISCIPLINE.COMPETENCIES[i//5]['to_be_able'] = textEdits[i + 4].toPlainText()

		self.infoMessagePopUp("Сохранение", "Компетенции сохранены.")

		self.ui.forwButton.setEnabled(True)
		self.BOXES[2][3] = False

	"""== Modules screen =="""

	def handleModuleSpinBoxValueChanged(self, parent):
		"""Display current hours' quantity as value of QSpinBox changes"""

		lineEdits = parent.moduleScrollArea.findChildren(QLineEdit)

		lect, lab, pract, sam = 0, 0, 0, 0
		
		for i in range(0, len(lineEdits), 5):  # итерация по всем найденным элементам интерфейса
			lect += int(lineEdits[i + 1].text())
			lab += int(lineEdits[i + 2].text())
			pract += int(lineEdits[i + 3].text())
			sam += int(lineEdits[i + 4].text())

		parent.lectRelLabel.setText(str(lect))
		parent.labRelLabel.setText(str(lab))
		parent.practRelLabel.setText(str(pract))
		parent.samRelLabel.setText(str(sam))

	def handleSaveModuleButtonClicked(self, parent, semester):  # почему я не реализовал это как метод класса moduleBox?
		"""Overwrites discipline.SEMESTER field with values set in the interface"""

		lineEdits = parent.findChildren(QLineEdit)  # QSpinBox представляется как QLineEdit тоже
		textEdits = parent.findChildren(QTextEdit)
		curr_box = 0
		
		if len(textEdits) == 0:
			self.infoMessagePopUp("Отмена действия", "Не добавлено ни одного раздела!", True)
			return

		for i in self.RPD.DISCIPLINE.SEMESTERS:
			curr_box +=1
			if i[0] == semester:
				i[1] = struct.semester()
				try:
					for k in range(len(textEdits)):
						i[1].add_module(
							int(lineEdits[k*5].text()),
							textEdits[k].toPlainText())
						i[1].add_study(
							int(lineEdits[k*5].text()),
							1,
							int(lineEdits[k*5 + 1].text()))
						i[1].add_study(
							int(lineEdits[k*5].text()),
							2,
							int(lineEdits[k*5 + 2].text()))
						i[1].add_study(
							int(lineEdits[k*5].text()),
							3,
							int(lineEdits[k*5 + 3].text()))
						i[1].add_study(
							int(lineEdits[k*5].text()),
							4,
							int(lineEdits[k*5 + 4].text()))
					break
				except ValueError as err:
					self.infoMessagePopUp("Отмена действия", "Не заполнен номер раздела!", True)
					return

		self.infoMessagePopUp("Сохранение", "Разделы семестра сохранены.")

		self.ui.forwButton.setEnabled(True)
		self.BOXES[2 + curr_box][3] = False

	"""== Labs screen =="""

	def handleLabSpinBoxValueChanged(self, parent):

		lineEdits = self.ui.labScrollArea.findChildren(QLineEdit)

		h = 0

		for i in range(0, len(lineEdits), 2):
			h += int(lineEdits[i+1].text())

		self.ui.labRelLabel.setText(str(h))

	def handleLabSaveButtonClicked(self):

		self.RPD.DISCIPLINE.LABS = []

		lineEdits = self.ui.labScrollArea.findChildren(QLineEdit)
		textEdits = self.ui.labScrollArea.findChildren(QTextEdit)

		if len(lineEdits) == 0:
			self.infoMessagePopUp("Отмена действия", "Не добавлено ни одной лабораторной работы!", True)
			return

		for i in range(0, len(lineEdits), 2):
			q = []
			q.append(lineEdits[i].text())
			q.append(textEdits[i//2].toPlainText())
			q.append(lineEdits[i+1].text())
			self.RPD.DISCIPLINE.LABS.append(q)

		self.infoMessagePopUp("Сохранение", "Лабораторные работы сохранены.")

		self.ui.forwButton.setEnabled(True)
		self.BOXES[3 + len(self.RPD.DISCIPLINE.STUDY_HOURS)][3] = False

	"""== Practs screen =="""

	def handlePractSpinBoxValueChanged(self, parent):

		lineEdits = self.ui.practScrollArea.findChildren(QLineEdit)

		h = 0

		for i in range(0, len(lineEdits), 2):
			h += int(lineEdits[i+1].text())

		self.ui.practRelLabel.setText(str(h))

	def handlePractSaveButtonClicked(self):

		self.RPD.DISCIPLINE.PRACT = []

		lineEdits = self.ui.practScrollArea.findChildren(QLineEdit)
		textEdits = self.ui.practScrollArea.findChildren(QTextEdit)

		if len(lineEdits) == 0:
			self.infoMessagePopUp("Отмена действия", "Не добавлено ни одной практической работы!", True)
			return

		for i in range(0, len(lineEdits), 2):
			q = []
			q.append(lineEdits[i].text())  # ОПАСНО: нет конвертации в int
			q.append(textEdits[i//2].toPlainText())
			q.append(lineEdits[i+1].text())
			self.RPD.DISCIPLINE.PRACT.append(q)

		self.infoMessagePopUp("Сохранение", "Практические работы сохранены.")
		
		self.ui.forwButton.setEnabled(True)
		self.BOXES[4 + len(self.RPD.DISCIPLINE.STUDY_HOURS)][3] = False

	"""== Download screen =="""

	def handleDownloadPathButtonClicked(self):
		"""Init QFileDialog to set RPD saving path"""
		
		dlg = QFileDialog()
		dlg.setFileMode(QFileDialog.Directory)
		self.RPD_PATH = dlg.getExistingDirectory(self, 'Сохранить рабочую программу', 'C\\')
		self.RPD_PATH = r"{}".format(self.RPD_PATH)  # разные методы обработки полученной от QFileDialog строки
		self.RPD_PATH = self.RPD_PATH.replace('/', '\\')  # возможно взаимозаменяемы
		self.RPD_PATH = self.RPD_PATH + '\\'  # добавить в конец / чтобы обращаться к директории
		self.ui.downloadPathLabel.setText(self.RPD_PATH)

	def handleDownloadButtonClicked(self):
		
		if self.RPD_PATH is None:
			self.infoMessagePopUp(
				"Неверное действие", 
				"Укажите папку для сохранения рабочей программы!", 
				True
			)
			return

		try:
			self.RPD.produce(self.RPD_PATH)
		except Exception as err:
			warn = QMessageBox()
			warn.setIcon(QMessageBox.Critical)
			warn.setWindowTitle("Критическая ошибка")
			warn.setText("В ходе формирования Рабочей программы произошла ошибка.")
			warn.setInformativeText("Тип ошибки представлен внизу. Сообщите его системному администратору.")
			warn.setDetailedText(str(err))
			warn.setStandardButtons(QMessageBox.Ok)
			warn.exec_()
		else:
			self.infoMessagePopUp(
				"Завершение работы", 
				"Рабочая программа успешно сформирована.\nСейчас откроется папка с Рабочей программой.\nВнимательно проверьте ее текст, дополните необходимой информацией."
			)
			os.system('explorer "{}"'.format(self.RPD_PATH))
		finally:
			sys.exit()

	"""== QModuleBox addition and deletion methods =="""

	def connectModuleBox(addfunc):
		"""Decorator for addBox method. Connects added QSpinBoxes to local method"""

		def wrapper(self, parent, element, number):
			addfunc(self, parent, element, number)
			e = parent
			while not isinstance(e, ui_RPD.Ui_semesterBox):  # найти тот элемент родитель, в котором есть нужные QLabel
				e = e.parent()
			for i in parent.findChildren(QSpinBox):
				i.valueChanged.connect(partial(self.handleModuleSpinBoxValueChanged, e))
		
		return wrapper

	@connectModuleBox
	def addBox_module(self, parent, element, number):  #какая же это хуйня. 
		"""Link to addBox method to connect decorator (and still have access to original method)"""

		self.addBox(parent, element, number)

	def connectLabBox(addfunc):
		"""Decorator for addBox method. Connects added QSpinBoxes to local method"""

		def wrapper(self, parent, element, number):
			addfunc(self, parent, element, number)
			e = parent
			while not isinstance(e, type(self.ui.labBox)):  # найти тот элемент родитель, в котором есть нужные QLabel
				e = e.parent()
			for i in parent.findChildren(QSpinBox):
				i.valueChanged.connect(self.handleLabSpinBoxValueChanged)
		
		return wrapper

	@connectLabBox
	def addBox_lab(self, parent, element, number):  #какая же это хуйня. 
		"""Link to addBox method to connect decorator (and still have access to original method)"""

		self.addBox(parent, element, number)

	def connectPractBox(addfunc):
		"""Decorator for addBox method. Connects added QSpinBoxes to local method"""

		def wrapper(self, parent, element, number):
			addfunc(self, parent, element, number)
			e = parent
			while not isinstance(e, type(self.ui.practBox)):  # найти тот элемент родитель, в котором есть нужные QLabel
				e = e.parent()
			for i in parent.findChildren(QSpinBox):
				i.valueChanged.connect(self.handlePractSpinBoxValueChanged)
		
		return wrapper

	@connectPractBox
	def addBox_pract(self, parent, element, number):  #какая же это хуйня. 
		"""Link to addBox method to connect decorator (and still have access to original method)"""

		self.addBox(parent, element, number)

	def addBox(self, parent, element, number):
		"""Sequential addition of QGroupBoxes.

		Args:
			parent (...): parent QWidget to add QGroupBoxes
			element (class): interface class to add
			number (int): quantity of elements to add
		"""

		if not parent.findChildren(QVBoxLayout):  # А почему я иду по QVBoxLayout, а не по самим вставляемым классам?
			vert_lay = QVBoxLayout(parent)  # добавление в layout для адекватного отображения элементов (не спрашивай)
		else:
			vert_lay = parent.findChildren(QVBoxLayout)[0]

		for i in range(number):
			e = element(parent)
			vert_lay.addWidget(e)

	def deleteBox(self, parent):
		"""Delete last QVBoxLayout in parent element"""

		if not parent.findChildren(QVBoxLayout):
			pass
		else:
			vert_lay = parent.findChildren(QVBoxLayout)[0]
			otems = [vert_lay.itemAt(i) for i in range(vert_lay.count())]
			if otems:
				box = otems[-1].widget()
				vert_lay.removeWidget(box)
				sip.delete(box)
				box = None
			else:
				pass

	"""== Error handling and dialog windows =="""

	def errorMessagePopUp(self, text):
		pass

	def infoMessagePopUp(self, title, text, warn = False):
		wind = QMessageBox()
		if warn == False:
			wind.setIcon(QMessageBox.Information)
		elif warn == True:
			wind.setIcon(QMessageBox.Warning)
		wind.setWindowTitle(title)
		wind.setText(text)
		wind.setStandardButtons(QMessageBox.Ok)
		wind.exec_()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = RPD_Window()
	window.show()
	sys.exit(app.exec_())
