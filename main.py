from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, 
	QFileDialog, QLabel, QLineEdit, QTextEdit, QGroupBox, 
	QFormLayout, QGridLayout, QVBoxLayout, QPushButton, QScrollArea,
	QSpinBox)
from pycore import commutator
from functools import partial
from inspect import isclass
import os, sys, sip, ui_RPD

class competencyBox(QWidget):
	"""QT Interface class: QGroupBox containing competencies info"""

	def __init__(self, parent):

		super(competencyBox, self).__init__(parent)

		self.compCodeLineEdit = QLineEdit()
		self.compCodeLineEdit.setDisabled(True)
		self.compDescrpTextEdit = QTextEdit()
		self.compDescrpTextEdit.setDisabled(True)
		self.compPartTextEdit = QTextEdit()
		self.compKnowTextEdit = QTextEdit()
		self.compCanTextEdit = QTextEdit()
		self.compAbilTextEdit = QTextEdit()

		self.lay = QVBoxLayout(self)
		self.box = QGroupBox(self)
		self.lay.addWidget(self.box)
		self.form_lay = QFormLayout(self)
		self.form_lay.addRow(QLabel("Код: "), self.compCodeLineEdit)
		self.form_lay.addRow(QLabel("Описание: "), self.compDescrpTextEdit)
		self.form_lay.addRow(QLabel("в части... "), self.compPartTextEdit)
		self.form_lay.addRow(QLabel("Знать: "), self.compKnowTextEdit)
		self.form_lay.addRow(QLabel("Уметь: "), self.compCanTextEdit)
		self.form_lay.addRow(QLabel("Владеть: "), self.compAbilTextEdit)

		self.box.setLayout(self.form_lay)
		# self.box.setFixedSize(460, 240)

class moduleBox(QWidget):
	"""QT Interface class: QGroupBox containing semester's module info"""

	def __init__(self, parent):

		super(moduleBox, self).__init__(parent)

		self.moduleNoLineEdit = QLineEdit()
		self.moduleDescrpTextEdit = QTextEdit()
		self.moduleLectSpinBox = QSpinBox()
		self.moduleLabSpinBox = QSpinBox()
		self.modulePractSpinBox = QSpinBox()
		self.moduleSamSpinBox = QSpinBox()

		self.lay = QVBoxLayout(self)
		self.box = QGroupBox(self)
		self.lay.addWidget(self.box)
		self.form_lay = QFormLayout(self)
		self.form_lay.addRow(QLabel("Номер раздела: "), self.moduleNoLineEdit)
		self.form_lay.addRow(QLabel("Название раздела: "), self.moduleDescrpTextEdit)
		self.form_lay.addRow(QLabel("Лекций (часов): "), self.moduleLectSpinBox)
		self.form_lay.addRow(QLabel("Лабораторных (часов): "), self.moduleLabSpinBox)
		self.form_lay.addRow(QLabel("Практик (часов): "), self.modulePractSpinBox)
		self.form_lay.addRow(QLabel("Самост. работ (часов): "), self.moduleSamSpinBox)

		self.box.setLayout(self.form_lay)

class semesterBox(QWidget):
	"""QT Interface class: QGroupBox containing semester info"""

	def __init__(self, parent):

		super(semesterBox, self).__init__(parent)

		font = QtGui.QFont()
		font.setPointSize(11)
		
		self.box = QGroupBox(self)
		self.box.setTitle("Разделы дисциплины")
		self.box.setFont(font)

		self.dicpInfoLabel = QLabel(self.box)
		self.dicpInfoLabel.setText("Дисциплина: ")
		self.dicpInfoLabel.setGeometry(QtCore.QRect(10, 30, 91, 16))
		self.dicpNameLabel = QLabel(self.box)
		self.dicpNameLabel.setGeometry(QtCore.QRect(100, 30, 431, 16))
		
		self.semNoInfoLabel = QLabel(self.box)
		self.semNoInfoLabel.setText("Семестр №")
		self.semNoInfoLabel.setGeometry(QtCore.QRect(10, 50, 81, 16))
		self.semNoLabel = QLabel(self.box)
		self.semNoLabel.setGeometry(QtCore.QRect(100, 50, 21, 16))
		self.lectInfoLabel = QLabel(self.box)
		self.lectInfoLabel.setText("Лк:")
		self.lectInfoLabel.setGeometry(QtCore.QRect(130, 50, 31, 16))
		self.lectLabel = QLabel(self.box)
		self.lectLabel.setGeometry(QtCore.QRect(160, 50, 21, 16))
		self.labInfoLabel = QLabel(self.box)
		self.labInfoLabel.setText("Лаб:")
		self.labInfoLabel.setGeometry(QtCore.QRect(190, 50, 31, 16))
		self.labLabel = QLabel(self.box)
		self.labLabel.setGeometry(QtCore.QRect(230, 50, 21, 16))
		self.practInfoLabel = QLabel(self.box)
		self.practInfoLabel.setText("Пр:")
		self.practInfoLabel.setGeometry(QtCore.QRect(260, 50, 31, 16))
		self.practLabel = QLabel(self.box)
		self.practLabel.setGeometry(QtCore.QRect(290, 50, 21, 16))
		self.samInfoLabel = QLabel(self.box)
		self.samInfoLabel.setText("Ср:")
		self.samInfoLabel.setGeometry(QtCore.QRect(320, 50, 31, 16))
		self.samLabel = QLabel(self.box)
		self.samLabel.setGeometry(QtCore.QRect(350, 50, 21, 16))
		self.controlInfoLabel = QLabel(self.box)
		self.controlInfoLabel.setText("Контроль:")
		self.controlInfoLabel.setGeometry(QtCore.QRect(380, 50, 71, 16))
		self.controlLabel = QLabel(self.box)
		self.controlLabel.setGeometry(QtCore.QRect(460, 50, 41, 16))
		
		self.totalInfoLabel = QLabel(self.box)
		self.totalInfoLabel.setText("Всего часов:")
		self.totalInfoLabel.setGeometry(QtCore.QRect(10, 70, 91, 16))
		self.totalLabel = QLabel(self.box)
		self.totalLabel.setGeometry(QtCore.QRect(110, 70, 51, 16))
		
		self.relevantInfoLabel = QLabel(self.box)
		self.relevantInfoLabel.setText("Часов введено:")
		self.relevantInfoLabel.setGeometry(QtCore.QRect(10, 90, 111, 16))
		self.lectRelInfoLabel = QLabel(self.box)
		self.lectRelInfoLabel.setText("Лк:")
		self.lectRelInfoLabel.setGeometry(QtCore.QRect(130, 90, 31, 16))
		self.lectRelLabel = QLabel(self.box)
		self.lectRelLabel.setGeometry(QtCore.QRect(160, 90, 21, 16))
		self.labRelInfoLabel = QLabel(self.box)
		self.labRelInfoLabel.setText("Лаб:")
		self.labRelInfoLabel.setGeometry(QtCore.QRect(190, 90, 31, 16))
		self.labRelLabel = QLabel(self.box)
		self.labRelLabel.setGeometry(QtCore.QRect(230, 90, 21, 16))
		self.practRelInfoLabel = QLabel(self.box)
		self.practRelInfoLabel.setText("Пр:")
		self.practRelInfoLabel.setGeometry(QtCore.QRect(260, 90, 31, 16))
		self.practRelLabel = QLabel(self.box)
		self.practRelLabel.setGeometry(QtCore.QRect(290, 90, 21, 16))
		self.samRelInfoLabel = QLabel(self.box)
		self.samRelInfoLabel.setText("Ср:")
		self.samRelInfoLabel.setGeometry(QtCore.QRect(320, 90, 31, 16))
		self.samRelLabel = QLabel(self.box)
		self.samRelLabel.setGeometry(QtCore.QRect(350, 90, 21, 16))

		self.createModuleButton = QPushButton(self.box)
		self.createModuleButton.setText("+")
		self.createModuleButton.setGeometry(QtCore.QRect(10, 120, 31, 31))
		self.delModuleButton = QPushButton(self.box)
		self.delModuleButton.setText("-")
		self.delModuleButton.setGeometry(QtCore.QRect(43, 120, 31, 31))
		self.saveModuleButton = QPushButton(self.box)
		self.saveModuleButton.setText("Сохранить")
		self.saveModuleButton.setGeometry(QtCore.QRect(76, 120, 101, 31))
		
		self.moduleScrollArea = QScrollArea(self.box)
		self.moduleScrollArea.move(10, 160)
		self.moduleScrollArea.setFixedWidth(531)
		self.moduleScrollArea.setMinimumHeight(450)
		self.moduleScrollArea.setWidgetResizable(True)
		self.moduleScrollAreaWidgetContents = QWidget()
		self.moduleScrollAreaWidgetContents.setObjectName("moduleScrollAreaWidgetContents")
		self.moduleScrollArea.setWidget(self.moduleScrollAreaWidgetContents)

class RPD_Window(QMainWindow):
	"""Main Window class"""

	def __init__(self):
		"""Global fields initialization and elements' signals connection"""

		super(RPD_Window, self).__init__()

		self.ui = ui_RPD.Ui_MainWindow()
		self.ui.setupUi(self)

		self.PLAN_FNAME = None
		self.SAMPLE_FNAME = None
		self.RPD = None  # может не надо?
		self.RPD_PATH = None

		# list of QGroupBoxes to iterate over
		# [QGroupBox, QLabel - associated label from side panel, Bool - flag to make QGroupBox visible]
		self.BOXES = [[self.ui.uploadBox, self.ui.uploadBoxLabel, True],
			[self.ui.disciplineBox, self.ui.disciplineBoxLabel, False],
			[self.ui.competencyBox, self.ui.competencyBoxLabel, False],
			[self.ui.downloadBox, self.ui.label_15, False]]

		self.ui.backButton.clicked.connect(self.browseBox)  # можно перенести в handleCreateButtonClicked
		self.ui.forwButton.clicked.connect(self.browseBox)
		self.ui.study_planUploadButton.clicked.connect(self.handlePlanButtonClicked)
		self.ui.rpdUploadButton.clicked.connect(self.handleRpdButtonClicked)
		self.ui.createButton.clicked.connect(self.handleCreateButtonClicked)
		self.ui.dispShowButton.clicked.connect(self.handleDispShowButtonClicked)
		self.ui.downloadPathButton.clicked.connect(self.handleDownloadPathButtonClicked)
		self.ui.downloadButton.clicked.connect(self.handleDownloadButtonClicked)

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
					break
				elif self.sender().text() == "Вернуться назад" and i != 0:
					self.BOXES[i][2] = False
					self.BOXES[i][1].setFont(QtGui.QFont("MS Shell Dlg 2", 11, QtGui.QFont.Normal))
					self.BOXES[i][0].setVisible(False)
					self.BOXES[i-1][2] = True
					self.BOXES[i-1][1].setFont(QtGui.QFont("MS Shell Dlg 2", 11, QtGui.QFont.Bold))
					self.BOXES[i-1][0].setVisible(True)
					break
	
	def handlePlanButtonClicked(self):
		"""Initialize QFileDialog in response to button click. Show chosen path via label."""
		
		self.PLAN_FNAME = QFileDialog.getOpenFileName(self, 'Открыть учебный план', 'C:\\')[0]
		self.ui.study_planPathLabel.setText(self.PLAN_FNAME)

	def handleRpdButtonClicked(self):
		"""Initialize QFileDialog in response to button click. Show chosen path via label."""
		
		self.SAMPLE_FNAME = QFileDialog.getOpenFileName(self, 'Открыть шаблон', 'C:\\')[0]
		self.ui.rpdPathLabel.setText(self.SAMPLE_FNAME)

	def handleCreateButtonClicked(self):
		"""Create RPD instance with parameters set in the interface. 

		TODO: Exceptions
		"""
		
		if self.PLAN_FNAME != None and self.SAMPLE_FNAME != None:  # если оба файла заданы
			self.RPD = commutator.rpd(self.PLAN_FNAME, self.SAMPLE_FNAME)  # создаем экземпляр
			self.ui.uploadStatusLabel.setText('Успешно!')
			self.ui.dispComboBox.addItems(  # добавляем в ComboBox доступные дисциплины, объединяя их в строку
				[i[0] + ' ' + i[1] for i in self.RPD.STUDY_PLAN.list_avail_disciplines()])
			self.ui.dispShowButton.setEnabled(True)
			# self.ui.dispComboBox.activated.connect(self.on_dispComboBox_activated)
			# self.ui.dispShowButton.clicked.connect(self.handleDispShowButtonClicked)
		else:
			self.ui.uploadStatusLabel.setText('Не выбраны файлы!')

		self.sender().setDisabled(True)

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

		self.addBox(self.ui.compScrollAreaWidgetContents, competencyBox, 
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
			e = semesterBox(self.ui.centralwidget)  # создаем объект класса с родителем - главным виджетом окна
			e.setGeometry(QtCore.QRect(250, 0, 551, 601))
			e.setVisible(False)
			self.BOXES.insert(3 + i, [e, self.ui.label_4, False])  # добавляем новый объект в список вкладок после конкретной позиции
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
				e.moduleScrollAreaWidgetContents, moduleBox, 1))  # partial для вызова метода-приемника сигнала с параметрами
			e.delModuleButton.clicked.connect(partial(self.deleteBox,
				e.moduleScrollAreaWidgetContents))
			e.saveModuleButton.clicked.connect(partial(
				self.handleSaveModuleButtonClicked, 
				e.moduleScrollAreaWidgetContents,
				int(e.semNoLabel.text())))

		self.sender().setDisabled(True)

	def handleCompSaveButtonClicked(self, parent):
		
		textEdits = parent.findChildren(QTextEdit)
		
		for i in range(0, len(textEdits), 5):
			self.RPD.DISCIPLINE.COMPETENCIES[i//5]['part'] = textEdits[i + 1].toPlainText()
			self.RPD.DISCIPLINE.COMPETENCIES[i//5]['to_know'] = textEdits[i + 2].toPlainText()
			self.RPD.DISCIPLINE.COMPETENCIES[i//5]['to_can'] = textEdits[i + 3].toPlainText()
			self.RPD.DISCIPLINE.COMPETENCIES[i//5]['to_be_able'] = textEdits[i + 4].toPlainText()

		self.sender().setDisabled(True)

	def handleSpinBoxValueChanged(self, parent):
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
				
		for i in self.RPD.DISCIPLINE.SEMESTERS:
			if i[0] == semester:
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

		self.sender().setDisabled(True)  # деактивировать кнопку сохранения

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
		
		self.RPD.produce(self.RPD_PATH)
		os.system('explorer "{}"'.format(self.RPD_PATH))
		sys.exit()

	def connectModuleBox(addfunc):
		"""Decorator for addBox method. Connects added QSpinBoxes to local method"""

		def wrapper(self, parent, element, number):
			addfunc(self, parent, element, number)
			e = parent
			while not isinstance(e, semesterBox):  # найти тот элемент родитель, в котором есть нужные QLabel
				e = e.parent()
			for i in parent.findChildren(QSpinBox):
				i.valueChanged.connect(partial(self.handleSpinBoxValueChanged, e))
		
		return wrapper

	@connectModuleBox
	def addBox_module(self, parent, element, number):  #какая же это хуйня. 
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

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = RPD_Window()
	window.show()
	sys.exit(app.exec_())
