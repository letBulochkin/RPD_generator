from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from pycore import commutator
import sys, ui_RPD

class RPD_Window(QMainWindow):

	def __init__(self):

		super(RPD_Window, self).__init__()

		self.ui = ui_RPD.Ui_MainWindow()
		self.ui.setupUi(self)

		self.PLAN_FNAME = None
		self.SAMPLE_FNAME = None
		self.RPD = None

		self.BOXES = [[self.ui.uploadBox, self.ui.uploadBoxLabel, True], 
			[self.ui.disciplineBox, self.ui.disciplineBoxLabel, False]]

		self.ui.backButton.clicked.connect(self.browse_box)
		self.ui.forwButton.clicked.connect(self.browse_box)
		self.ui.study_planUploadButton.clicked.connect(self.on_planButton_clicked)
		self.ui.rpdUploadButton.clicked.connect(self.on_rpdButton_clicked)
		self.ui.createButton.clicked.connect(self.on_createButton_clicked)

	def browse_box(self):

		for i in range(len(self.BOXES)):
			if self.sender().text() == "Далее" and i != len(self.BOXES) - 1:
				if self.BOXES[i][2] == True:
					self.BOXES[i][2] = False
					self.BOXES[i][0].setVisible(False)
					self.BOXES[i+1][2] = True
					self.BOXES[i+1][0].setVisible(True)
			elif self.sender().text() == "Вернуться назад" and i != 0:
				if self.BOXES[i][2] == True:
					self.BOXES[i][2] = False
					self.BOXES[i][0].setVisible(False)
					self.BOXES[i-1][2] = True
					self.BOXES[i-1][0].setVisible(True)
	
	def on_planButton_clicked(self):
		
		self.PLAN_FNAME = QFileDialog.getOpenFileName(self, 'Открыть учебный план', 'C:\\')[0]
		self.ui.study_planPathLabel.setText(self.PLAN_FNAME)

	def on_rpdButton_clicked(self):
		
		self.SAMPLE_FNAME = QFileDialog.getOpenFileName(self, 'Открыть шаблон', 'C:\\')[0]
		self.ui.rpdPathLabel.setText(self.SAMPLE_FNAME)

	def on_createButton_clicked(self):
		"""TODO: Exceptions"""
		
		if self.PLAN_FNAME != None and self.SAMPLE_FNAME != None:
			self.RPD = commutator.rpd(self.PLAN_FNAME, self.SAMPLE_FNAME)
			self.ui.uploadStatusLabel.setText('Успешно!')
		else:
			self.ui.uploadStatusLabel.setText('Не выбраны файлы!')

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = RPD_Window()
	window.show()
	sys.exit(app.exec_())