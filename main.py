from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, 
	QFileDialog, QLabel, QLineEdit, QTextEdit, QGroupBox, 
	QFormLayout, QGridLayout, QVBoxLayout, QPushButton, QScrollArea,
	QSpinBox)
from pycore import commutator
from functools import partial
import sys, sip, ui_RPD

class competencyBox(QWidget):

	def __init__(self, parent):

		super(competencyBox, self).__init__(parent)

		self.compCodeLineEdit = QLineEdit()
		self.compDescrpTextEdit = QTextEdit()

		self.lay = QVBoxLayout(self)
		self.box = QGroupBox(self)
		self.lay.addWidget(self.box)
		self.form_lay = QFormLayout(self)
		self.form_lay.addRow(QLabel("Код: "), self.compCodeLineEdit)
		self.form_lay.addRow(QLabel("Описание: "), self.compDescrpTextEdit)

		self.box.setLayout(self.form_lay)
		self.box.setFixedSize(460, 240)

class moduleBox(QWidget):

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
		self.createModuleButton = QPushButton(self.box)
		self.createModuleButton.setText("+")
		self.createModuleButton.setGeometry(QtCore.QRect(10, 100, 31, 31))
		self.delModuleButton = QPushButton(self.box)
		self.delModuleButton.setText("-")
		self.delModuleButton.setGeometry(QtCore.QRect(43, 100, 31, 31))
		self.saveModuleButton = QPushButton(self.box)
		self.saveModuleButton.setText("Сохранить")
		self.saveModuleButton.setGeometry(QtCore.QRect(76, 100, 101, 31))
		self.moduleScrollArea = QScrollArea(self.box)
		self.moduleScrollArea.move(10, 140)
		self.moduleScrollArea.setFixedWidth(531)
		self.moduleScrollArea.setMinimumHeight(450)
		self.moduleScrollArea.setWidgetResizable(True)
		self.moduleScrollAreaWidgetContents = QWidget()
		self.moduleScrollAreaWidgetContents.setObjectName("moduleScrollAreaWidgetContents")
		self.moduleScrollArea.setWidget(self.moduleScrollAreaWidgetContents)

class RPD_Window(QMainWindow):

	def __init__(self):

		super(RPD_Window, self).__init__()

		self.ui = ui_RPD.Ui_MainWindow()
		self.ui.setupUi(self)

		self.PLAN_FNAME = None
		self.SAMPLE_FNAME = None
		self.RPD = None  # может не надо?
		self.RPD_PATH = None

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
					print(i, i+1)
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
		print("Tyler the creator!")
		if self.PLAN_FNAME != None and self.SAMPLE_FNAME != None:  # если оба файла заданы
			self.RPD = commutator.rpd(self.PLAN_FNAME, self.SAMPLE_FNAME)  # создаем экземпляр
			self.ui.uploadStatusLabel.setText('Успешно!')
			self.ui.dispComboBox.addItems(  # добавляем в ComboBox доступные дисциплины, объединяя их в строку
				[i[0] + ' ' + i[1] for i in self.RPD.STUDY_PLAN.list_avail_disciplines()])
			# self.ui.dispComboBox.activated.connect(self.on_dispComboBox_activated)
			# self.ui.dispShowButton.clicked.connect(self.handleDispShowButtonClicked)
		else:
			self.ui.uploadStatusLabel.setText('Не выбраны файлы!')

	def handleDispShowButtonClicked(self):
		"""Create discipline instance, fill the QLineEdits with information and add competency descriptions to the noext box

		ATTENTION: does not work if called multiple times! 
		"""

		self.RPD.create_discipline(
			self.ui.dispComboBox.itemText(
				self.ui.dispComboBox.currentIndex()).rsplit(' ')[0])
		self.ui.dispNameEdit.setText(self.RPD.DISCIPLINE.NAME)
		self.ui.dispFieldEdit.setText(self.RPD.STUDY_PLAN.FIELD_OF_KNOW)
		self.ui.dispProfileEdit.setText(self.RPD.STUDY_PLAN.PROFILE)
		self.ui.dispInstituteEdit.setText(self.RPD.STUDY_PLAN.INSTITUTE)
		self.ui.dispFormEdit.setText(self.RPD.STUDY_PLAN.EDU_FORMAT)
		self.ui.dispProgEdit.setText(self.RPD.STUDY_PLAN.EDU_PROG)
		self.ui.dispCathEdit.setText(self.RPD.STUDY_PLAN.CATHEDRA)
		if self.RPD.DISCIPLINE.PART == True:
			self.ui.dispPartBaseButton.setChecked(True)
		else:
			self.ui.dispPartVarButton.setChecked(True)
		if self.RPD.DISCIPLINE.OBLIGATION == True:
			self.ui.dispObligTrueButton.setChecked(True)
		else:
			self.ui.dispObligFalseButton.setChecked(True)

		self.addBox(self.ui.compScrollAreaWidgetContents, competencyBox, 
			len(self.RPD.DISCIPLINE.COMPETENCIES))
		lineEdits = self.ui.compScrollAreaWidgetContents.findChildren(QLineEdit)
		textEdits = self.ui.compScrollAreaWidgetContents.findChildren(QTextEdit)
		for i in range(len(lineEdits)):  # это наверняка можно оптимизировать
			lineEdits[i].setText(self.RPD.DISCIPLINE.COMPETENCIES[i][0])
		for i in range(len(textEdits)):
			textEdits[i].setText(self.RPD.DISCIPLINE.COMPETENCIES[i][1])

		self.ui.compAddButton.clicked.connect(partial(self.addBox,
			self.ui.compScrollAreaWidgetContents, competencyBox, 1))

		self.ui.compDelButton.clicked.connect(partial(self.deleteBox,
			self.ui.compScrollAreaWidgetContents))

		for i in range(len(self.RPD.DISCIPLINE.STUDY_HOURS)):
			e = semesterBox(self.ui.centralwidget)
			e.setGeometry(QtCore.QRect(250, 0, 551, 601))
			e.setVisible(False)
			self.BOXES.insert(3 + i, [e, self.ui.label_4, False])
			e.dicpNameLabel.setText(self.RPD.DISCIPLINE.NAME)
			e.semNoLabel.setText(str(self.RPD.DISCIPLINE.STUDY_HOURS[i][0]))
			e.lectLabel.setText(str(self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['lect']))
			e.labLabel.setText(str(self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['lab']))
			e.practLabel.setText(str(self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['pract']))
			e.samLabel.setText(str(self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['sam']))
			e.controlLabel.setText(str(self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['krpa'] 
				+ self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['control']))
			e.totalLabel.setText(str(self.RPD.DISCIPLINE.STUDY_HOURS[i][1]['total']))
			e.createModuleButton.clicked.connect(partial(self.addBox, 
				e.moduleScrollAreaWidgetContents, moduleBox, 1))
			e.delModuleButton.clicked.connect(partial(self.deleteBox,
				e.moduleScrollAreaWidgetContents))
			e.saveModuleButton.clicked.connect(partial(
				self.handleSaveModuleButtonClicked, 
				e.moduleScrollAreaWidgetContents,
				int(e.semNoLabel.text())))
			#e.createModuleButton.clicked.connect(lambda: self.addBox(
				#e.moduleScrollAreaWidgetContents, moduleBox, 1))
			print("Button!", e.createModuleButton)
			print("Del Button!", e.delModuleButton)
			print("SAWC!!!", e.moduleScrollAreaWidgetContents)

	def handleCompSaveButtonClicked(self):
		pass

	def handleSaveModuleButtonClicked(self, parent, semester):

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

		self.sender().setDisabled(True)

	def handleDownloadPathButtonClicked(self):
		
		dlg = QFileDialog()
		dlg.setFileMode(QFileDialog.Directory)
		self.RPD_PATH = dlg.getExistingDirectory(self, 'Сохранить рабочую программу', 'C\\')
		self.RPD_PATH = r"{}".format(self.RPD_PATH)
		self.RPD_PATH = self.RPD_PATH.replace('/', '\\')
		self.RPD_PATH = self.RPD_PATH + '\\'
		self.ui.downloadPathLabel.setText(self.RPD_PATH)

	def handleDownloadButtonClicked(self):
		
		self.RPD.produce(self.RPD_PATH)

	def addBox(self, parent, element, number):
		
		print("==SENDER==", self.sender())
		print("==PARENT==", parent)

		if not parent.findChildren(QVBoxLayout):
			vert_lay = QVBoxLayout(parent)
		else:
			vert_lay = parent.findChildren(QVBoxLayout)[0]

		for i in range(number):
			e = element(parent)
			vert_lay.addWidget(e)

		print(parent.findChildren(QVBoxLayout))

	def deleteBox(self, parent):

		print("==SENDER==", self.sender())
		print("==PARENT==", parent)
		print(parent.findChildren(QVBoxLayout))

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
